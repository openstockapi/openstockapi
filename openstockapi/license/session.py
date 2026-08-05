import os
import uuid
import platform
import hashlib
import httpx
from typing import Optional, Union

from openstockapi.core.types import DataTier
from openstockapi.core.exceptions import ApiKeyRequiredError
from openstockapi.config.settings import BACKEND_URL

def get_device_fingerprint() -> str:
    try:
        sys_info = f"{platform.node()}-{platform.system()}-{uuid.getnode()}"
        return hashlib.sha256(sys_info.encode()).hexdigest()[:32]
    except Exception:
        return "fallback_fingerprint_dev"

import threading
import time

class Session:
    """Manages API key authentication and resolves the current tier via server handshake."""
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENSTOCKAPI_KEY")
        if not self.api_key:
            raise ApiKeyRequiredError()
            
        self.session_token: Optional[str] = None
        self.tier = DataTier.FREE
        self._usage_counter = 0
        self._counter_lock = threading.Lock()
        self._heartbeat_interval = 15
        self._stop_heartbeat = threading.Event()
        self._heartbeat_thread = None

        self._handshake()

        if self.session_token and not self.session_token.startswith("mock_"):
            self._start_heartbeat_thread()

    def increment_usage(self) -> None:
        with self._counter_lock:
            self._usage_counter += 1

    def __del__(self) -> None:
        try:
            if hasattr(self, "_stop_heartbeat"):
                self._stop_heartbeat.set()
        except Exception:
            pass

    def _start_heartbeat_thread(self) -> None:
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    def _heartbeat_loop(self) -> None:
        while not self._stop_heartbeat.wait(self._heartbeat_interval):
            with self._counter_lock:
                count = self._usage_counter
                self._usage_counter = 0
            
            try:
                payload = {
                    "session_token": self.session_token,
                    "usage_counter_local": count
                }
                url = f"{BACKEND_URL}/v1/license/heartbeat"
                response = httpx.post(url, json=payload, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    new_token = data.get("session_token")
                    if new_token:
                        self.session_token = new_token
            except Exception:
                pass

    def _handshake(self) -> None:
        # Shortcut bare strings reserved for offline unit testing/development
        key = self.api_key.strip().lower()
        if key in ("free", "community", "pro", "premium"):
            self.session_token = f"mock_jwt_token_{key}"
            if "community" in key:
                self.tier = DataTier.COMMUNITY
            elif "pro" in key:
                self.tier = DataTier.PRO
            elif "premium" in key or "prem" in key:
                self.tier = DataTier.PREMIUM
            else:
                self.tier = DataTier.FREE
            return

        # Perform actual REST Handshake with Core Engine
        url = f"{BACKEND_URL}/v1/license/handshake"
        payload = {
            "api_key": self.api_key,
            "device_fingerprint": get_device_fingerprint(),
            "version": "0.1.0"
        }
        
        try:
            response = httpx.post(url, json=payload, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get("session_token")
                self._heartbeat_interval = data.get("heartbeat_interval", 15)
                tier_str = data.get("tier", "free").lower()
                if tier_str == "community":
                    self.tier = DataTier.COMMUNITY
                elif tier_str == "pro":
                    self.tier = DataTier.PRO
                elif tier_str in ("premium", "prem"):
                    self.tier = DataTier.PREMIUM
                else:
                    self.tier = DataTier.FREE
            elif response.status_code == 403:
                import logging
                err_detail = "Forbidden"
                try:
                    err_detail = response.json().get("detail", "Forbidden")
                except Exception:
                    pass
                logging.getLogger("openstockapi.session").warning(
                    f"Handshake failed (403): {err_detail}. Falling back to local tier check."
                )
                self._resolve_tier_fallback()
            elif response.status_code == 401:
                raise ApiKeyRequiredError()
            else:
                self._resolve_tier_fallback()
        except (httpx.RequestError, httpx.HTTPStatusError):
            self._resolve_tier_fallback()

    def _resolve_tier_fallback(self) -> None:
        key = self.api_key.strip().lower()
        if "community_" in key or key == "community":
            self.tier = DataTier.COMMUNITY
        elif "pro_" in key or key == "pro":
            self.tier = DataTier.PRO
        elif "premium_" in key or "prem_" in key or key == "premium" or "openstock_key_" in key:
            self.tier = DataTier.PREMIUM
        else:
            self.tier = DataTier.FREE
        self.session_token = f"mock_token_{self.tier.value}"


# Default global session singleton — requires init() or OPENSTOCKAPI_KEY env var
_current_session: Optional["Session"] = None

def get_current_session() -> "Session":
    global _current_session
    if _current_session is None:
        api_key = os.getenv("OPENSTOCKAPI_KEY")
        if api_key:
            _current_session = Session(api_key)
        else:
            # Fallback to anonymous free session if not initialized
            _current_session = Session("free")
    return _current_session

def set_current_session(session: Union["Session", str]) -> None:
    global _current_session
    if isinstance(session, str):
        _current_session = Session(session)
    else:
        _current_session = session


def init(api_key: str) -> None:
    """Initialize OpenStockAPI with your API key.
    
    Args:
        api_key: Your API key.
                 Register at: https://openstockapi.com/register
    """
    set_current_session(Session(api_key))

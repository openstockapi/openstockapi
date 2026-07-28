"""
CDK Schema Validator
=====================
Standalone schema validation for provider output — independent of pytest.
Can be used at runtime to validate data before it reaches the end user,
or in CI pipelines as a quality gate.

Usage:
    from openstockapi.cdk.validator import validate_ohlcv, validate_financial

    bars = provider.get_ohlcv("HPG", "1D", "2024-01-01", "2024-12-31")
    issues = validate_ohlcv(bars, symbol="HPG", provider_name="kbs")
    if issues:
        raise DataQualityError(issues)
"""

from datetime import datetime
from typing import List, Any, Optional
from dataclasses import dataclass, field


# ──────────────────────────────────────────────────────────────────────────────
# Validation result types
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ValidationIssue:
    """Represents a single schema validation failure."""
    rule_id: str      # e.g. "CDK-102"
    severity: str     # "ERROR" | "WARNING"
    message: str
    row_index: Optional[int] = None  # Index into the list, if applicable

    def __str__(self) -> str:
        location = f" [row {self.row_index}]" if self.row_index is not None else ""
        return f"[{self.severity}] {self.rule_id}{location}: {self.message}"


@dataclass
class ValidationResult:
    """Aggregate result of a validation run."""
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "ERROR"]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "WARNING"]

    def __str__(self) -> str:
        status = "PASSED" if self.passed else "FAILED"
        lines = [f"Validation {status} — {len(self.errors)} error(s), {len(self.warnings)} warning(s)"]
        lines.extend(str(i) for i in self.issues)
        return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# OHLCV Validator
# ──────────────────────────────────────────────────────────────────────────────

def validate_ohlcv(
    bars: List[Any],
    symbol: str,
    provider_name: str,
) -> ValidationResult:
    """
    Validate a list of OHLCVBar objects against CDK contract rules CDK-101 to CDK-109.

    Args:
        bars:          The list returned by provider.get_ohlcv().
        symbol:        The symbol that was requested.
        provider_name: The expected provider name (matches provider.name attribute).

    Returns:
        ValidationResult with all discovered issues.
    """
    issues: List[ValidationIssue] = []

    # CDK-101: Must be a non-empty list
    if not isinstance(bars, list):
        issues.append(ValidationIssue(
            rule_id="CDK-101",
            severity="ERROR",
            message=f"get_ohlcv() must return a list, got {type(bars).__name__}.",
        ))
        return ValidationResult(passed=False, issues=issues)

    if len(bars) == 0:
        issues.append(ValidationIssue(
            rule_id="CDK-101",
            severity="WARNING",
            message="get_ohlcv() returned an empty list. This may be expected for date ranges with no data.",
        ))
        return ValidationResult(passed=True, issues=issues)

    # Per-bar checks
    prev_ts = None
    for i, bar in enumerate(bars):
        # CDK-102: Price fields must be float and > 0
        for price_field in ("open", "high", "low", "close"):
            val = getattr(bar, price_field, None)
            if val is None or not isinstance(val, (int, float)):
                issues.append(ValidationIssue(
                    rule_id="CDK-102", severity="ERROR", row_index=i,
                    message=f"'{price_field}' is not a numeric type: {val!r}",
                ))
            elif val <= 0:
                issues.append(ValidationIssue(
                    rule_id="CDK-102", severity="ERROR", row_index=i,
                    message=f"'{price_field}' must be > 0, got {val}",
                ))

        # CDK-103: Volume must be numeric and >= 0
        vol = getattr(bar, "volume", None)
        if vol is None or not isinstance(vol, (int, float)):
            issues.append(ValidationIssue(
                rule_id="CDK-103", severity="ERROR", row_index=i,
                message=f"'volume' is not a numeric type: {vol!r}",
            ))
        elif vol < 0:
            issues.append(ValidationIssue(
                rule_id="CDK-103", severity="ERROR", row_index=i,
                message=f"'volume' must be >= 0, got {vol}",
            ))

        # CDK-104: Timestamp must be a datetime
        ts = getattr(bar, "timestamp", None)
        if not isinstance(ts, datetime):
            issues.append(ValidationIssue(
                rule_id="CDK-104", severity="ERROR", row_index=i,
                message=f"'timestamp' must be a datetime, got {type(ts).__name__}: {ts!r}",
            ))

        # CDK-105: Sorted ascending by timestamp
        if prev_ts is not None and isinstance(ts, datetime) and ts < prev_ts:
            issues.append(ValidationIssue(
                rule_id="CDK-105", severity="ERROR", row_index=i,
                message=f"Results not sorted ascending. Row {i} timestamp {ts} < previous {prev_ts}.",
            ))
        if isinstance(ts, datetime):
            prev_ts = ts

        # CDK-106: Symbol must match input
        bar_symbol = getattr(bar, "symbol", None)
        if bar_symbol != symbol:
            issues.append(ValidationIssue(
                rule_id="CDK-106", severity="ERROR", row_index=i,
                message=f"'symbol' mismatch: expected '{symbol}', got '{bar_symbol}'",
            ))

        # CDK-107: Provider name must match
        bar_provider = getattr(bar, "provider", None)
        if bar_provider != provider_name:
            issues.append(ValidationIssue(
                rule_id="CDK-107", severity="WARNING", row_index=i,
                message=f"'provider' mismatch: expected '{provider_name}', got '{bar_provider}'",
            ))

        # CDK-108: high >= open, close, low
        o = getattr(bar, "open", 0) or 0
        h = getattr(bar, "high", 0) or 0
        l = getattr(bar, "low", 0) or 0
        c = getattr(bar, "close", 0) or 0
        if h < o or h < c or h < l:
            issues.append(ValidationIssue(
                rule_id="CDK-108", severity="ERROR", row_index=i,
                message=f"OHLCV integrity: high ({h}) must be >= open ({o}), close ({c}), low ({l})",
            ))

        # CDK-109: low <= open, close, high
        if l > o or l > c or l > h:
            issues.append(ValidationIssue(
                rule_id="CDK-109", severity="ERROR", row_index=i,
                message=f"OHLCV integrity: low ({l}) must be <= open ({o}), close ({c}), high ({h})",
            ))

    passed = not any(i.severity == "ERROR" for i in issues)
    return ValidationResult(passed=passed, issues=issues)


# ──────────────────────────────────────────────────────────────────────────────
# Financial Statement Validator
# ──────────────────────────────────────────────────────────────────────────────

VALID_STMT_TYPES = {"income", "balance", "cashflow", "ratios"}
VALID_YEAR_RANGE = (2000, 2040)


def validate_financial(
    items: List[Any],
    symbol: str,
    stmt_type: str,
) -> ValidationResult:
    """
    Validate a list of FinancialItem objects against CDK contract rules CDK-201 to CDK-205.

    Args:
        items:     The list returned by provider.get_financial_statements().
        symbol:    The symbol that was requested.
        stmt_type: The statement type that was requested.

    Returns:
        ValidationResult with all discovered issues.
    """
    issues: List[ValidationIssue] = []

    if not isinstance(items, list):
        issues.append(ValidationIssue(
            rule_id="CDK-201", severity="ERROR",
            message=f"get_financial_statements() must return a list, got {type(items).__name__}.",
        ))
        return ValidationResult(passed=False, issues=issues)

    for i, item in enumerate(items):
        # CDK-202: statement_type must be a valid enum value
        s_type = getattr(item, "statement_type", None)
        if s_type not in VALID_STMT_TYPES:
            issues.append(ValidationIssue(
                rule_id="CDK-202", severity="ERROR", row_index=i,
                message=f"'statement_type' must be one of {VALID_STMT_TYPES}, got '{s_type}'",
            ))

        # CDK-203: year must be an int in valid range
        year = getattr(item, "year", None)
        if not isinstance(year, int):
            issues.append(ValidationIssue(
                rule_id="CDK-203", severity="ERROR", row_index=i,
                message=f"'year' must be an int, got {type(year).__name__}: {year!r}",
            ))
        elif not (VALID_YEAR_RANGE[0] <= year <= VALID_YEAR_RANGE[1]):
            issues.append(ValidationIssue(
                rule_id="CDK-203", severity="WARNING", row_index=i,
                message=f"'year' {year} is outside expected range {VALID_YEAR_RANGE}",
            ))

        # CDK-204: items dict values must be float or None — never strings
        raw_items = getattr(item, "items", {}) or {}
        for key, val in raw_items.items():
            if val is not None and not isinstance(val, (int, float)):
                issues.append(ValidationIssue(
                    rule_id="CDK-204", severity="ERROR", row_index=i,
                    message=f"Financial item '{key}' must be float or None, got {type(val).__name__}: {val!r}",
                ))

        # CDK-205: symbol must match
        item_symbol = getattr(item, "symbol", None)
        if item_symbol != symbol:
            issues.append(ValidationIssue(
                rule_id="CDK-205", severity="ERROR", row_index=i,
                message=f"'symbol' mismatch: expected '{symbol}', got '{item_symbol}'",
            ))

    passed = not any(i.severity == "ERROR" for i in issues)
    return ValidationResult(passed=passed, issues=issues)


# ──────────────────────────────────────────────────────────────────────────────
# Company Profile Validator
# ──────────────────────────────────────────────────────────────────────────────

def validate_company_profile(
    profile: Any,
    symbol: str,
) -> ValidationResult:
    """
    Validate a CompanyProfile object against CDK contract rules CDK-301 to CDK-304.

    Args:
        profile: The object returned by provider.get_company_profile().
        symbol:  The symbol that was requested.

    Returns:
        ValidationResult with all discovered issues.
    """
    issues: List[ValidationIssue] = []

    if profile is None:
        issues.append(ValidationIssue(
            rule_id="CDK-301", severity="ERROR",
            message="get_company_profile() returned None.",
        ))
        return ValidationResult(passed=False, issues=issues)

    # CDK-302: full_name must not be empty
    full_name = getattr(profile, "full_name", None)
    if not full_name or not str(full_name).strip():
        issues.append(ValidationIssue(
            rule_id="CDK-302", severity="ERROR",
            message=f"'full_name' must not be empty, got: {full_name!r}",
        ))

    # CDK-303: exchange must not be empty
    exchange = getattr(profile, "exchange", None)
    if not exchange or not str(exchange).strip():
        issues.append(ValidationIssue(
            rule_id="CDK-303", severity="ERROR",
            message=f"'exchange' must not be empty, got: {exchange!r}",
        ))

    # CDK-304: symbol must match
    profile_symbol = getattr(profile, "symbol", None)
    if profile_symbol != symbol:
        issues.append(ValidationIssue(
            rule_id="CDK-304", severity="ERROR",
            message=f"'symbol' mismatch: expected '{symbol}', got '{profile_symbol}'",
        ))

    passed = not any(i.severity == "ERROR" for i in issues)
    return ValidationResult(passed=passed, issues=issues)

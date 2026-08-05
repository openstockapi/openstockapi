import pytest
import openstockapi as osapi

def test_global_indices():
    # Test US index (S&P 500)
    gspc = osapi.ohlcv("^GSPC", market="US", resolution="1d", start="2026-01-01")
    assert len(gspc) > 0, "Failed to retrieve US index S&P 500 (^GSPC)"

    # Test JP index (Nikkei 225)
    n225 = osapi.ohlcv("^N225", market="JP", resolution="1d", start="2026-01-01")
    assert len(n225) > 0, "Failed to retrieve JP index Nikkei 225 (^N225)"

    # Test HK index (Hang Seng Index)
    hsi = osapi.ohlcv("^HSI", market="HK", resolution="1d", start="2026-01-01")
    assert len(hsi) > 0, "Failed to retrieve HK index Hang Seng (^HSI)"

    # Test CN index (CSI 300)
    csi300 = osapi.ohlcv("000300.SS", market="CN", resolution="1d", start="2026-01-01")
    assert len(csi300) > 0, "Failed to retrieve CN index CSI 300 (000300.SS)"

    # Test ASX index (S&P/ASX 200)
    axjo = osapi.ohlcv("^AXJO", market="ASX", resolution="1d", start="2026-01-01")
    assert len(axjo) > 0, "Failed to retrieve ASX index S&P/ASX 200 (^AXJO)"

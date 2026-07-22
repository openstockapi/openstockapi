import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (tai khoan Free)
set_current_session("free")


# ============================================================
# Use Case 1.1 — Du lieu gia lich su OHLCV (Dong bo)
# ============================================================

# resolution: "1D" = theo ngay, "1W" = theo tuan, "1M" = theo thang
# provider (tu chon): "dnse", "kbs", "vci" (bo qua hoac provider=None de tu dong chon nguon)
data = osapi.ohlcv(
    symbol="VNM",
    resolution="1D",
    start="2025-01-01",
    end="2025-06-30",
    provider="kbs"  # Tu chon nguon thu cong: "dnse", "kbs", "vci"
)


# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in data])

# Xem 5 dong dau tien
df.head()

# Luu du lieu ra file Excel
df.to_excel("VNM_ohlcv.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_ohlcv.xlsx'")


# ============================================================
# Use Case 1.2 — Du lieu OHLCV bat dong bo (Async)
# ============================================================

import asyncio

# Lay dong thoi 3 ma co phieu cung luc
vnm_data, fpt_data, vic_data = asyncio.run(asyncio.gather(
    osapi.async_ohlcv("VNM", resolution="1D", start="2025-01-01", end="2025-06-30"),
    osapi.async_ohlcv("FPT", resolution="1D", start="2025-01-01", end="2025-06-30"),
    osapi.async_ohlcv("VIC", resolution="1D", start="2025-01-01", end="2025-06-30"),
))

# Gop tat ca vao mot DataFrame
df_vnm = pd.DataFrame([e.model_dump() for e in vnm_data])
df_fpt = pd.DataFrame([e.model_dump() for e in fpt_data])
df_vic = pd.DataFrame([e.model_dump() for e in vic_data])

# Luu ra 3 sheet trong cung 1 file Excel
with pd.ExcelWriter("multi_ohlcv.xlsx") as writer:
    df_vnm.to_excel(writer, sheet_name="VNM", index=False)
    df_fpt.to_excel(writer, sheet_name="FPT", index=False)
    df_vic.to_excel(writer, sheet_name="VIC", index=False)

print("Da luu du lieu vao file 'multi_ohlcv.xlsx'")


# ============================================================
# Use Case 1.3 — Ho so cong ty (Company Profile)
# ============================================================

profile = osapi.profile("VNM")

# Chuyen sang DataFrame (1 dong)
df = pd.DataFrame([profile.model_dump()])

# Xem du lieu
df.head()

# Luu ra file Excel
df.to_excel("VNM_profile.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_profile.xlsx'")


# ============================================================
# Use Case 1.4 — Bao gia thoi gian thuc [Yeu cau Pro]
# ============================================================

# Thiet lap lai session voi API key Pro
set_current_session("YOUR_PRO_API_KEY")

quote = osapi.quote("VNM")

# Chuyen sang DataFrame (1 dong)
df = pd.DataFrame([quote.model_dump()])

# Xem du lieu
df.head()

# Luu ra file Excel
df.to_excel("VNM_quote.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_quote.xlsx'")

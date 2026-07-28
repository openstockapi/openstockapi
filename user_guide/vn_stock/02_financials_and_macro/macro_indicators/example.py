import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (tai khoan Free)
set_current_session("free")


# ============================================================
# Use Case 5.1 — Lay cac chi so vi mo
# ============================================================

# Lay du lieu cung tien M2, tin dung he thong ngan hang
data = osapi.indicators()

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in data])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("macro_indicators.xlsx", index=False)
print("Da luu du lieu vao file 'macro_indicators.xlsx'")


# ============================================================
# Use Case 5.2 — Toc do tang truong M2 va Tin dung
# ============================================================

# Loc chi so Cung tien M2
df_m2 = df[df["indicator_name"] == "Cung tien M2"].copy()
df_m2 = df_m2.sort_values("date").reset_index(drop=True)

# Tinh tang truong thang/thang (MoM)
df_m2["mom_growth_pct"] = df_m2["value"].pct_change() * 100

# Xem ket qua
df_m2.head()

# Luu ra file Excel
df_m2.to_excel("m2_growth.xlsx", index=False)
print("Da luu du lieu vao file 'm2_growth.xlsx'")


# ============================================================
# Use Case 5.3 — Ket hop vi mo voi du lieu co phieu ngan hang
# ============================================================

# Lay gia co phieu nhom ngan hang
vcb_ohlcv = osapi.ohlcv("VCB", resolution="1M", start="2024-01-01", end="2025-06-30")
bid_ohlcv = osapi.ohlcv("BID", resolution="1M", start="2024-01-01", end="2025-06-30")

df_vcb = pd.DataFrame([e.model_dump() for e in vcb_ohlcv])
df_bid = pd.DataFrame([e.model_dump() for e in bid_ohlcv])

# Luu tat ca ra 1 file Excel voi nhieu sheet
with pd.ExcelWriter("macro_bank_analysis.xlsx") as writer:
    df.to_excel(writer, sheet_name="Macro Indicators", index=False)
    df_vcb.to_excel(writer, sheet_name="VCB OHLCV", index=False)
    df_bid.to_excel(writer, sheet_name="BID OHLCV", index=False)

print("Da luu du lieu vao file 'macro_bank_analysis.xlsx'")

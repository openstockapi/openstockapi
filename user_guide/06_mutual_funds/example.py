import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (tai khoan Free)
set_current_session("free")


# ============================================================
# Use Case 6.1 — Xem chi tiet mot quy mo
# ============================================================

# Fund ID tren Fmarket: VESAF = 23, VFMVSF = 27, DCVFMVN30 = 35, BVPF = 9
fund = osapi.fund_details(23)

# Chuyen thong tin co ban sang DataFrame (1 dong)
df_info = pd.DataFrame([{
    "name": fund.name,
    "nav": fund.nav,
    "management_fee": fund.management_fee,
    "total_assets": fund.total_assets,
}])

# Xem du lieu
df_info.head()

# Luu ra file Excel
df_info.to_excel("VESAF_info.xlsx", index=False)
print("Da luu du lieu vao file 'VESAF_info.xlsx'")


# ============================================================
# Use Case 6.2 — Xem danh muc nam giu (Top Holdings)
# ============================================================

# Chuyen danh sach holdings sang DataFrame
df_holdings = pd.DataFrame([h.model_dump() for h in fund.holdings])

# Xem 10 dong dau tien
df_holdings.head(10)

# Luu ra file Excel
df_holdings.to_excel("VESAF_holdings.xlsx", index=False)
print("Da luu du lieu vao file 'VESAF_holdings.xlsx'")


# ============================================================
# Use Case 6.3 — So sanh nhieu quy mo
# ============================================================

# Lay thong tin cua nhieu quy
vesaf     = osapi.fund_details(23)
vfmvsf    = osapi.fund_details(27)
dcvfmvn30 = osapi.fund_details(35)
bvpf      = osapi.fund_details(9)

# Tao DataFrame so sanh
df_compare = pd.DataFrame([
    {"ticker": "VESAF",      "nav": vesaf.nav,     "management_fee": vesaf.management_fee,     "total_assets": vesaf.total_assets},
    {"ticker": "VFMVSF",     "nav": vfmvsf.nav,    "management_fee": vfmvsf.management_fee,    "total_assets": vfmvsf.total_assets},
    {"ticker": "DCVFMVN30",  "nav": dcvfmvn30.nav, "management_fee": dcvfmvn30.management_fee, "total_assets": dcvfmvn30.total_assets},
    {"ticker": "BVPF",       "nav": bvpf.nav,       "management_fee": bvpf.management_fee,      "total_assets": bvpf.total_assets},
])

# Xem du lieu
df_compare.head()

# Luu ra file Excel
df_compare.to_excel("fund_comparison.xlsx", index=False)
print("Da luu du lieu vao file 'fund_comparison.xlsx'")

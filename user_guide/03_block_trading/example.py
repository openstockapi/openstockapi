import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (yeu cau tai khoan Pro)
set_current_session("YOUR_PRO_API_KEY")


# ============================================================
# Use Case 3.1 — Giao dich khoi ngoai (Foreign Trading)
# ============================================================

# Lay 20 phien giao dich cua nha dau tu nuoc ngoai tren ma VNM
foreign = osapi.foreign("VNM", limit=20)

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in foreign])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("VNM_foreign_trading.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_foreign_trading.xlsx'")


# ============================================================
# Use Case 3.2 — Giao dich tu doanh (Proprietary Trading)
# ============================================================

prop = osapi.prop_trade("HPG", limit=10)

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in prop])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("HPG_prop_trade.xlsx", index=False)
print("Da luu du lieu vao file 'HPG_prop_trade.xlsx'")


# ============================================================
# Use Case 3.3 — Giao dich noi bo / Co dong lon (Insider Trading)
# ============================================================

insider = osapi.insider("FPT", limit=10)

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in insider])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("FPT_insider_trading.xlsx", index=False)
print("Da luu du lieu vao file 'FPT_insider_trading.xlsx'")


# ============================================================
# Use Case 3.4 — Phan tich dong tien ngoai (30 phien)
# ============================================================

foreign30 = osapi.foreign("VNM", limit=30)

# Chuyen sang DataFrame de tinh toan
df = pd.DataFrame([e.model_dump() for e in foreign30])

# Tinh tong mua, ban va mua/ban rong
total_buy  = df["buy_volume"].sum()
total_sell = df["sell_volume"].sum()
net        = total_buy - total_sell

print("Tong mua    :", total_buy)
print("Tong ban    :", total_sell)
print("Mua/Ban rong:", net)

# Luu ra file Excel
df.to_excel("VNM_foreign_30sessions.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_foreign_30sessions.xlsx'")

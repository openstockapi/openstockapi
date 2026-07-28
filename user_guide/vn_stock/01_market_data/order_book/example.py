import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session

# Thiet lap session (yeu cau tai khoan Pro)
set_current_session("YOUR_PRO_API_KEY")


# ============================================================
# Use Case 4.1 — Gia mua/ban tot nhat (Bid/Ask Spread)
# ============================================================

# Lay gia mua tot nhat va gia ban tot nhat cua ma VNM
data = osapi.bid_ask("VNM")

# Chuyen sang DataFrame (1 dong)
df = pd.DataFrame([data.model_dump()])

# Xem du lieu
df.head()

# Luu ra file Excel
df.to_excel("VNM_bid_ask.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_bid_ask.xlsx'")


# ============================================================
# Use Case 4.2 — Do sau so lenh (Market Depth)
# ============================================================

# Lay toan bo cac muc gia mua va ban trong so lenh
depth = osapi.depth("VNM")

# Chuyen Ask va Bid sang DataFrame rieng biet
df_ask = pd.DataFrame([l.model_dump() for l in depth.ask_levels])
df_bid = pd.DataFrame([l.model_dump() for l in depth.bid_levels])

# Xem du lieu
print("Ben ban (Ask):")
df_ask.head()

print("Ben mua (Bid):")
df_bid.head()

# Luu ra 2 sheet trong cung 1 file Excel
with pd.ExcelWriter("VNM_order_book.xlsx") as writer:
    df_ask.to_excel(writer, sheet_name="Ask (Ben ban)", index=False)
    df_bid.to_excel(writer, sheet_name="Bid (Ben mua)", index=False)

print("Da luu du lieu vao file 'VNM_order_book.xlsx'")


# ============================================================
# Use Case 4.3 — Order Book Imbalance (OBI)
# ============================================================

# Tinh OBI tu DataFrame da co san
total_bid = df_bid["volume"].sum()
total_ask = df_ask["volume"].sum()
obi       = (total_bid - total_ask) / (total_bid + total_ask)

# Tong hop ket qua vao DataFrame de luu
df_obi = pd.DataFrame([{
    "symbol": "VNM",
    "total_bid_volume": total_bid,
    "total_ask_volume": total_ask,
    "obi": round(obi, 4),
}])

df_obi.head()

# Luu ra file Excel
df_obi.to_excel("VNM_obi.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_obi.xlsx'")

import pandas as pd
import openstockapi as osapi
from openstockapi.license.session import set_current_session
from datetime import datetime

# Thiet lap session (tai khoan Free)
set_current_session("free")


# ============================================================
# Use Case 7.1 — Lay tin tuc doanh nghiep
# ============================================================

# Lay 15 tin tuc moi nhat cua ma VNM
news = osapi.company_news("VNM", limit=15)

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in news])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("VNM_news.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_news.xlsx'")


# ============================================================
# Use Case 7.2 — Lay su kien doanh nghiep
# ============================================================

# Lay cac su kien quan trong: chia co tuc, hop DHDCD, phat hanh them...
events = osapi.company_events("FPT", limit=10)

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in events])

# Xem 5 dong dau tien
df.head()

# Luu ra file Excel
df.to_excel("FPT_events.xlsx", index=False)
print("Da luu du lieu vao file 'FPT_events.xlsx'")


# ============================================================
# Use Case 7.3 — Tin tuc theo danh muc theo doi
# ============================================================

# Lay tin tuc moi nhat cua nhieu ma cung luc
watchlist = ["VNM", "FPT", "VIC", "HPG", "MBB"]

rows = []
for symbol in watchlist:
    latest = osapi.company_news(symbol, limit=1)
    rows.append({
        "symbol": symbol,
        "date": latest[0].published_at.date(),
        "title": latest[0].title,
        "source": latest[0].source,
        "url": latest[0].url,
    })

df = pd.DataFrame(rows)

# Xem ket qua
df.head()

# Luu ra file Excel
df.to_excel("watchlist_news.xlsx", index=False)
print("Da luu du lieu vao file 'watchlist_news.xlsx'")


# ============================================================
# Use Case 7.4 — Canh bao su kien sap toi
# ============================================================

# Loc cac su kien trong tuong lai
all_events = osapi.company_events("VNM", limit=20)
today      = datetime.today()

upcoming = [e for e in all_events if e.event_date >= today]

# Chuyen sang DataFrame
df = pd.DataFrame([e.model_dump() for e in upcoming])

# Xem ket qua
df.head()

# Luu ra file Excel
df.to_excel("VNM_upcoming_events.xlsx", index=False)
print("Da luu du lieu vao file 'VNM_upcoming_events.xlsx'")

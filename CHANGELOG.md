# Changelog

Tất cả các thay đổi đáng chú ý của dự án **OpenStockAPI** sẽ được ghi nhận tại đây theo chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [v0.1.1] - 2026-07-21

### Thêm mới (Added)
- Hỗ trợ đa thị trường (Multi-market) với tham số `market="VN"` hoặc `market="US"`.
- Hỗ trợ định danh ký hiệu mã cổ phiếu theo dạng `AAPL.US`, `VNM.VN`.
- Bộ kịch bản kiểm thử chấp nhận người dùng (UAT) tự động `uat/run_uat.py` xuất kết quả định dạng JSON kèm dấu mốc thời gian (timestamp).
- Kịch bản đóng gói và tự động hóa phát hành lên PyPI `scripts/publish.py` và `publish.ps1`.
- Tài liệu hướng dẫn Re-deploy PyPI tại `docs/pyPI_redeployment/README.md`.

### Thay đổi (Changed)
- Cho phép truyền trực tiếp chuỗi API Key vào `set_current_session("YOUR_KEY")`.
- Cấu trúc lại danh sách ưu tiên Provider (`DEFAULT_PROVIDER_PRIORITY`) phân nhóm theo thị trường.

---

## [v0.1.0] - 2026-07-20

### Thêm mới (Added)
- Khởi tạo dự án Data Plane mã nguồn mở theo Apache License 2.0.
- Các module tích hợp dữ liệu chứng khoán Việt Nam:
  - `stock`: OHLCV lịch sử (DNSE), Company Profile (VNDirect), Realtime Quote (DNSE/VCI).
  - `financial`: Bảng CĐKT, KQKD, LCTT, Chỉ số tài chính (MAS GraphQL).
  - `trading`: Giao dịch khối ngoại, tự doanh, nội bộ (VCI Vietcap).
  - `orderbook`: Giá mua/bán tốt nhất, độ sâu sổ lệnh.
  - `macro`: Cung tiền M2, Tín dụng NHNN (Maybank).
  - `fund`: Thông tin chi tiết quỹ mở & danh mục nắm giữ (Fmarket).
  - `news`: Tin tức & Sự kiện doanh nghiệp (KB Securities).
- Đăng ký package đầu tiên lên PyPI.

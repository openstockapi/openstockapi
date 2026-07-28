# ⚖️ Điều khoản Dịch vụ & Tuyên bố Từ chối Trách nhiệm

Cảm ơn bạn đã sử dụng **OpenStockAPI**. Thư viện mã nguồn mở này kết nối trực tiếp đến các API công khai của các tổ chức tài chính, công ty chứng khoán, sàn giao dịch tài sản số và quỹ mở.

Bằng việc tích hợp hoặc sử dụng thư viện này, bạn thừa nhận và đồng ý với các điều khoản, tuyên bố miễn trừ trách nhiệm và hướng dẫn tuân thủ dữ liệu của bên thứ ba dưới đây.

---

## 1. Tuyên bố Miễn trừ Trách nhiệm Chung

*   **Mục đích Học thuật và Nghiên cứu:** OpenStockAPI là dự án nguồn mở phi thương mại được phát triển thuần túy phục vụ mục đích học tập, nghiên cứu và phát triển cá nhân. Dự án không cung cấp bất kỳ dịch vụ phân phối lại dữ liệu thương mại nào.
*   **Không phải Lời khuyên Tài chính:** Toàn bộ thông tin thu thập được từ thư viện này chỉ mang tính chất tham khảo. Nhà phát triển và những người đóng góp không chịu trách nhiệm đối với bất kỳ quyết định đầu tư, tổn thất tài chính hoặc rủi ro pháp lý nào phát sinh từ việc sử dụng dữ liệu này.
*   **Độ trễ và Tính chính xác:** Dữ liệu được truy xuất trực tiếp từ các hệ thống của bên thứ ba. Chúng tôi không cam kết bảo đảm tính chính xác, đầy đủ hoặc liên tục của dữ liệu. Dữ liệu có thể bị trễ (delayed) hoặc tạm ngừng theo chính sách của từng nhà cung cấp.

---

## 2. Tuân thủ Điều khoản của Nhà cung cấp (ToS)

Các nhà cung cấp dữ liệu (công ty chứng khoán, công ty quản lý quỹ, sàn giao dịch tài sản số) đều có Điều khoản Dịch vụ (ToS) riêng. Khi sử dụng OpenStockAPI, bạn đang gián tiếp tương tác với các hệ thống này và phải tuân thủ các quy tắc sau:

### 2.1 Chỉ Sử dụng Phi thương mại & Cá nhân
Hầu hết các nhà cung cấp quy định rõ:
*   Dữ liệu bảng giá, thông tin tài chính và doanh nghiệp chỉ được cung cấp cho mục đích sử dụng cá nhân, phi thương mại.
*   Nghiêm cấm hành vi đóng gói, thương mại hóa hoặc phân phối lại (redistribute) dữ liệu cho bên thứ ba khi chưa có sự đồng ý chính thức bằng văn bản từ nhà cung cấp dữ liệu gốc.

### 2.2 Tần suất Truy cập Hợp lý (Fair Use & Rate Limiting)
Hành vi gửi yêu cầu liên tục với tần suất cao (scraping/spamming) có thể bị coi là lạm dụng tài nguyên hệ thống:
*   **Rate Limiting:** Vui lòng tuân thủ cấu hình phân tầng truy cập của OpenStockAPI hoặc tự triển khai cơ chế delay/throttling trong mã nguồn của bạn.
*   **Cơ chế Cache:** Hãy chủ động lưu trữ tạm thời (cache) dữ liệu tĩnh (như thông tin doanh nghiệp, báo cáo tài chính lịch sử) thay vì gửi yêu cầu lặp đi lặp lại nhiều lần trong khoảng thời gian ngắn.
*   **Tính toàn vẹn hệ thống:** Tránh tạo các vòng lặp vô hạn gọi API liên tục mà không có thời gian nghỉ (sleep).

### 2.3 Rủi ro Kỹ thuật và Bảo mật
*   **Thay đổi API:** Các nhà cung cấp có quyền thay đổi cấu trúc URL endpoint, payload hoặc chặn địa chỉ IP truy cập bất cứ lúc nào mà không cần báo trước.
*   **Xác thực và Bảo mật:** Đối với các API yêu cầu API Key hoặc tài khoản, bạn phải tự chịu trách nhiệm bảo mật thông tin của mình. OpenStockAPI không lưu trữ hay truyền thông tin xác thực này (toàn bộ chạy cục bộ trên máy của bạn).

---

## 3. Điều khoản Đặc thù theo Sản phẩm

Khi dự án mở rộng, vui lòng tham khảo tài liệu hướng dẫn cụ thể trong từng phân mục:
*   **Thị trường Chứng khoán Việt Nam:** Tham khảo [Vietnam Stock Terms and Disclaimer](./vn_stock/terms_and_disclaimer.md) để biết chi tiết về chính sách của TCBS, Vietcap, KB Securities, DNSE, và Fmarket.
*   **Thị trường Quốc tế / Crypto / Forex:** Tham khảo hướng dẫn tương ứng tại các thư mục con khi được giới thiệu.

---

## 4. Giới hạn Trách nhiệm pháp lý

Trong mọi trường hợp, các nhà phát triển và người đóng góp cho OpenStockAPI không chịu trách nhiệm đối với bất kỳ thiệt hại trực tiếp, gián tiếp, ngẫu nhiên hoặc do hậu quả nào phát sinh từ việc sử dụng hoặc không thể sử dụng phần mềm này.

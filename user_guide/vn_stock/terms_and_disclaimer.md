# ⚖️ Tuyên bố từ chối trách nhiệm & Hướng dẫn tuân thủ ToS Nhà cung cấp
## Disclaimer & Data Provider Terms of Service Compliance

Cảm ơn bạn đã sử dụng **OpenStockAPI**. Thư viện này kết nối trực tiếp đến các API công khai của các tổ chức tài chính, công ty chứng khoán và quỹ mở tại Việt Nam. 

Trước khi tích hợp hoặc sử dụng thư viện này vào hệ thống của bạn, vui lòng đọc kỹ các điều khoản và hướng dẫn dưới đây để đảm bảo tuân thủ đầy đủ về mặt pháp lý và kỹ thuật.

---

## 1. Tuyên bố từ chối trách nhiệm (Disclaimer)

*   **Mục đích học thuật và nghiên cứu:** OpenStockAPI là dự án nguồn mở phi thương mại được phát triển cho mục đích học tập, nghiên cứu và phát triển cá nhân. Dự án không cung cấp bất kỳ dịch vụ phân phối lại dữ liệu thương mại nào.
*   **Không phải lời khuyên tài chính:** Toàn bộ thông tin thu thập được từ thư viện này chỉ mang tính chất tham khảo. Chúng tôi không chịu trách nhiệm đối với bất kỳ quyết định đầu tư, tổn thất tài chính hoặc rủi ro pháp lý nào phát sinh từ việc sử dụng dữ liệu này.
*   **Độ trễ và Tính chính xác:** Dữ liệu được truy xuất trực tiếp từ các hệ thống của bên thứ ba. Chúng tôi không cam kết, đảm bảo tính chính xác, đầy đủ hoặc liên tục của dữ liệu. Dữ liệu có thể bị trễ (delayed) hoặc tạm ngừng theo chính sách của từng nhà cung cấp.

---

## 2. Hướng dẫn tuân thủ Điều khoản sử dụng của Nhà cung cấp (Data Provider ToS)

Các nhà cung cấp dữ liệu (như **TCBS, Vietcap, KB Securities, Fmarket, MAS, DNSE, VNDirect**) đều có các điều khoản và điều kiện dịch vụ (Terms of Service - ToS) riêng được công bố trên website chính thức của họ. Khi sử dụng OpenStockAPI, bạn được coi là đang gián tiếp giao tiếp với các hệ thống này và phải tuân thủ các quy tắc sau:

### 2.1 Sử dụng phi thương mại & cá nhân (Personal & Non-Commercial Use Only)
Hầu hết các điều khoản dịch vụ của công ty chứng khoán quy định rõ:
*   Dữ liệu bảng giá, thông tin tài chính và sự kiện chỉ được cung cấp cho mục đích sử dụng cá nhân của khách hàng.
*   Nghiêm cấm hành vi đóng gói, thương mại hóa hoặc phân phối lại (redistribute) dữ liệu cho bên thứ ba khi chưa có sự đồng ý chính thức bằng văn bản từ nhà cung cấp dữ liệu gốc.

### 2.2 Tần suất truy cập hợp lý (Fair Use & Rate Limiting)
Các hành vi gửi yêu cầu liên tục với tần suất cao (scraping/spamming) có thể bị coi là tấn công từ chối dịch vụ (DoS) hoặc lạm dụng tài nguyên hệ thống:
*   **Rate Limiting:** Vui lòng tuân thủ cấu hình phân tầng truy cập của OpenStockAPI hoặc tự triển khai cơ chế delay/throttling trong code của bạn.
*   **Bảo vệ hệ thống:** Tránh tạo các vòng lặp vô hạn (infinite loops) gọi API liên tục mà không có thời gian nghỉ (sleep).
*   **Cơ chế Cache:** Hãy chủ động lưu trữ tạm thời (cache) dữ liệu tĩnh (như thông tin doanh nghiệp, báo cáo tài chính lịch sử) thay vì gửi yêu cầu lặp đi lặp lại nhiều lần trong khoảng thời gian ngắn.

### 2.3 Rủi ro kỹ thuật và bảo mật
*   **Thay đổi cấu trúc API:** Các nhà cung cấp có quyền thay đổi cấu trúc URL endpoint, payload hoặc chặn địa chỉ IP truy cập bất cứ lúc nào mà không cần báo trước.
*   **Xác thực tài khoản (Authentication):** Đối với các dịch vụ yêu cầu tài khoản cá nhân, bạn phải tự chịu trách nhiệm bảo mật thông tin đăng nhập và API Key của mình. OpenStockAPI không lưu trữ thông tin này trên máy chủ trung gian (hoạt động hoàn toàn cục bộ trên máy của bạn).

---

## 3. Danh sách ToS tham chiếu của các Nhà cung cấp lớn

Để đảm bảo an toàn pháp lý cao nhất, chúng tôi khuyến cáo bạn nên truy cập và đọc trực tiếp điều khoản dịch vụ của từng bên:

1.  **Techcom Securities (TCBS):** [Điều khoản giao dịch điện tử và sử dụng dịch vụ TCInvest](https://www.tcbs.com.vn)
2.  **Vietcap Securities (Vietcap):** [Điều khoản sử dụng và chính sách bảo mật thông tin Vietcap](https://www.vietcap.com.vn)
3.  **KB Securities Vietnam (KBSec):** [Điều khoản dịch vụ giao dịch trực tuyến KB Buddy](https://www.kbsec.com.vn)
4.  **Fmarket (Công nghệ tài chính Fmarket):** [Quy chế hoạt động và bảo mật thông tin quỹ mở Fmarket](https://fmarket.vn)
5.  **DNSE (Chứng khoán DNSE):** [Điều khoản sử dụng nền tảng giao dịch Entrade X](https://www.dnse.com.vn)

---

## 4. Trách nhiệm pháp lý của Người dùng cuối

Bằng việc sử dụng OpenStockAPI, bạn thừa nhận và đồng ý rằng:
*   Bạn chịu toàn bộ trách nhiệm trước pháp luật và các nhà cung cấp dữ liệu nếu có bất kỳ tranh chấp hoặc khiếu nại nào liên quan đến hành vi sử dụng dữ liệu sai mục đích.
*   Nhà phát triển và những người đóng góp cho OpenStockAPI được miễn trừ hoàn toàn khỏi mọi nghĩa vụ liên quan đến thiệt hại trực tiếp hoặc gián tiếp gây ra bởi ứng dụng của bạn.

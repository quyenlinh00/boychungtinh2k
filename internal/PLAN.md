# 1.000$ trong tháng 10 — Kế hoạch có số

> Tài liệu nội bộ. Repo này đang để **public** — trước khi merge, chuyển thư mục `internal/` sang repo private.

## 1. Nói thật trước

- Không ai hứa chắc được 1.000$, kể cả mình. Mình không tự nhận tiền được. Mình dựng máy bán hàng, bạn là người nhắn tin và chốt.
- Mục tiêu đổi ra tiền Việt: **~26,5 triệu đ** (tỷ giá quanh 26.100–26.500 đ/USD trong các nguồn mình tìm được, chưa có số đúng ngày hôm nay — bạn kiểm lại ở Vietcombank trước khi chốt).
- Còn **24 ngày** (7/10 → 31/10). Tiền phải **vào tài khoản** trước 31/10, không phải "đã chốt".

## 2. Vì sao không phải thử thách 21 ngày (ở dạng hiện tại)

Trang thử thách đang bán: 20 suất × cọc 300k, **hoàn 100% nếu làm đủ**.
- Tối đa thu: 20 × 300k = **6 triệu đ (~226$)**, và nếu mọi người làm đủ thì doanh thu thật gần như **bằng 0**.
- Để chạm 26,5 triệu bằng gói 199k cần ~133 người, bằng gói 399k cần ~67 người. Trang cũng ghi bắt đầu 15/4/2026 — đã cũ 6 tháng.
- Kết luận: cấu trúc đó đo cam kết, không phải kiếm tiền. Nó vẫn là sản phẩm tốt, chỉ là không phải đường ngắn nhất tới 1.000$ trong 24 ngày. Xem mục 8 nếu muốn sửa giá.

## 3. Đường chính: "Website 48 Giờ" cho tiệm nhỏ

Lý do chọn: bạn đã có sẵn nguyên liệu (bản demo Phố Cổ Barbershop, quy trình Claude + Antigravity), bán cho doanh nghiệp thật nên giá cao hơn bán cho cá nhân, và **ít khách cũng đủ**.

Trang bán hàng: `index.html` ở thư mục gốc (đã dựng, 3 gói).

| Gói | Giá đề xuất | Ghi chú |
|---|---|---|
| Khai trương | 2.900.000đ | Landing 1 trang |
| Chốt khách | 5.900.000đ | 5 mục + form đặt lịch |
| Trọn hệ thống | 9.900.000đ | + 30 bài fanpage + hỗ trợ 30 ngày |

**Giá này là giá đề xuất để test, mình chưa kiểm chứng được mặt bằng giá ở khu vực của bạn** (trang tham khảo giá bị chặn mạng khi mình tra). Cách kiểm chứng rẻ nhất: gửi 10 tin đầu, nghe phản ứng về giá, chỉnh trước khi gửi đợt lớn.

### Cần bao nhiêu khách?

| Kịch bản | Cơ cấu | Tổng | ≈ USD |
|---|---|---|---|
| A | 3 × Trọn hệ thống | 29,7 tr | 1.121$ |
| B | 2 × Trọn hệ thống + 1 × Chốt khách + 1 × Khai trương | 28,6 tr | 1.079$ |
| C | 5 × Chốt khách | 29,5 tr | 1.113$ |
| D | 10 × Khai trương | 29,0 tr | 1.094$ |

Mốc thực tế nên nhắm: **4–5 khách**, mix gói giữa. Cộng thêm chăm sóc 490k/tháng (tùy chọn) làm đệm.

### Phễu — đây là GIẢ ĐỊNH, không phải số đã đo

100 tin cá nhân hóa → ~15 phản hồi → ~8 xem demo → 3–4 chốt.
Nếu phễu tệ gấp đôi, bạn cần ~200 tin. Vì vậy có điểm kiểm tra ở mục 5: sai thì sửa sớm, đừng chờ hết tháng.

## 4. Quy trình dựng demo 30 phút (phần của Claude)

Với mỗi tiệm bạn chọn, đưa cho Claude: tên tiệm, loại hình, địa chỉ, link fanpage/Maps, 3–5 ảnh công khai, bảng giá nếu có. Claude dựng bản xem trước đúng tên và màu tiệm, bạn gửi link/ảnh chụp màn hình trong tin nhắn. Chỉ dựng cho tiệm đã có dấu hiệu quan tâm hoặc đã trả lời tin đầu — đừng dựng 100 demo cho 100 người chưa hề trả lời.

## 5. Lịch 24 ngày

| Ngày | Việc | Mốc đo |
|---|---|---|
| **T4 7/10 – T5 8/10** | Chốt giá và điều khoản (mục 6). Bật GitHub Pages cho `index.html`. Lấy mã QR nhận tiền. Lập danh sách **60 tiệm** (tiệm tóc, barber, spa, nail, cà phê, gym gần bạn; ưu tiên chưa có web, fanpage có người đăng đều) vào `leads-tracker.csv`. | Có 60 dòng + link trang chạy |
| **T6 9/10 – T2 12/10** | **Đợt 1:** 40 tin cá nhân hóa (kịch bản 1). Mỗi ngày ~10 tin. Trả lời nhanh trong ngày. | ≥ 4 phản hồi |
| **T3 13/10** | **Điểm kiểm tra #1.** Dưới 3 phản hồi / 40 tin → đổi câu mở (nhắn kèm ảnh chụp demo thay vì chữ) hoặc đổi loại hình. Đừng gửi thêm đợt khi chưa sửa. | Quyết định sửa gì |
| **13/10 – 19/10** | **Đợt 2:** thêm 60 tin + follow-up (kịch bản 2). Dựng demo cho ai đã trả lời. Chốt khách đầu, thu cọc 50%, giao. | ≥ 1 khách cọc |
| **T3 20/10** | **Điểm kiểm tra #2.** Chưa có khách nào cọc → nhắn lại mọi người đã xem demo với ưu đãi có thời hạn thật (kịch bản 4), mở thêm 40 tin. | Còn ~11 ngày |
| **20/10 – 26/10** | Chốt các khách còn lại. Giao hàng song song. Thu 50% cuối khi bàn giao. | Tổng cọc ≥ 50% mục tiêu |
| **T4 28/10** | **Hạn cuối nhận cọc mới** (cần 48h giao + thu nốt trước 31/10). | |
| **29/10 – T7 31/10** | Giao nốt, thu tiền còn lại, xin giới thiệu (kịch bản 6). | ≥ 26,5 tr đã nhận |

## 6. Điều khoản đề xuất (bạn sửa theo ý)

- Xem bản dựng thử miễn phí. Chốt gói thì **cọc 50%**, nhận bàn giao rồi trả **50% còn lại**.
- Tên miền/hosting tính riêng theo giá nhà cung cấp, đứng tên khách. Báo giá trước khi chốt.
- Chỉnh sửa: 1 lần miễn phí sau bàn giao (gói Chốt khách), hỗ trợ 30 ngày (gói Trọn hệ thống).
- Ảnh/thông tin dùng là ảnh khách cung cấp hoặc công khai của tiệm. Khách xác nhận trước khi đưa lên mạng.
- Trang bán hàng đang hứa: giao 48 giờ, 30 bài fanpage, hỗ trợ 30 ngày. **Chỉ giữ những gì bạn chắc làm được** — sửa trong `index.html` nếu thay đổi.

## 7. Việc hằng ngày của bạn (~60–90 phút)

1. Gửi 10 tin cá nhân hóa (mỗi tin 3–4 phút: xem fanpage tiệm, chọn 1 chi tiết thật để nhắc).
2. Trả lời mọi phản hồi trong ngày.
3. Follow-up ai đã im 2 ngày.
4. Cập nhật `leads-tracker.csv` 5 phút cuối ngày.

Quy tắc gửi: nhắn từ tài khoản thật của bạn, từng tin viết riêng, không gửi hàng loạt giống hệt. Người ta từ chối thì cảm ơn và dừng. Làm vậy vừa đúng, vừa không bị khóa tài khoản.

## 8. Đường phụ: sửa thử thách 21 ngày để bán được tiền

Không bắt buộc, quyết định của bạn. Nếu muốn thử song song:
- Đổi từ "cọc hoàn 100%" sang **học phí thật**, ví dụ 1.490.000đ, làm đủ 21 ngày thì **hoàn một phần** (ví dụ 30%). Vẫn giữ tinh thần "thắng lại tiền của bạn".
- 18 người × 1,49 tr ≈ 26,8 tr (~1.011$). Nhưng điều này cần **tệp người theo dõi** đã có sẵn, mà mình không thấy số liệu nào về nó trong repo. Chưa có tệp thì đường này không kịp trong 24 ngày.
- Làm sau, đừng làm cùng lúc: chia sức sẽ làm cả hai chậm.

## 9. Mình cần bạn quyết / cung cấp

1. Giá 3 gói có ổn không, có muốn bỏ gói nào.
2. Số Zalo trên trang: đang dùng 0936007937 lấy từ trang thử thách của bạn. Đúng số chưa?
3. Khu vực bạn nhắm (quận/thành phố) và 60 tiệm đầu tiên.
4. Bạn chắc làm được "48 giờ"? Nếu 72 giờ thì mình sửa trang.
5. Cách nhận tiền (QR ngân hàng/Momo) và có cần hóa đơn không.

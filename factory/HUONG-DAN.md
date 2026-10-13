# Xưởng làm web — hướng dẫn cho Linh

Không cần biết lập trình. Bạn chỉ cần hai việc: **đưa thông tin tiệm cho mình**, và **đưa web lên mạng**.

## A. Đưa thông tin một tiệm cho mình

Copy khung dưới, điền, dán vào cuộc trò chuyện với mình. Mục nào chưa có thì để trống, mình tự lo hoặc bỏ qua.

```
Tên tiệm:
Loại hình: (tiệm tóc / nha khoa / trung tâm / quán cà phê / khác)
Khu vực: (quận)
Địa chỉ đầy đủ:
Số điện thoại / Zalo:
Giờ mở cửa:
Link fanpage hoặc Google Maps:
Dịch vụ và giá (nếu thấy ở fanpage):
1 điều khách hay khen ở tiệm này:
Gói muốn báo: (Khởi động / Doanh nghiệp / Tăng trưởng)
```

Mình sẽ:
1. Dựng web, đặt tên cho tiệm đó.
2. Chụp ảnh điện thoại của bản dựng thử.
3. Viết sẵn tin nhắn để bạn gửi.

Có ảnh thật của tiệm thì đưa mình, web nhìn thật hơn nhiều. Khi chưa có ảnh, web vẫn đẹp vì dùng màu và chữ.

## B. Đưa web lên mạng (khi khách đã cọc)

Mình đưa bạn thư mục web của khách đó (có file `index.html` bên trong). Cách đơn giản nhất, mất khoảng 5 phút:

1. Vào **app.netlify.com/drop** (bạn đã từng dùng Netlify cho trang thử thách, đăng nhập bằng tài khoản đó).
2. **Kéo cả thư mục** web vào khung trên trang. Vài giây sau có đường link chạy thật.
3. Gửi link cho khách xem. Muốn gắn tên miền riêng (kiểu tentiem.com) thì làm thêm bước kết nối tên miền, mình hướng dẫn từng bước khi có khách thật.

Lưu ý: mình mô tả Netlify theo hiểu biết của mình, chưa mở giao diện hiện tại để kiểm tra. Nếu nút bấm nằm khác chỗ, bạn chụp màn hình gửi mình, mình chỉ tiếp.

## C. Để thông tin khách điền vào form về email của chủ tiệm

Form đặt lịch trên web chỉ nhận được thông tin khi web nằm trên Netlify. Sau khi đưa web lên, cần bật nhận thông báo:

1. Mở trang quản lý site đó trên Netlify, vào mục **Forms**.
2. Thêm thông báo gửi về email của chủ tiệm (hoặc email của bạn, rồi chuyển lại cho khách).

Theo mình nhớ, gói miễn phí giới hạn số lượt gửi mỗi tháng (khoảng 100). Bạn kiểm tra lại trước khi hứa với khách. Mình **chưa test được form trên Netlify thật**. Lần đầu có khách, bạn tự điền thử một lần xem email có về không rồi hãy bàn giao.

## C2. Ảnh thật làm web đẹp hơn nhiều

Hình minh họa mình vẽ giúp web có hồn khi chưa có ảnh, nhưng **ảnh thật của chính tiệm** mới là thứ thuyết phục nhất: khách thấy phòng khám của họ trên màn hình điện thoại.
- Xin chủ tiệm 5–10 ảnh (mặt tiền, phòng khám/không gian, đội ngũ, công việc thực tế), hoặc tải từ fanpage/Google Maps của họ.
- Gửi ảnh vào cuộc trò chuyện với mình. Mình đặt ảnh chính vào đầu trang, ảnh còn lại thành mục "Không gian thực tế" (đã thử bố cục này, chạy tốt).
- Nếu máy mình không nhận được file ảnh gốc, mình sẽ báo ngay để tìm cách khác. Mình chưa thử việc này với ảnh bạn gửi.
- Chỉ đưa ảnh lên web thật khi chủ tiệm đồng ý. Dùng ảnh công khai của họ trong bản xem thử gửi riêng cho chính họ là bình thường.

## D. Dành cho kỹ thuật (bạn có thể bỏ qua)

- `build.py` đọc `clients/*.json`, xuất `out/<tên>/index.html`. Chạy `python3 build.py`.
- Bản 2 có: hình minh họa riêng cho từng loại hình, thẻ nổi, biểu tượng dịch vụ, quy trình, khối đánh giá Google (cần `maps_url`), chỗ cho ảnh thật (`images.hero`, `images.gallery`), khung bản đồ dự phòng.
- 4 loại hình có sẵn: `salon`, `clinic`, `edu`, `fnb` (bảng màu và tên mục riêng).
- 4 file `mau-*.json` là bản demo minh họa, dùng thông tin giả. Số điện thoại trong mẫu là số Zalo của bạn.
- Tên, địa chỉ, giá khách nhập đều được xử lý an toàn trước khi đưa vào web (đã thử với dữ liệu chèn mã).

# Nguồn và cách cài

Skill `impeccable` (phiên bản 4.5.2).

- Repo: https://github.com/pbakaus/impeccable (giấy phép Apache 2.0, xem `LICENSE`, `NOTICE.md`).
- Bản lấy về: commit `245ad82` (12/10/2026). `SKILL.md` và `reference/` giữ nguyên, không sửa.
- Đã xem trước khi cài (13/10/2026): `SKILL.md`, danh mục, chương trình khởi chạy, các tệp hooks; quét toàn bộ `reference/` tìm lệnh nguy hiểm, gọi mạng, câu bảo bỏ qua luật. Phần chỉ dẫn sạch. **Chưa đọc từng dòng** của ~520 KB `reference/`.

## Cố ý KHÔNG cài
- `scripts/impeccable` gốc: là trình khởi chạy, nếu thiếu thì **tải một tệp chạy được từ GitHub Releases rồi chạy nó** (chỉ kiểm bằng mã băm lấy từ cùng nơi tải). Không ai trong đội kiểm tra được bên trong tệp đó.
- Hooks (`.claude/settings.json` và bản cho công cụ khác): gọi tệp trên **sau mỗi lần sửa file và mỗi lần dừng**, kể cả ở phiên tự động không có người xem.
- `scripts/data/` (chỉ mục phông chữ 1,1 MB cho chương trình trên), `.claude/agents/` của repo nguồn.
- Thay vào đó `scripts/impeccable` ở đây là **stub** thoát với mã 127 và một dòng giải thích, không chạy gì khác.

## Hệ quả
- Dùng được: toàn bộ phần chỉ dẫn (shape, critique, audit, polish, typeset, layout, colorize, harden, clarify, adapt...).
- Không chạy: những lệnh cần chương trình hỗ trợ (`context`, `pin`, `hooks`, `live`, `generate`, bộ dò tự động). Skill tự có nhánh dự phòng: đọc `PRODUCT.md` và `DESIGN.md` trực tiếp.
- Muốn bật đầy đủ là **quyết định của Linh**, làm theo hướng dẫn của repo nguồn, sau khi cân nhắc rủi ro ở trên.
- Cập nhật: lấy lại từ repo nguồn, thay `SKILL.md` và `reference/`, cập nhật commit ở trên.

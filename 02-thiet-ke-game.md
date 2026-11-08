# Thiết kế game

> Phần đánh dấu _(chưa chốt)_ là chủ dự án điền. Claude không tự bịa.

## Mục tiêu

Mod roguelike dungeon cho Minecraft, có bản sắc riêng (màn hình tiêu đề riêng, không chỉ thêm nút vào màn vanilla).

## 8 dungeon

_(chưa chốt: 8 dungeon là gì, khác nhau thế nào)_

## Một lớp dungeon (theo code hiện tại)

- Lưới mặc định 13×13 ô, mỗi ô 16 block = 1 chunk. Phòng vào ở ô giữa (6, 6).
- Phòng: 16×16 (nội thất 14×14), 16×32, 32×32; cao nội thất 16 block. Trọng số 6 : 3 : 1.
- 16–24 phòng ở pha chính; tối thiểu **4 phòng cụt**.
- Phòng cụt sinh ở **pha cuối**: thêm phòng, có thể kèm phòng cầu nối, đánh dấu chỗ để phòng cụt sau không mọc ở đó.
- Vai trò phòng: `START`, `NORMAL`, và 6 phòng đặc biệt:
  - 4 ở phòng cụt: `BOSS`, `TREASURE`, `SHOP`, `LIBRARY`
  - 2 thay phòng thường: `MYSTERY` (tối đa 2), `ELITE` (tối đa 1)
- Cùng seed → cùng dungeon.

## Tiến trình (meta-progression)

- File save riêng cho tiến trình và thành tựu, kiểu Isaac / Slay the Spire, mở khóa nội dung.
- Khó đọc/sửa, gắn với tài khoản Minecraft bản quyền.
- _(chưa chốt: mở khóa những gì, lưu ở đâu)_

## Thứ tự làm

1. Màn hình tiêu đề mới
2. Tạo world void nhanh
3. Sinh dungeon
4. File save tiến trình
5. Nội dung mở khóa

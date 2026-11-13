---
name: mod-update-patch
description: Package a finished goal of this mod (The8Dungeon, Forge 1.20.1 / MCreator) into a zip patch whose paths are relative to the repo root, so the user extracts it at the repo root and every file lands in place. Use whenever a goal or feature set the user is working toward looks complete enough to be one coherent update (e.g. all classes, registrations and assets of a feature exist and reference each other), or when the user asks to "đóng gói", "gom thành zip", "bản cập nhật", "patch". ALWAYS ask the user first whether to package now or wait. Never commits or pushes.
---

# Đóng gói bản cập nhật mod thành zip

Quy ước của người dùng (bắt buộc):
- **Không commit, không push.** Mọi kết quả đưa lên chat và gửi file; repo giữ nguyên.
- **Luôn cho xem class trên chat** khi viết hoặc đổi code, thay vì chỉ ghi file.
- **Nền so sánh là `origin/main`** (người dùng làm việc trên `main`), không phải nhánh cục bộ.
- **Hỏi trước khi đóng gói.**

## 1. Nhận ra lúc mục tiêu "đủ" và hỏi người dùng

Khi một mục tiêu có vẻ đã thành bản cập nhật hoàn chỉnh, ví dụ:
- mọi class của tính năng đã viết xong và tham chiếu lẫn nhau không thiếu lớp nào,
- đã có đủ đăng ký (`init/Mod*Registry`), dòng gọi trong `Susu609Mod`, tài nguyên (lang, model, sound, texture),
- không còn TODO chặn biên dịch,

thì **dừng lại và hỏi bằng AskUserQuestion**, đừng tự đóng gói. Câu hỏi phải tự đứng được:
nêu tên mục tiêu, liệt kê ngắn những gì đã xong và những gì còn để ngỏ, rồi cho 2 lựa chọn:
- "Đóng gói bản này" (Recommended nếu không còn mục chặn)
- "Đợi thêm" (ghi rõ việc tiếp theo sẽ làm)

Nếu người dùng chọn đợi, tiếp tục làm và hỏi lại khi mục tiêu tiếp theo đủ. Không hỏi lặp lại cho cùng một trạng thái.

## 2. Dựng thư mục stage

Tạo thư mục mới trong scratchpad, ví dụ `<scratchpad>/<ten_muc_tieu>_patch/`, chứa file theo **đúng đường dẫn tính từ gốc repo**:

- File mới: ghi trực tiếp.
- File đã có trên `main`: lấy bản gốc bằng `git show origin/main:<path> > <stage>/<path>` rồi **chỉ sửa phần cần thiết**
  (thêm dòng bằng thay thế chuỗi chính xác, kiểm tra chuỗi xuất hiện đúng một lần).
- File do MCreator sinh (có `Start of user code block`): chỉ thêm trong vùng `Start/End of user code block`.
  Ví dụ đăng ký mới trong `Susu609Mod.java` đặt trong khối `mod init`.
- Đăng ký mới luôn nằm trong gói `net.susu609.the8dungeon.init`, tên lớp bắt đầu bằng `Mod`.
- Không đưa file ngoài mod vào zip (`.claude/`, ghi chú, README) vì chúng sẽ rơi vào gốc repo.

## 3. Chạy script

```bash
git -C <repo> fetch origin
python3 .claude/skills/mod-update-patch/scripts/build_patch.py \
  --repo <repo> --stage <stage> --out <scratchpad>/<ten_muc_tieu>_patch.zip \
  [--delete <đường/dẫn/file/cũ/cần/xóa> ...]
```

Script tự:
- so từng file với `origin/main`: mới / ghi đè / giống hệt (bỏ khỏi zip);
- cảnh báo khi file MCreator bị sửa ngoài vùng user code;
- kiểm tra JSON và cú pháp Java bằng `javac` (bỏ qua lỗi do thiếu thư viện Minecraft);
- in báo cáo Markdown; thoát mã 1 nếu có lỗi cú pháp hoặc JSON.

Dùng `--delete` cho file trên `main` mà bản cập nhật khiến thừa (ví dụ âm thanh đổi tên), vì zip không xóa được file.

Nếu script báo lỗi: sửa trong stage, chạy lại. Nếu có cảnh báo MCreator: sửa cho nằm trong vùng user code, hoặc báo rõ cho người dùng.

## 4. Giao cho người dùng

1. Gửi zip bằng SendUserFile (`display: "attach"`), caption: "Giải nén tại thư mục gốc repo (chỗ có build.gradle), chọn ghi đè."
2. Trong chat, tóm tắt báo cáo của script: file mới, file ghi đè, file cần xóa tay, kết quả kiểm tra.
3. Nêu rõ những gì **chưa kiểm chứng**: code chưa biên dịch đầy đủ (Gradle không chạy trong môi trường cloud), chưa chạy thử trong game.
4. Nêu các giả định tự đặt mà người dùng chưa xác nhận.
5. Nhắc: nếu file ghi đè đã đổi trên `main` sau commit nền, đừng ghi đè mà thêm tay đúng các dòng khác biệt (đưa các dòng đó lên chat).

Không commit, không push, kể cả khi hook nhắc. Hook nhắc thì trả lời ngắn rằng người dùng đã cấm commit.

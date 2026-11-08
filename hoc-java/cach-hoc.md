# Cách học với Claude

Claude gợi mở, bạn tự nghĩ. Bạn có thể gọi tên từng kỹ thuật, ví dụ "cho mình bậc 2".

## 1. Gợi ý theo bậc

Bị kẹt thì xin lên một bậc, không nhảy bậc.

| Bậc | Claude đưa |
|---|---|
| 1 | Hướng nghĩ, câu hỏi gợi ý |
| 2 | Tên class / API / khái niệm cần dùng |
| 3 | Mã giả (tiếng Việt) |
| 4 | Một dòng code mẫu kèm giải thích |

## 2. Ghi chú 👀

Claude chỉ chỗ cần đọc, kèm một câu hỏi:
> 👀 `DungeonLayout.java`, `Arrays.fill(row, -1)`: vì sao -1 mà không phải 0?

## 3. Khung để điền

Claude đưa công thức có chỗ trống:
```java
public static final DeferredRegister<___> ITEMS =
        DeferredRegister.create(ForgeRegistries.___, ___);
```

## 4. Dự đoán trước

Trước khi giải thích hoặc build: "Nếu đổi X thì sao?" Bạn đoán → kiểm tra → so sánh.

## 5. Tìm lỗi cố ý

Claude đưa đoạn code ngắn có đúng 1 lỗi. Bạn tìm và sửa.

## 6. Tự giải thích

Bạn viết comment tiếng Việt cho một method. Claude chấm: đúng, thiếu, sai.

## 7. Review từng lỗi một

Claude chỉ lỗi quan trọng nhất trước. Sửa xong mới đến lỗi tiếp.

## 8. Ôn cuối buổi

Claude hỏi 3 câu ngắn và đề xuất dòng thêm vào [nhat-ky-hoc.md](nhat-ky-hoc.md) và [tu-dien.md](tu-dien.md).

## Câu lệnh nhanh

| Bạn nói | Claude làm |
|---|---|
| "bậc 1/2/3/4" | Gợi ý đúng bậc đó |
| "đố mình" | Câu hỏi hoặc bài tìm lỗi |
| "chấm giúp" | Review code của bạn |
| "giải thích dòng N" | Giải thích một dòng |
| "ôn" | 3 câu ôn tập |
| "viết hộ" / "gấp" | Đưa code, vẫn tóm tắt từng đoạn |

---
name: dich-ma-java
description: Translate Java code (mod The8Dungeon, Forge 1.20.1) into Vietnamese pseudo-code line by line, keeping every concrete name unchanged (class, interface, method, field, variable, parameter, package, constant, annotation, string and number literals). Use when the user asks to "dịch mã", "dịch code sang tiếng Việt", "đọc code bằng tiếng Việt", "mã giả", "bậc 3", or pastes/uploads a Java file and wants to understand it. Only explains; never edits, commits or pushes code.
---

# Dịch mã Java sang tiếng Việt

Mục tiêu: người học đọc từng dòng Java như đọc câu tiếng Việt, nhưng vẫn thấy đúng tên trong code
để tra cứu và dịch ngược lại. Đây là "bậc 3: mã giả tiếng Việt" trong `hoc-java/cach-hoc.md`.

## Quy tắc bắt buộc

1. **Giữ nguyên mọi tên cụ thể**, không dịch, không đổi hoa thường:
   tên lớp, interface, enum, record, phương thức, trường, biến, tham số, gói, hằng,
   annotation (`@Override`, `@NotNull`...), kiểu generic (`<T>`, `BlockEntityType<?>`),
   chuỗi (`"fuelTicks"`) và số (`12000`, `0x80000000`).
2. **Chỉ dịch từ khóa, toán tử và cấu trúc** theo bảng bên dưới.
3. **Một dòng Java = một dòng tiếng Việt**, giữ nguyên thứ tự và thụt lề, để đối chiếu được.
   Dấu `{ }` giữ lại; dấu `;` bỏ đi.
4. **Lời gọi phương thức giữ nguyên dạng**: `level.setBlock(pos, state, Block.UPDATE_ALL)`
   thành `gọi level.setBlock(pos, state, Block.UPDATE_ALL)`.
5. **Comment** `//` và `/** */`: giữ nguyên nếu đã là tiếng Việt, dịch nếu là tiếng Anh.
6. **Không sửa code** khi dịch. Nếu thấy lỗi, ghi riêng ở phần "Ghi chú" sau bản dịch, kèm số dòng.
7. Không commit, không push, không ghi đè file của người dùng. Kết quả đưa lên chat.

## Bảng dịch

| Java | Tiếng Việt |
|---|---|
| `package a.b` | `gói a.b` |
| `import a.b.C` | `dùng a.b.C` |
| `import static a.B.X` | `dùng thẳng X từ a.B` |
| `class X` | `lớp X` |
| `interface X` | `giao diện X` |
| `record X(...)` | `bản ghi X(...)` |
| `enum X` | `liệt kê X` |
| `extends Y` | `kế thừa Y` |
| `implements Z` | `thực thi Z` |
| `public` / `protected` / `private` | `công khai` / `bảo vệ` / `riêng` |
| `static` | `dùng chung (static)` |
| `final` | `cố định` |
| `static final` | `hằng` |
| `abstract` | `trừu tượng` |
| `void` | `không trả về` |
| kiểu trả về `T` | `trả về T` |
| constructor `X(...)` | `hàm khởi tạo X(...)` |
| phương thức `m(...)` | `hàm m(...)` |
| `return v` | `trả về v` |
| `new X(...)` | `tạo mới X(...)` |
| `this` / `this.f` | `chính nó` / `f của chính nó` |
| `super(...)` | `gọi khởi tạo cha(...)` |
| `super.m(...)` | `gọi m(...) của cha` |
| `if (c)` / `else if` / `else` | `nếu (c)` / `ngược lại nếu` / `ngược lại` |
| `for (int i = 0; i < n; i++)` | `lặp i từ 0 đến trước n` |
| `for (T x : list)` | `với mỗi x (kiểu T) trong list` |
| `while (c)` | `trong khi (c)` |
| `break` / `continue` | `thoát vòng lặp` / `sang lượt tiếp` |
| `switch (v)` / `case A ->` | `xét v` / `trường hợp A thì` |
| `=` | `gán` |
| `==` / `!=` | `bằng` / `khác` |
| `<` `<=` `>` `>=` | `nhỏ hơn` `không quá` `lớn hơn` `ít nhất` |
| `&&` / `\|\|` / `!` | `và` / `hoặc` / `không` |
| `x++` / `x--` | `tăng x thêm 1` / `giảm x đi 1` |
| `+=` / `-=` | `cộng thêm vào` / `trừ bớt từ` |
| `a / b` (số nguyên) | `a chia b (lấy phần nguyên)` |
| `a % b` | `phần dư của a chia b` |
| `c ? a : b` | `nếu c thì a, không thì b` |
| `x instanceof T t` | `x là kiểu T (gọi là t)` |
| `null` | `rỗng (null)` |
| `true` / `false` | `đúng` / `sai` |
| `(T) x` | `ép x thành kiểu T` |
| `x -> ...` | `hàm nhận x: ...` |
| `X::m` | `tham chiếu hàm X::m` |
| `try` / `catch (E e)` / `finally` | `thử` / `nếu lỗi E (gọi là e)` / `cuối cùng luôn chạy` |
| `throw new E(...)` | `ném lỗi tạo mới E(...)` |
| `throws E` | `có thể ném lỗi E` |
| `@Override` | `@Override (ghi đè hàm của cha)` |

Annotation khác giữ nguyên, có thể thêm chú thích ngắn trong ngoặc ở lần xuất hiện đầu.

## Định dạng trả lời

1. Một khối mã `text` chứa bản dịch, giữ thụt lề như bản gốc.
2. Nếu đoạn ngắn (dưới ~15 dòng), có thể dùng bảng 2 cột "Java | Tiếng Việt" thay cho khối mã.
3. Phần **Ghi chú** (chỉ khi cần): lỗi nhìn thấy, khái niệm mới nên tra trong `hoc-java/tu-dien.md`.
4. Không đưa lời giải hay bản sửa trừ khi người dùng yêu cầu.

## Ví dụ

Java:

```java
public static void tick(Level level, BlockPos pos, BlockState state, ModTorchBlockEntity be) {
    if (level.isClientSide()) return;
    be.fuelTicks--;
    int stage = (be.fuelTicks * 4 + MAX_TICKS - 1) / MAX_TICKS;
    if (stage != state.getValue(FUEL)) {
        level.setBlock(pos, state.setValue(FUEL, stage), Block.UPDATE_ALL);
    }
}
```

Bản dịch:

```text
công khai dùng chung (static) hàm tick(Level level, BlockPos pos, BlockState state, ModTorchBlockEntity be), không trả về {
    nếu (gọi level.isClientSide()) thì trả về
    giảm be.fuelTicks đi 1
    biến int stage gán (be.fuelTicks nhân 4 cộng MAX_TICKS trừ 1) chia MAX_TICKS (lấy phần nguyên)
    nếu (stage khác gọi state.getValue(FUEL)) {
        gọi level.setBlock(pos, gọi state.setValue(FUEL, stage), Block.UPDATE_ALL)
    }
}
```

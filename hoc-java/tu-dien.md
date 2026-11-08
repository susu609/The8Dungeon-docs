# Từ điển Java/Forge

Mỗi thuật ngữ gắn với chỗ có thật trong mod. Thêm dòng khi gặp từ mới. Cột "Hiểu?" bạn tự đánh: ❌ / 🤔 / ✅.

## Java

| Thuật ngữ | Nghĩa ngắn | Trong mod ở đâu | Hiểu? |
|---|---|---|---|
| `class` | Bản thiết kế cho một loại đối tượng | `DungeonLayout` | |
| `final class` | Class không cho kế thừa | `DungeonLayout`, `DungeonCommand` | |
| `private` constructor | Cấm `new` từ bên ngoài | `DungeonCommand()` | |
| `static` | Thuộc về class, không cần tạo object | `DungeonParams.DEFAULT` | |
| `final` (biến) | Gán một lần, không đổi | `RoomPreset.CELL = 16` | |
| `enum` | Tập giá trị cố định, có thể có trường và method | `RoomPreset`, `Role` | |
| `record` | Class chỉ chứa dữ liệu; Java tự viết constructor, getter, `equals` | `DungeonParams`, `Room`, `Door` | |
| compact constructor | Khối kiểm tra đầu vào của record, chạy trước khi gán | `public DungeonParams { ... }` | |
| mảng 2D | Mảng của mảng, truy cập `a[hàng][cột]` | `grid[z][x]` | |
| `List` / `ArrayList` | Danh sách có thứ tự, thêm bớt được | `rooms`, `doors` | |
| `Set` / `HashSet` | Tập không trùng phần tử | `tagged` | |
| generic `<T>` | Ghi rõ kiểu phần tử bên trong | `List<Room>` | |
| lambda `x -> ...` | Hàm ngắn không tên | `ctx -> run(...)` | |
| method reference `A::b` | Viết gọn của lambda gọi sẵn method | `Config::validateItemName` | |
| `throw` / exception | Báo lỗi, dừng luồng chạy bình thường | `IllegalArgumentException` trong `DungeonParams` | |
| `try` / `catch` | Bắt lỗi để xử lý thay vì crash | `DungeonCommand.run` | |
| `extends` | Kế thừa class cha | `ModTitleScreen extends Screen` | |
| `interface` | Danh sách method phải có, không có thân | `TitleScreenInterface` | |
| `.clone()` | Tạo bản sao (mảng) | `presetWeights.clone()` | |

## Forge / Minecraft

| Thuật ngữ | Nghĩa ngắn | Trong mod ở đâu | Hiểu? |
|---|---|---|---|
| `@Mod` | Đánh dấu lớp chính để Forge nạp | `The8DungeonsMod` | |
| `MODID` | Tên định danh mod, là namespace tài nguyên | `"susu609"` | |
| mod event bus | Sự kiện lúc khởi động: đăng ký, setup | `BLOCKS.register(modEventBus)` | |
| Forge event bus | Sự kiện trong game: lệnh, tick, người chơi | `RegisterCommandsEvent` | |
| `@SubscribeEvent` | Method nhận một sự kiện | `onRegisterCommands` | |
| `@EventBusSubscriber` | Tự đăng ký cả class vào bus | `DungeonCommand` | |
| `DeferredRegister` | Đăng ký block/item đúng thời điểm | `The8DungeonsMod.BLOCKS` | |
| `ServerLevel` | World phía server, nơi đặt block | `DungeonBuilder.build` | |
| `BlockPos` | Tọa độ một block (x, y, z) | `origin` | |
| chunk | Ô 16×16 block | `RoomPreset.CELL` | |
| Brigadier | Thư viện tạo lệnh `/...` | `Commands.literal("dungeon")` | |
| `hasPermission(2)` | Chỉ OP mới dùng được lệnh | `DungeonCommand` | |
| client / server | Client vẽ hình, server chạy logic | `client/` chỉ chạy client | |
| world preset | JSON mô tả kiểu tạo world | `void.json` | |

## Dễ nhầm

| Cặp | Khác nhau |
|---|---|
| `==` vs `.equals()` | `==` so sánh cùng một object; `.equals()` so sánh nội dung |
| `static` vs không `static` | Của class vs của từng object |
| mod bus vs Forge bus | Lúc khởi động vs lúc chơi |
| `List` vs `Set` | Có thứ tự, cho trùng vs không trùng |
| `record` vs `class` | Chỉ dữ liệu, bất biến vs tự do |
| `ArrayList` vs mảng `[]` | Đổi kích thước được vs cố định |

## Công thức trong mod

| Công thức | Ý nghĩa | 👀 Ở đâu |
|---|---|---|
| `block = ô × 16` | Đổi ô lưới sang block | `RoomPreset.CELL` |
| `tâm = origin + (ô + số_ô / 2.0) × 16` | Tọa độ giữa phòng | `DungeonCommand.run` |
| `số ô = kích thước / 16` | Phòng chiếm mấy ô | `RoomPreset.cellsX` |
| `cần ≥ 1 + 4 + (6 − 4)` | Số phòng tối thiểu | `DungeonParams` |

👀 Câu hỏi: trong công thức tâm phòng, vì sao chia `2.0` mà không chia `2`?

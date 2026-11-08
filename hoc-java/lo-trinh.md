# Lộ trình học Java qua dự án

Mỗi bài gắn với code thật trong repo. Đánh dấu `[x]` khi tự giải thích lại được.

## 1. Cơ bản
- [ ] Biến, kiểu dữ liệu, toán tử — đọc `WorldRandom`
- [ ] if/else, vòng lặp — vòng `for` kiểm trọng số trong `DungeonParams`
- [ ] Method, tham số, giá trị trả về
- [ ] Mảng, mảng 2D — `grid[z][x]` trong `DungeonLayout`

## 2. Hướng đối tượng
- [ ] Class và object, constructor
- [ ] `static` và `final` — `RoomPreset.CELL`, `DungeonParams.DEFAULT`
- [ ] Kế thừa — `ModTitleScreen extends Screen`
- [ ] Interface — `TitleScreenInterface`
- [ ] `private` constructor, class tiện ích — `DungeonCommand`

## 3. Java hiện đại
- [ ] `enum` có trường và method — `RoomPreset`
- [ ] `record`, compact constructor — `DungeonParams`, `Room`, `Door`
- [ ] List / Set / Map — `rooms`, `doors`, `tagged`
- [ ] Generic — `List<Room>`, `RegistryObject<Item>`
- [ ] Lambda, method reference — `ctx -> run(...)`, `Config::validateItemName`
- [ ] Exception: throw, try/catch — `IllegalArgumentException` trong `DungeonCommand`
- [ ] `null` và `Optional`

## 4. Forge
- [ ] Vòng đời mod, `@Mod`
- [ ] Event bus (mod bus vs Forge bus), `@SubscribeEvent`
- [ ] Registry, `DeferredRegister`
- [ ] Client vs server
- [ ] Lệnh (Brigadier) — `DungeonCommand`
- [ ] Tài nguyên JSON

## 5. Áp dụng
- [ ] Thuật toán sinh dungeon, seed
- [ ] `SavedData` / NBT
- [ ] Bảo vệ file save

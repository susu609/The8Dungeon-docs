# Sinh dungeon

**Trạng thái:** đang làm

**File:** `dungeon/`
- `DungeonParams` — record thông số, kiểm tra đầu vào; `DEFAULT` = lưới 13×13, 16–24 phòng, ≥ 4 phòng cụt.
- `RoomPreset` — enum kích thước phòng.
- `DungeonLayout` — dữ liệu thuần, không import Minecraft. 3 pha: mọc cây phòng → thêm phòng cụt → gán vai trò. Lỗi thì thử lại (tối đa 200 lần).
- `DungeonBuilder` — đặt block vào world.
- `DungeonCommand` — `/dungeon build [seed]`, phòng vào ở chunk (0, 0), y = 0.

**Kiểm tra:** `/dungeon build 123` hai lần → phải giống nhau. Xem số phòng/phòng cụt trong chat.

**Còn lại:** _(chủ dự án điền)_

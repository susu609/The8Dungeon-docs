# Quy ước code

## Không vibe coding

1. Hiểu trước, code sau. Tính năng mới: nêu mục tiêu, file, API Forge, cách kiểm tra → chờ đồng ý.
2. Mỗi lần một việc nhỏ, kiểm tra được trong game.
3. Giải thích mọi thay đổi. Chủ dự án phải giải thích lại được.
4. Không bịa API. Chỉ dùng API đúng **Forge 47 / MC 1.20.1 / official**. Không chép mẫu NeoForge, Fabric, 1.19, 1.21 mà không đối chiếu.
5. Hỏi trước khi thêm dependency, mixin, access transformer, network packet, sửa `build.gradle`/`mods.toml`.
6. Báo cáo thật: đã build hay chưa kiểm chứng.
7. Không commit/push khi chưa được yêu cầu.

## Cấu trúc package

```text
net/susu609/the8dungeons/
├── The8DungeonsMod.java
├── Config.java
├── client/gui/        # màn hình, inspector (CHỈ client)
├── dungeon/           # DungeonLayout (dữ liệu thuần), DungeonBuilder, DungeonCommand
├── world/             # void world, WorldRandom
├── registry/          # khi có block/item thật
└── mixin/
```

## Quy tắc

- ID registry: `snake_case`, tiếng Anh.
- Đăng ký qua `DeferredRegister` + `RegistryObject`.
- Tài nguyên: `assets/susu609/…` (client), `data/susu609/…` (server).
- Không import `net.minecraft.client.*` ngoài `client/`.
- Logic game chạy phía server; kiểm `level.isClientSide()`.
- Tách logic thuần khỏi Minecraft khi được (như `DungeonLayout`) để dễ test.
- Comment tiếng Việt, giải thích *vì sao*. Tên trong code tiếng Anh.

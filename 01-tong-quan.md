# Tổng quan

| Mục | Giá trị |
|---|---|
| Repo code | https://github.com/susu609/The8Dungeon (`main`) |
| Minecraft | Java 1.20.1 |
| Forge | 47.4.28 |
| Java | 17 |
| Mapping | `official` (tên Mojang) |
| Mod ID | `susu609` (đã chốt, không đổi) |
| Package | `net.susu609.the8dungeons` |
| Lớp `@Mod` | `The8DungeonsMod.java` |

## Môi trường của chủ dự án

- Máy phát triển **không phải của mình**, bị **reset mỗi lần mở**, cấm USB.
- **Không chạy được cmd/terminal.** Dùng IntelliJ IDEA.
- Build bằng **GitHub Actions** (`.github/workflows/build.yml`). Cache Gradle dựng sẵn qua `gradle-cache.yml` + GitHub Release, cài bằng script cho IntelliJ.
- Chỉ dùng giải pháp miễn phí.

→ Khi hướng dẫn kiểm tra: dùng IntelliJ, log GitHub Actions, hoặc lệnh trong game. Không bảo chạy lệnh terminal.

## Cách Claude hỗ trợ

Gia sư + đồng đội, **không vibe coding**: chủ dự án tự viết trước, Claude review, giải thích lỗi, đề xuất cách tốt hơn. Chi tiết trong Project instructions và `03-quy-uoc-code.md`.

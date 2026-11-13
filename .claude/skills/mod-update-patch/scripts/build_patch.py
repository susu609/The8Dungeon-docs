#!/usr/bin/env python3
"""Đóng gói một bản cập nhật mod thành zip "giải nén tại gốc repo là đúng chỗ".

Cách dùng:
  build_patch.py --repo REPO --stage STAGE_DIR --out PATCH.zip [--base origin/main]
                 [--delete path/in/repo ...] [--no-fetch]

STAGE_DIR chứa các file theo đúng đường dẫn tính từ gốc repo (ví dụ STAGE_DIR/src/main/java/...).
Script:
  - so từng file với bản trên --base: NEW (mới), MODIFIED (khác), SAME (giống hệt, bỏ khỏi zip);
  - cảnh báo khi file MCreator (có "Start of user code block") bị sửa ngoài vùng user code;
  - kiểm tra JSON, kiểm tra cú pháp Java bằng javac (bỏ qua lỗi do thiếu thư viện Minecraft);
  - tạo zip chỉ gồm NEW + MODIFIED, và in báo cáo Markdown ra stdout.
Không bao giờ commit hay push.
"""
import argparse, difflib, json, os, re, shutil, subprocess, sys, tempfile, zipfile

LIB_ERRORS = re.compile(
    r"package .* does not exist|cannot find symbol|cannot access|static import only|"
    r"does not override or implement a method from a supertype|"
    r"incompatible types|cannot be applied to|no suitable (method|constructor)|"
    r"is not abstract and does not override|cannot infer type|bad operand|"
    r"method does not override|unreported exception|not a functional interface|"
    r"cannot be dereferenced|has private access|is not public")


def git(repo, *args, binary=False, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} lỗi: {r.stderr.decode(errors='replace')}")
    return r.stdout if binary else r.stdout.decode(errors="replace")


def base_bytes(repo, base, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{base}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def outside_user_code(old: str, new: str):
    """Trả về các dòng bị thay đổi nằm ngoài vùng 'Start/End of user code block'."""
    def inside_flags(lines):
        flags, inside = [], False
        for ln in lines:
            if "Start of user code block" in ln:
                inside = True; flags.append(False); continue
            if "End of user code block" in ln:
                inside = False; flags.append(False); continue
            flags.append(inside)
        return flags
    a, b = old.splitlines(), new.splitlines()
    fa, fb = inside_flags(a), inside_flags(b)
    bad = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        # dòng bị xóa phải nằm trong vùng user code của bản cũ, dòng thêm phải nằm trong vùng của bản mới
        bad += [a[i] for i in range(i1, i2) if not fa[i]]
        bad += [b[j] for j in range(j1, j2) if not fb[j]]
    return bad


def javac_check(java_files):
    if not java_files or shutil.which("javac") is None:
        return None
    out = tempfile.mkdtemp()
    r = subprocess.run(["javac", "-proc:none", "-Xmaxerrs", "5000", "-d", out, *java_files],
                       capture_output=True, text=True)
    errs = [l for l in (r.stdout + r.stderr).splitlines() if "error:" in l and not LIB_ERRORS.search(l)]
    shutil.rmtree(out, ignore_errors=True)
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--delete", nargs="*", default=[])
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()

    if not a.no_fetch:
        subprocess.run(["git", "-C", a.repo, "fetch", "--quiet", "origin"], capture_output=True)
    base_commit = git(a.repo, "rev-parse", "--short", a.base).strip()

    files = sorted(os.path.relpath(os.path.join(dp, f), a.stage).replace(os.sep, "/")
                   for dp, _, fs in os.walk(a.stage) for f in fs)
    new, modified, same, warnings, json_bad = [], [], [], [], []
    for rel in files:
        data = open(os.path.join(a.stage, rel), "rb").read()
        old = base_bytes(a.repo, a.base, rel)
        if old is None:
            new.append(rel)
        elif old == data:
            same.append(rel)
            continue
        else:
            modified.append(rel)
            o, n = old.decode(errors="replace"), data.decode(errors="replace")
            if "Start of user code block" in o:
                bad = outside_user_code(o, n)
                if bad:
                    warnings.append((rel, bad[:5]))
        if rel.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except Exception as e:  # noqa: BLE001
                json_bad.append(f"{rel}: {e}")

    missing_deletes = [p for p in a.delete if base_bytes(a.repo, a.base, p) is None]
    java = [os.path.join(a.stage, p) for p in new + modified if p.endswith(".java")]
    syntax = javac_check(java)

    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in new + modified:
            z.write(os.path.join(a.stage, rel), rel)

    p = print
    p(f"## Bản cập nhật so với `{a.base}` ({base_commit})\n")
    p(f"Zip: `{a.out}` · {len(new)} file mới · {len(modified)} file ghi đè · {len(same)} file giống hệt (bỏ qua)\n")
    p("Giải nén tại **thư mục gốc repo** (chỗ có `build.gradle`), chọn ghi đè.\n")
    if new:
        p("### File mới"); [p(f"- `{f}`") for f in new]; p()
    if modified:
        p("### File ghi đè"); [p(f"- `{f}`") for f in modified]; p()
    if a.delete:
        p("### Cần xóa bằng tay (zip không xóa được file)")
        for d in a.delete:
            p(f"- `{d}`" + (" (không có trên base, bỏ qua)" if d in missing_deletes else ""))
        p()
    p("### Kiểm tra")
    if syntax is None:
        p("- Cú pháp Java: không kiểm tra (không có javac hoặc không có file Java).")
    elif syntax:
        p("- Cú pháp Java: **có lỗi**"); [p(f"  - {e}") for e in syntax]
    else:
        p("- Cú pháp Java: không có lỗi cú pháp (chưa biên dịch đầy đủ vì thiếu thư viện Minecraft).")
    p("- JSON: " + ("**lỗi**: " + "; ".join(json_bad) if json_bad else "hợp lệ."))
    if warnings:
        p("- **Cảnh báo MCreator**: các file sau bị sửa ngoài vùng user code, MCreator có thể ghi đè khi xuất lại:")
        for rel, lines in warnings:
            p(f"  - `{rel}`: " + " | ".join(l.strip()[:80] for l in lines))
    else:
        p("- MCreator: không có thay đổi ngoài vùng user code.")
    text_mod = [f for f in modified if not f.lower().endswith((".ogg", ".png", ".jar", ".wav", ".nbt"))]
    if text_mod:
        p(f"\nNếu các file sau đã thay đổi sau `{base_commit}`, đừng ghi đè mà thêm tay phần khác biệt: "
          + ", ".join(f"`{f}`" for f in text_mod))
    sys.exit(1 if (syntax or json_bad) else 0)


if __name__ == "__main__":
    main()

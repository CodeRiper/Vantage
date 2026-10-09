#!/usr/bin/env python3
"""
Syncs newly built distribution binaries into releases-v1.2.7
and generates verified SHA256 checksums.
"""

import os
import shutil
import hashlib

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_win = os.path.join(root_dir, "dist-windows")
    dist_linux = os.path.join(root_dir, "dist-linux")
    dist_android = os.path.join(root_dir, "dist-android")
    rel_dir = os.path.join(root_dir, "releases-v1.2.7")

    win_dir = os.path.join(rel_dir, "Windows")
    lin_dir = os.path.join(rel_dir, "Linux")
    and_dir = os.path.join(rel_dir, "Android")
    all_dir = os.path.join(rel_dir, "all-files-to-upload")

    for d in [win_dir, lin_dir, and_dir, all_dir]:
        os.makedirs(d, exist_ok=True)

    print("=" * 60)
    print("  SYNCING FRESH BUILDS TO RELEASES-V1.2.7")
    print("=" * 60)

    # 1. Sync Windows
    print("\n[1/4] Syncing Windows packages...")
    win_files = [
        ("Vantage-Setup-v1.2.7.exe", "Vantage-Setup-v1.2.7.exe"),
        ("Vantage-Portable.exe", "Vantage-Portable-v1.2.7.exe"),
        ("Vantage-Windows-x64.zip", "Vantage-Windows-v1.2.7-x64.zip")
    ]
    for src_name, dst_name in win_files:
        src = os.path.join(dist_win, src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(win_dir, dst_name))
            shutil.copy2(src, os.path.join(all_dir, dst_name))
            size_mb = os.path.getsize(src) / (1024 * 1024)
            print(f"  [OK] Synced {dst_name} ({size_mb:.2f} MB)")

    # 2. Sync Linux
    print("\n[2/4] Syncing Linux packages...")
    lin_files = [
        ("vantage_1.2.7_amd64.deb", "vantage_1.2.7_amd64.deb"),
        ("Vantage-Linux-x64.tar.gz", "Vantage-Linux-v1.2.7-x64.tar.gz"),
        ("Vantage-Linux-x64.zip", "Vantage-Linux-v1.2.7-x64.zip")
    ]
    for src_name, dst_name in lin_files:
        src = os.path.join(dist_linux, src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(lin_dir, dst_name))
            shutil.copy2(src, os.path.join(all_dir, dst_name))
            size_mb = os.path.getsize(src) / (1024 * 1024)
            print(f"  [OK] Synced {dst_name} ({size_mb:.2f} MB)")

    # 3. Sync Android
    print("\n[3/4] Syncing Android packages...")
    and_files = [
        ("Vantage-v1.2.7.apk", "Vantage-v1.2.7.apk"),
        ("Vantage-v1.2.7.apk.idsig", "Vantage-v1.2.7.apk.idsig")
    ]
    for src_name, dst_name in and_files:
        src = os.path.join(dist_android, src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(and_dir, dst_name))
            shutil.copy2(src, os.path.join(all_dir, dst_name))
            size_mb = os.path.getsize(src) / (1024 * 1024)
            print(f"  [OK] Synced {dst_name} ({size_mb:.2f} MB)")

    # 4. Generate Checksums
    print("\n[4/4] Generating verified SHA-256 Checksums...")
    lines = []
    items_to_check = [
        ("Windows/Vantage-Portable-v1.2.7.exe", os.path.join(win_dir, "Vantage-Portable-v1.2.7.exe")),
        ("Windows/Vantage-Setup-v1.2.7.exe", os.path.join(win_dir, "Vantage-Setup-v1.2.7.exe")),
        ("Windows/Vantage-Windows-v1.2.7-x64.zip", os.path.join(win_dir, "Vantage-Windows-v1.2.7-x64.zip")),
        ("Linux/Vantage-Linux-v1.2.7-x64.tar.gz", os.path.join(lin_dir, "Vantage-Linux-v1.2.7-x64.tar.gz")),
        ("Linux/Vantage-Linux-v1.2.7-x64.zip", os.path.join(lin_dir, "Vantage-Linux-v1.2.7-x64.zip")),
        ("Linux/vantage_1.2.7_amd64.deb", os.path.join(lin_dir, "vantage_1.2.7_amd64.deb")),
        ("Android/Vantage-v1.2.7.apk", os.path.join(and_dir, "Vantage-v1.2.7.apk")),
        ("Android/Vantage-v1.2.7.apk.idsig", os.path.join(and_dir, "Vantage-v1.2.7.apk.idsig"))
    ]

    for rel_path, abs_path in items_to_check:
        if os.path.exists(abs_path):
            ck = sha256_file(abs_path)
            size_mb = os.path.getsize(abs_path) / (1024 * 1024)
            line = f"{ck}  {rel_path} ({size_mb:.2f} MB)"
            lines.append(line)
            print(f"  {line}")

    sums_file = os.path.join(rel_dir, "SHA256SUMS.txt")
    with open(sums_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    all_sums_file = os.path.join(all_dir, "SHA256SUMS.txt")
    with open(all_sums_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n" + "=" * 60)
    print("  ALL BINARIES SYNCED & CHECKSUMS GENERATED!")
    print("=" * 60)

if __name__ == "__main__":
    main()

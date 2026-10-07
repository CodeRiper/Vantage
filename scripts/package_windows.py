#!/usr/bin/env python3
"""
Packages all Windows distributions for Vantage v1.2.7:
- Setup Installer (.exe): Vantage-Setup-v1.2.7.exe
- Portable Executable (.exe): Vantage-Portable.exe
- Zip archive (.zip): Vantage-Windows-x64.zip
"""

import os
import sys
import subprocess
import shutil
import zipfile
import time

def package_windows():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_win = os.path.join(root_dir, "dist-windows")
    portable_build = os.path.join(root_dir, "portable-build")
    nsis_exe = r"C:\Program Files (x86)\NSIS\makensis.exe"

    os.makedirs(dist_win, exist_ok=True)

    print("=" * 60)
    print("  PACKAGING VANTAGE WINDOWS RELEASES (v1.2.7)")
    print("=" * 60)

    # 1. Compile NSIS Setup Installer
    if os.path.exists(nsis_exe):
        setup_nsi = os.path.join(portable_build, "VantageSetup.nsi")
        print(f"\n[1/3] Compiling Setup Installer: {setup_nsi}...")
        res = subprocess.run([nsis_exe, "/V2", setup_nsi], cwd=portable_build)
        if res.returncode != 0:
            print("[ERROR] Failed to compile VantageSetup.nsi")
            sys.exit(1)
        setup_src = os.path.join(root_dir, "Vantage-Setup-v1.2.7.exe")
        setup_dest = os.path.join(dist_win, "Vantage-Setup-v1.2.7.exe")
        if os.path.exists(setup_src):
            shutil.copy2(setup_src, setup_dest)
            print(f"  -> Built and synced {setup_dest} ({os.path.getsize(setup_dest)/(1024*1024):.1f} MB)")

        # 2. Compile NSIS Portable Launcher
        portable_nsi = os.path.join(portable_build, "VantagePortable.nsi")
        print(f"\n[2/3] Compiling Portable Launcher: {portable_nsi}...")
        res = subprocess.run([nsis_exe, "/V2", portable_nsi], cwd=portable_build)
        if res.returncode != 0:
            print("[ERROR] Failed to compile VantagePortable.nsi")
            sys.exit(1)
        portable_src = os.path.join(root_dir, "Vantage-Portable.exe")
        portable_dest = os.path.join(dist_win, "Vantage-Portable.exe")
        if os.path.exists(portable_src):
            shutil.copy2(portable_src, portable_dest)
            print(f"  -> Built and synced {portable_dest} ({os.path.getsize(portable_dest)/(1024*1024):.1f} MB)")
    else:
        print(f"[WARN] NSIS executable not found at {nsis_exe}. Skipping installer compilation.")

    # 3. Build Windows x64 zip package
    zip_out = os.path.join(dist_win, "Vantage-Windows-x64.zip")
    print(f"\n[3/3] Building Windows Zip Archive: {zip_out}...")

    # Files to include in the portable zip distribution
    include_files = [
        "LICENSE", "LICENSES.chromium.html", "README.txt", "Vantage.exe",
        "chrome_100_percent.pak", "chrome_200_percent.pak", "d3dcompiler_47.dll",
        "dxcompiler.dll", "dxil.dll", "ffmpeg.dll", "icudtl.dat", "resources.pak",
        "snapshot_blob.bin", "v8_context_snapshot.bin", "version",
        "vk_swiftshader.dll", "vk_swiftshader_icd.json", "vulkan-1.dll"
    ]

    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root binary and config files
        for fname in include_files:
            fpath = os.path.join(root_dir, fname)
            if os.path.exists(fpath):
                zf.write(fpath, arcname=f"Vantage-win32-x64/{fname}")

        # Add locales (en-US.pak)
        loc_dir = os.path.join(root_dir, "locales")
        if os.path.exists(loc_dir):
            for loc in os.listdir(loc_dir):
                if loc.startswith("en"):
                    zf.write(os.path.join(loc_dir, loc), arcname=f"Vantage-win32-x64/locales/{loc}")

        # Add resources/app
        app_dir = os.path.join(root_dir, "resources", "app")
        for f in os.listdir(app_dir):
            fpath = os.path.join(app_dir, f)
            if os.path.isfile(fpath) and f.endswith(('.html', '.js', '.css', '.png', '.ico', '.json')):
                zf.write(fpath, arcname=f"Vantage-win32-x64/resources/app/{f}")

    print(f"  -> Built {zip_out} ({os.path.getsize(zip_out)/(1024*1024):.1f} MB)")
    print("\n" + "=" * 60)
    print("  ALL WINDOWS PACKAGES CREATED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    package_windows()

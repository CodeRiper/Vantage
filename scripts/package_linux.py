#!/usr/bin/env python3
"""
Packages all Linux distributions for Vantage v1.2.8:
- Debian Package (.deb): vantage_1.2.8_amd64.deb
- Tarball (.tar.gz): Vantage-Linux-x64.tar.gz
- Zip archive (.zip): Vantage-Linux-x64.zip
"""

import os
import sys
import shutil
import tarfile
import zipfile
import time

# Import build_deb from build_deb.py
from build_deb import build_deb

def package_all():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_linux = os.path.join(root_dir, "dist-linux")
    src_dir = os.path.join(dist_linux, "Vantage-linux-x64")
    
    print("=" * 60)
    print("  PACKAGING VANTAGE LINUX RELEASES (v1.2.8)")
    print("=" * 60)
    
    # Ensure all web assets are synced
    app_src = os.path.join(root_dir, "resources", "app")
    app_dest = os.path.join(src_dir, "resources", "app")
    for f in os.listdir(app_src):
        src_file = os.path.join(app_src, f)
        if os.path.isfile(src_file) and f.endswith(('.html', '.js', '.css', '.png', '.ico', '.json')):
            shutil.copy2(src_file, os.path.join(app_dest, f))
    print(f"Synced web assets to {app_dest}")
    
    # 1. Build .deb package
    deb_out = os.path.join(dist_linux, "vantage_1.2.8_amd64.deb")
    build_deb(src_dir, deb_out, version="1.2.8")
    
    # 2. Build .tar.gz archive
    tar_out = os.path.join(dist_linux, "Vantage-Linux-x64.tar.gz")
    print(f"\nBuilding Tarball: {tar_out}...")
    with tarfile.open(tar_out, "w:gz") as tar:
        for item in os.listdir(src_dir):
            item_path = os.path.join(src_dir, item)
            tar.add(item_path, arcname=f"Vantage-linux-x64/{item}")
    print(f"Built {tar_out} ({os.path.getsize(tar_out)/(1024*1024):.1f} MB)")
    
    # 3. Build .zip archive
    zip_out = os.path.join(dist_linux, "Vantage-Linux-x64.zip")
    print(f"\nBuilding Zip archive: {zip_out}...")
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir)
                zf.write(full_path, arcname=f"Vantage-linux-x64/{rel_path}")
    print(f"Built {zip_out} ({os.path.getsize(zip_out)/(1024*1024):.1f} MB)")
    
    print("\n" + "=" * 60)
    print("  ALL LINUX PACKAGES CREATED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    package_all()

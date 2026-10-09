#!/usr/bin/env python3
import os
import tarfile
import io
import time

def create_ar_entry(name, data, mode=0o644, mtime=None):
    if mtime is None:
        mtime = int(time.time())
    header = (
        f'{name:<16}'
        f'{mtime:<12}'
        f'0     '
        f'0     '
        f'{oct(mode)[2:]:<8}'
        f'{len(data):<10}'
        '`\n'
    ).encode('latin1')
    padded_data = data if len(data) % 2 == 0 else data + b'\n'
    return header + padded_data

def build_deb(app_dir, output_deb, version="1.2.8"):
    print(f"Building Debian package {output_deb} from {app_dir}...")
    
    # 1. Calculate installed size in KB
    total_bytes = 0
    for root, dirs, files in os.walk(app_dir):
        for f in files:
            total_bytes += os.path.getsize(os.path.join(root, f))
    installed_size_kb = (total_bytes // 1024) + 1024

    # 2. Build control.tar.gz
    control_content = f"""Package: vantage
Version: {version}
Section: utils
Priority: optional
Architecture: amd64
Depends: libgtk-3-0, libnotify4, libnss3, libxss1, libasound2
Installed-Size: {installed_size_kb}
Maintainer: Akash
Homepage: https://vantage.app
Description: Observation, Investigation & Planning Trainer
 Vantage is an observation, reasoning, and investigation board trainer
 featuring visual mind mapping, sticky note workspaces, and recurring plan automations.
""".replace('\r\n', '\n').strip() + '\n'

    postinst_content = """#!/bin/sh
set -e
if [ "$1" = "configure" ]; then
    chmod 4755 /opt/vantage/chrome-sandbox 2>/dev/null || chmod +x /opt/vantage/chrome-sandbox 2>/dev/null || true
    chmod +x /opt/vantage/vantage 2>/dev/null || true
    chmod +x /usr/bin/vantage 2>/dev/null || true
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    fi
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
    fi
fi
exit 0
""".replace('\r\n', '\n')

    postrm_content = """#!/bin/sh
set -e
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database /usr/share/applications 2>/dev/null || true
    fi
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
    fi
fi
exit 0
""".replace('\r\n', '\n')

    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode='w:gz') as tar:
        # control file
        c_bytes = control_content.encode('utf-8')
        ti = tarfile.TarInfo(name='./control')
        ti.size = len(c_bytes)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(c_bytes))

        # postinst
        p_bytes = postinst_content.encode('utf-8')
        ti = tarfile.TarInfo(name='./postinst')
        ti.size = len(p_bytes)
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(p_bytes))

        # postrm
        r_bytes = postrm_content.encode('utf-8')
        ti = tarfile.TarInfo(name='./postrm')
        ti.size = len(r_bytes)
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(r_bytes))

    control_tar_gz = control_buf.getvalue()

    # 3. Build data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode='w:gz') as tar:
        # /opt/vantage files
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                if file in ('install.sh', 'uninstall.sh'):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, app_dir).replace('\\', '/')
                arcname = f"./opt/vantage/{rel_path}"
                
                with open(full_path, 'rb') as f_in:
                    f_data = f_in.read()
                
                ti = tarfile.TarInfo(name=arcname)
                ti.size = len(f_data)
                ti.mtime = int(time.time())
                ti.uname = 'root'
                ti.gname = 'root'
                
                # Executable permissions
                if file in ('vantage', 'chrome-sandbox', 'chrome_crashpad_handler', 'run-vantage.sh') or file.endswith('.so') or '.so.' in file:
                    ti.mode = 0o755
                else:
                    ti.mode = 0o644
                tar.addfile(ti, io.BytesIO(f_data))

        # /usr/bin/vantage wrapper
        usr_bin_wrapper = b"""#!/bin/sh
exec /opt/vantage/vantage "$@"
"""
        ti = tarfile.TarInfo(name='./usr/bin/vantage')
        ti.size = len(usr_bin_wrapper)
        ti.mode = 0o755
        ti.mtime = int(time.time())
        ti.uname = 'root'
        ti.gname = 'root'
        tar.addfile(ti, io.BytesIO(usr_bin_wrapper))

        # /usr/share/applications/vantage.desktop
        desktop_content = b"""[Desktop Entry]
Name=Vantage
Comment=Observation, Investigation & Planning Trainer
Exec=/usr/bin/vantage %U
Icon=vantage
Terminal=false
Type=Application
Categories=Utility;Education;Office;Development;
StartupWMClass=Vantage
Keywords=vantage;mindmap;notes;investigation;planning;
"""
        ti = tarfile.TarInfo(name='./usr/share/applications/vantage.desktop')
        ti.size = len(desktop_content)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        ti.uname = 'root'
        ti.gname = 'root'
        tar.addfile(ti, io.BytesIO(desktop_content))

        # /usr/share/icons/hicolor/512x512/apps/vantage.png
        icon_path = os.path.join(app_dir, 'resources', 'app', 'icon.png')
        if os.path.exists(icon_path):
            with open(icon_path, 'rb') as f_icon:
                icon_bytes = f_icon.read()
            ti = tarfile.TarInfo(name='./usr/share/icons/hicolor/512x512/apps/vantage.png')
            ti.size = len(icon_bytes)
            ti.mode = 0o644
            ti.mtime = int(time.time())
            ti.uname = 'root'
            ti.gname = 'root'
            tar.addfile(ti, io.BytesIO(icon_bytes))

    data_tar_gz = data_buf.getvalue()

    # 4. Assemble ar archive (.deb)
    debian_binary = b"2.0\n"
    
    with open(output_deb, 'wb') as f_deb:
        f_deb.write(b"!<arch>\n")
        f_deb.write(create_ar_entry("debian-binary", debian_binary))
        f_deb.write(create_ar_entry("control.tar.gz", control_tar_gz))
        f_deb.write(create_ar_entry("data.tar.gz", data_tar_gz))

    size_mb = os.path.getsize(output_deb) / (1024 * 1024)
    print(f"Successfully built {output_deb} ({size_mb:.1f} MB)!")

if __name__ == '__main__':
    src = os.path.join("dist-linux", "Vantage-linux-x64")
    out = os.path.join("dist-linux", "vantage_1.2.8_amd64.deb")
    build_deb(src, out, version="1.2.8")

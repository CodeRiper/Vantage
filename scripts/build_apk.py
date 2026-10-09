#!/usr/bin/env python3
"""
Vantage Android APK Build Pipeline
Compiles, dexes, packages, aligns, and signs Vantage into an ultra-fast,
low-memory native Android APK optimized for 1GB RAM devices.
"""

import os
import sys
import subprocess
import shutil
import zipfile
import time

def main():
    start_time = time.time()
    print("=" * 60)
    print("  VANTAGE ANDROID BUILD PIPELINE")
    print("  Optimized for 1GB RAM & Low-End Devices (API 21-35)")
    print("=" * 60)

    # 1. Base Paths
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    android_dir = os.path.join(root_dir, "android")
    build_dir = os.path.join(android_dir, "build")
    gen_dir = os.path.join(build_dir, "gen")
    obj_dir = os.path.join(build_dir, "obj")
    dex_dir = os.path.join(build_dir, "dex")
    dist_dir = os.path.join(root_dir, "dist-android")
    res_dir = os.path.join(android_dir, "res")
    assets_dir = os.path.join(android_dir, "assets")
    manifest_file = os.path.join(android_dir, "AndroidManifest.xml")

    # 2. Tool Paths
    sdk_dir = os.environ.get("ANDROID_HOME") or r"C:\Users\Akash.J\AppData\Local\Android\Sdk"
    build_tools_dir = os.path.join(sdk_dir, "build-tools", "36.0.0")
    android_jar = os.path.join(sdk_dir, "platforms", "android-35", "android.jar")

    jdk_dir = r"C:\Program Files\Android\Android Studio\jbr"
    javac_bin = os.path.join(jdk_dir, "bin", "javac.exe")
    keytool_bin = os.path.join(jdk_dir, "bin", "keytool.exe")

    aapt2_bin = os.path.join(build_tools_dir, "aapt2.exe")
    d8_bin = os.path.join(build_tools_dir, "d8.bat")
    zipalign_bin = os.path.join(build_tools_dir, "zipalign.exe")
    apksigner_bin = os.path.join(build_tools_dir, "apksigner.bat")

    # Verify tool availability
    tools = [
        ("AAPT2", aapt2_bin),
        ("D8", d8_bin),
        ("ZIPALIGN", zipalign_bin),
        ("APKSIGNER", apksigner_bin),
        ("JAVAC", javac_bin),
        ("KEYTOOL", keytool_bin),
        ("ANDROID JAR", android_jar)
    ]
    for name, path in tools:
        if not os.path.exists(path):
            print(f"[ERROR] Required tool '{name}' not found at: {path}")
            sys.exit(1)

    print("[1/8] Cleaning and creating build directories...")
    for d in [gen_dir, obj_dir, dex_dir, dist_dir]:
        os.makedirs(d, exist_ok=True)

    # 3. Synchronize Web Assets
    print("[2/8] Syncing latest HTML/JS/CSS web assets...")
    www_dir = os.path.join(assets_dir, "www")
    os.makedirs(www_dir, exist_ok=True)
    for f in os.listdir(os.path.join(root_dir, "resources", "app")):
        src_file = os.path.join(root_dir, "resources", "app", f)
        if os.path.isfile(src_file) and f.endswith(('.html', '.js', '.css', '.png', '.ico', '.json')):
            shutil.copy2(src_file, os.path.join(www_dir, f))

    # 4. Compile Resources with AAPT2
    print("[3/8] Compiling Android resources with AAPT2...")
    compiled_res_zip = os.path.join(build_dir, "compiled_res.zip")
    cmd_compile = [aapt2_bin, "compile", "--dir", res_dir, "-o", compiled_res_zip]
    res = subprocess.run(cmd_compile, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] aapt2 compile failed:")
        print(res.stderr)
        sys.exit(1)

    # 5. Link Resources & Generate R.java
    print("[4/8] Linking APK package and generating R.java...")
    base_apk = os.path.join(build_dir, "base.apk")
    cmd_link = [
        aapt2_bin, "link",
        "-I", android_jar,
        compiled_res_zip,
        "--manifest", manifest_file,
        "-o", base_apk,
        "--java", gen_dir,
        "-A", assets_dir
    ]
    res = subprocess.run(cmd_link, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] aapt2 link failed:")
        print(res.stderr)
        sys.exit(1)

    # 6. Compile Java Source Code
    print("[5/8] Compiling Java classes with javac (Target: Java 8/21)...")
    r_java = os.path.join(gen_dir, "com", "vantage", "app", "R.java")
    main_java = os.path.join(android_dir, "src", "com", "vantage", "app", "MainActivity.java")
    cmd_javac = [
        javac_bin,
        "-cp", android_jar,
        "-d", obj_dir,
        "-source", "1.8",
        "-target", "1.8",
        r_java,
        main_java
    ]
    res = subprocess.run(cmd_javac, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] javac failed:")
        print(res.stderr)
        sys.exit(1)

    # 7. Convert bytecode to Dalvik Executable (classes.dex) with D8
    print("[6/8] Converting class files to Dalvik bytecode (classes.dex) with D8...")
    class_files = []
    for root, _, files in os.walk(obj_dir):
        for f in files:
            if f.endswith(".class"):
                class_files.append(os.path.join(root, f))

    cmd_d8 = [d8_bin, "--min-api", "21", "--output", dex_dir] + class_files
    res = subprocess.run(cmd_d8, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] d8 failed:")
        print(res.stderr)
        sys.exit(1)

    # 8. Add classes.dex to base.apk
    print("[7/8] Packaging classes.dex into base.apk...")
    classes_dex = os.path.join(dex_dir, "classes.dex")
    with zipfile.ZipFile(base_apk, "a", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(classes_dex, arcname="classes.dex")

    # 9. Zipalign APK
    print("[8/8] Aligning and signing final APK...")
    unaligned_apk = os.path.join(build_dir, "Vantage-unaligned.apk")
    shutil.copy2(base_apk, unaligned_apk)

    final_apk = os.path.join(dist_dir, "Vantage-v1.2.8.apk")
    if os.path.exists(final_apk):
        os.remove(final_apk)

    cmd_zipalign = [zipalign_bin, "-p", "-f", "4", unaligned_apk, final_apk]
    res = subprocess.run(cmd_zipalign, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] zipalign failed:")
        print(res.stderr)
        sys.exit(1)

    # 10. Generate Keystore if needed and Sign
    keystore_path = os.path.join(android_dir, "vantage-release.keystore")
    if not os.path.exists(keystore_path):
        print("  Generating release keystore...")
        cmd_keytool = [
            keytool_bin, "-genkeypair", "-v",
            "-keystore", keystore_path,
            "-storepass", "vantage123",
            "-alias", "vantage",
            "-keypass", "vantage123",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-dname", "CN=Vantage, OU=Mobile, O=VantageApp, L=Global, ST=Earth, C=US"
        ]
        res = subprocess.run(cmd_keytool, capture_output=True, text=True)
        if res.returncode != 0:
            print("[ERROR] keytool failed:")
            print(res.stderr)
            sys.exit(1)

    cmd_sign = [
        apksigner_bin, "sign",
        "--ks", keystore_path,
        "--ks-pass", "pass:vantage123",
        "--ks-key-alias", "vantage",
        "--key-pass", "pass:vantage123",
        final_apk
    ]
    res = subprocess.run(cmd_sign, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] apksigner failed:")
        print(res.stderr)
        sys.exit(1)

    # 11. Verify Signature
    cmd_verify = [apksigner_bin, "verify", "--verbose", final_apk]
    res = subprocess.run(cmd_verify, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] apksigner verify failed:")
        print(res.stderr)
        sys.exit(1)

    apk_size = os.path.getsize(final_apk)
    apk_size_mb = apk_size / (1024 * 1024)
    elapsed = time.time() - start_time

    print("=" * 60)
    print("  BUILD SUCCESSFUL!")
    print(f"  Output APK: {final_apk}")
    print(f"  File Size:  {apk_size_mb:.2f} MB ({apk_size:,} bytes)")
    print(f"  Build Time: {elapsed:.2f} seconds")
    print("=" * 60)
    print("  Verification Output:")
    for line in res.stdout.strip().splitlines()[:5]:
        print(f"    {line}")
    print("=" * 60)

if __name__ == "__main__":
    main()

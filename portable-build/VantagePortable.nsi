; ============================================================================
; Vantage Portable — Single-File Self-Extracting Launcher
; ============================================================================
; Packs the entire Electron app into ONE .exe.
; First run  → extracts to %LOCALAPPDATA%\VantageApp, shows progress.
; Later runs → detects existing extraction, launches instantly.
; ============================================================================

!include "MUI2.nsh"
!include "FileFunc.nsh"

; --------------- basic metadata ---------------
Name        "Vantage"
OutFile     "..\Vantage-Portable.exe"
Caption     "Vantage"
BrandingText "Vantage 1.2.8"

; Use best compression — makes a big difference on 300 MB
SetCompressor /SOLID lzma
SetCompressorDictSize 64

; We don't need an install directory chosen by the user.
; Silently extract to LOCALAPPDATA.
InstallDir "$LOCALAPPDATA\VantageApp"

; Request user-level privileges only (no admin needed)
RequestExecutionLevel user

; No pages shown — runs silently except for progress
SilentInstall normal
AutoCloseWindow true

; Icon
!define MUI_ICON "..\resources\app\icon.ico"
Icon "..\resources\app\icon.ico"

; --------------- version info embedded in the exe ---------------
VIProductVersion "1.2.8.0"
VIAddVersionKey "ProductName"     "Vantage"
VIAddVersionKey "ProductVersion"  "1.2.8"
VIAddVersionKey "FileDescription" "Vantage — Observation, Investigation & Planning"
VIAddVersionKey "FileVersion"     "1.2.8.0"
VIAddVersionKey "CompanyName"     "Akash"
VIAddVersionKey "LegalCopyright"  "© 2026 Akash"

; --------------- the one-page UI: just a progress bar ---------------
!define MUI_PAGE_HEADER_TEXT "Preparing Vantage..."
!define MUI_PAGE_HEADER_SUBTEXT "This only happens once. Please wait..."
!define MUI_INSTFILESPAGE_FINISHHEADER_TEXT "Ready!"
!define MUI_INSTFILESPAGE_FINISHHEADER_SUBTEXT "Launching Vantage now..."
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; --------------- marker file to detect existing extraction ---------------
!define MARKER "$INSTDIR\.vantage-version"
!define APP_VERSION "1.2.8"

; ============================================================================
; .onInit — check if already extracted; if so, skip straight to launch
; ============================================================================
Function .onInit
  ; Check if the marker file exists AND matches our version
  IfFileExists "${MARKER}" 0 need_extract

  ; Read the version from the marker
  FileOpen $0 "${MARKER}" r
  FileRead $0 $1
  FileClose $0

  ; Compare versions
  StrCmp $1 "${APP_VERSION}" already_extracted need_extract

already_extracted:
  ; Already extracted and correct version — just launch and quit
  Exec '"$INSTDIR\Vantage.exe"'
  Abort   ; Abort = exit the installer immediately (no extraction)

need_extract:
  ; Fall through to the extraction section
FunctionEnd

; ============================================================================
; Section — extract all app files
; ============================================================================
Section "Extract"
  ; Check if core engine already exists in $INSTDIR — if so, skip 280MB engine extract!
  IfFileExists "$INSTDIR\Vantage.exe" skip_engine_extract 0

  SetOutPath "$INSTDIR"

  ; ---- root files ----
  File "..\Vantage.exe"
  File "..\LICENSE"
  File "..\LICENSES.chromium.html"
  File "..\chrome_100_percent.pak"
  File "..\chrome_200_percent.pak"
  File "..\d3dcompiler_47.dll"
  File "..\dxcompiler.dll"
  File "..\dxil.dll"
  File "..\ffmpeg.dll"
  File "..\icudtl.dat"
  File "..\resources.pak"
  File "..\snapshot_blob.bin"
  File "..\v8_context_snapshot.bin"
  File "..\version"
  File "..\vk_swiftshader.dll"
  File "..\vk_swiftshader_icd.json"
  File "..\vulkan-1.dll"

  ; ---- locales ----
  SetOutPath "$INSTDIR\locales"
  File "..\locales\en-US.pak"

skip_engine_extract:
  ; ---- resources\app (always updated to latest code) ----
  SetOutPath "$INSTDIR\resources\app"
  File "..\resources\app\icon.ico"
  File "..\resources\app\icon.png"
  File "..\resources\app\index.html"
  File "..\resources\app\main.js"
  File "..\resources\app\package.json"
  File "..\resources\app\preload.js"

  ; ---- write version marker ----
  SetOutPath "$INSTDIR"
  FileOpen $0 "${MARKER}" w
  FileWrite $0 "${APP_VERSION}"
  FileClose $0

  ; ---- launch the app ----
  Exec '"$INSTDIR\Vantage.exe"'
SectionEnd

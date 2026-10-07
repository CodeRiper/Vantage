; ============================================================================
; Vantage — Windows Setup Installer (NSIS)
; ============================================================================
!include "MUI2.nsh"
!include "FileFunc.nsh"

; --------------- Basic Metadata ---------------
Name "Vantage"
OutFile "..\Vantage-Setup-v1.2.7.exe"
Caption "Vantage Setup"
BrandingText "Vantage 1.2.7"

; Solid LZMA compression for compact installer size
SetCompressor /SOLID lzma
SetCompressorDictSize 64

; Per-user install to %LOCALAPPDATA%\Programs\Vantage (standard modern pattern)
InstallDir "$LOCALAPPDATA\Programs\Vantage"
InstallDirRegKey HKCU "Software\Vantage" "InstallDir"

RequestExecutionLevel user

; --------------- Version Information ---------------
VIProductVersion "1.2.7.0"
VIAddVersionKey "ProductName"     "Vantage"
VIAddVersionKey "ProductVersion"  "1.2.7"
VIAddVersionKey "FileDescription" "Vantage — Observation, Investigation & Planning Trainer"
VIAddVersionKey "FileVersion"     "1.2.7.0"
VIAddVersionKey "CompanyName"     "Akash"
VIAddVersionKey "LegalCopyright"  "© 2026 Akash"

; --------------- UI & Icons ---------------
!define MUI_ICON "..\resources\app\icon.ico"
!define MUI_UNICON "..\resources\app\icon.ico"
!define MUI_ABORTWARNING

; --------------- Installer Pages ---------------
!define MUI_WELCOMEPAGE_TITLE "Welcome to Vantage Setup"
!define MUI_WELCOMEPAGE_TEXT "Vantage is an observation, reasoning, and investigation board trainer featuring visual mind mapping, sticky note workspaces, and recurring plan automations.$\r$\n$\r$\nClick Next to continue."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_RUN "$INSTDIR\Vantage.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Vantage now"
!insertmacro MUI_PAGE_FINISH

; --------------- Uninstaller Pages ---------------
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ============================================================================
; Installation Section
; ============================================================================
Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on

  ; Root application & Chromium engine files
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

  ; Locales
  SetOutPath "$INSTDIR\locales"
  File "..\locales\en-US.pak"

  ; Application source & assets
  SetOutPath "$INSTDIR\resources\app"
  File "..\resources\app\icon.ico"
  File "..\resources\app\icon.png"
  File "..\resources\app\index.html"
  File "..\resources\app\main.js"
  File "..\resources\app\package.json"
  File "..\resources\app\preload.js"

  ; Create Uninstaller
  SetOutPath "$INSTDIR"
  WriteUninstaller "$INSTDIR\uninstall.exe"

  ; Create Shortcuts
  CreateDirectory "$SMPROGRAMS\Vantage"
  CreateShortcut "$SMPROGRAMS\Vantage\Vantage.lnk" "$INSTDIR\Vantage.exe" "" "$INSTDIR\resources\app\icon.ico" 0
  CreateShortcut "$SMPROGRAMS\Vantage\Uninstall Vantage.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortcut "$DESKTOP\Vantage.lnk" "$INSTDIR\Vantage.exe" "" "$INSTDIR\resources\app\icon.ico" 0

  ; Register in Windows Registry
  WriteRegStr HKCU "Software\Vantage" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "DisplayName" "Vantage"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "DisplayVersion" "1.2.7"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "Publisher" "Akash"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "DisplayIcon" "$INSTDIR\resources\app\icon.ico,0"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "NoRepair" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage" "EstimatedSize" 280000
SectionEnd

; ============================================================================
; Uninstallation Section
; ============================================================================
Section "Uninstall"
  ; Delete Shortcuts
  Delete "$DESKTOP\Vantage.lnk"
  Delete "$SMPROGRAMS\Vantage\Vantage.lnk"
  Delete "$SMPROGRAMS\Vantage\Uninstall Vantage.lnk"
  RMDir "$SMPROGRAMS\Vantage"

  ; Delete Files
  Delete "$INSTDIR\Vantage.exe"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\LICENSES.chromium.html"
  Delete "$INSTDIR\chrome_100_percent.pak"
  Delete "$INSTDIR\chrome_200_percent.pak"
  Delete "$INSTDIR\d3dcompiler_47.dll"
  Delete "$INSTDIR\dxcompiler.dll"
  Delete "$INSTDIR\dxil.dll"
  Delete "$INSTDIR\ffmpeg.dll"
  Delete "$INSTDIR\icudtl.dat"
  Delete "$INSTDIR\resources.pak"
  Delete "$INSTDIR\snapshot_blob.bin"
  Delete "$INSTDIR\v8_context_snapshot.bin"
  Delete "$INSTDIR\version"
  Delete "$INSTDIR\vk_swiftshader.dll"
  Delete "$INSTDIR\vk_swiftshader_icd.json"
  Delete "$INSTDIR\vulkan-1.dll"

  ; Delete subdirectories
  RMDir /r "$INSTDIR\locales"
  RMDir /r "$INSTDIR\resources\app"
  RMDir "$INSTDIR\resources"
  RMDir "$INSTDIR"

  ; Delete Registry Keys
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vantage"
  DeleteRegKey HKCU "Software\Vantage"
SectionEnd

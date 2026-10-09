# Vantage (v1.2.8)

[![Version](https://img.shields.io/badge/version-1.2.8-blue.svg)](https://github.com/CodeRiper/Vantage/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-green.svg)](https://github.com/CodeRiper/Vantage/releases)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

> **Tactical Observation, Investigation Board, Influence/Negotiation Simulator, and Automated Plan Management Workstation.**

Vantage is a high-performance desktop and mobile productivity and tactical analysis application. It unifies visual investigation boards, flash observation drills, negotiation simulations, and an automated rule-based planner into a clean, modern interface.

---

## 🌟 Modules & Features

### 🧠 1. Mindmap & Investigation Board
- **Interactive Canvas**: Pan, zoom, and arrange evidence nodes freely.
- **Node Connections**: Link entities, suspects, clues, and topics with dynamic visual relationship lines.
- **Node Customization**: Multiple node types, tags, color-coding, and custom metadata.
- **Export & Import**: Instant mindmap snapshots and workspace state backups.

### 📝 2. Tactical Notes & Rich Clipboard Intel
- **Smart Image Paste**: Paste images directly from external sources, clipboards, and screenshots.
- **Auto-Optimization & Layout**: Automatically formats and neatly structures pasted text and high-res imagery without bloat.
- **Quick Intel Dossier**: Real-time note capture with instant search and state persistence.

### 🎯 3. Flash Observation Trainer
- **Situational Drills**: Quick-fire observation exercises designed to test memory, entity recall, and situational awareness.
- **Configurable Speed & Difficulty**: Tailor the reveal duration and question complexity to hone cognitive sharpness.
- **Scoring & Performance Metrics**: Real-time evaluation of accuracy and reaction latency.

### 🤝 4. Influence & Negotiation Trainer
- **Scenario Simulations**: High-stakes conversation trees with branching outcomes.
- **Tactic Evaluation**: Test negotiation strategies (anchoring, mirroring, emotional labeling, reciprocal concessions) and monitor trust/resistance meters.
- **Feedback & After-Action Review**: Review choices and tactical missteps to improve persuasion dynamics.

### 📋 5. Plan & Kanban Engine
- **Workflow Columns**: Organize initiatives across `Backlog`, `Active`, `Review`, and `Done`.
- **One-Click State Transitions**: Direct complete/reopen toggle (`✓ Complete` / `↺ Reopen`) on cards and table views.
- **Shift Controls**: Quick-move buttons (`‹` / `›`) to transition tickets across stages without dragging.
- **Subtask Checklists**: Detailed subtasks with live progress bars and priority tags (`urgent`, `high`, `medium`, `low`).

### ⚙️ 6. Automated Recurring Rules Engine
- **Time-Based Scheduling**: Automatically spawn plan items daily, weekly (select days), or monthly.
- **Completion-Triggered Workflows**: Configure tasks to recur `X` days after ticket completion (`mode: after`).
- **Predictable Triggering**: Rules default to the current active day and date to fire reliably.

### 🧹 7. Auto-Clean & Storage Compression
- **Smart Retention**: Cleans expired tasks based on completion timestamps (`completedAt`), preserving active and recently completed tickets.
- **Storage Compression**: Prunes excess activity history and fired automation logs to keep the local storage footprint ultra-fast and lightweight.

---

## 📥 Downloads & Releases

Production binaries are available on the [GitHub Releases](https://github.com/CodeRiper/Vantage/releases) page:

| Platform | Format | File Name | Size |
|---|---|---|---|
| **Windows** | Setup Installer | `Vantage-Setup-v1.2.8.exe` | ~98 MB |
| **Windows** | Portable Executable | `Vantage-Portable-v1.2.8.exe` | ~98 MB |
| **Windows** | Portable Zip | `Vantage-Windows-v1.2.8-x64.zip` | ~141 MB |
| **Linux** | Debian / Ubuntu | `vantage_1.2.8_amd64.deb` | ~116 MB |
| **Linux** | Portable Tarball | `Vantage-Linux-v1.2.8-x64.tar.gz` | ~116 MB |
| **Linux** | Portable Zip | `Vantage-Linux-v1.2.8-x64.zip` | ~119 MB |
| **Android** | Native APK (API 21-35) | `Vantage-v1.2.8.apk` | ~201 KB |

---

## 🛠️ Repository Architecture

```text
├── resources/app/          # Core web application & Electron entrypoint
│   ├── index.html          # Main application UI, canvas, planner & logic
│   ├── main.js             # Electron main process
│   ├── preload.js          # Electron preload bridge
│   ├── package.json        # Application manifest
│   ├── icon.ico            # Windows application icon
│   └── icon.png            # App logo
├── android/                # Native Android wrapper (Java & AAPT2/D8 pipeline)
│   ├── AndroidManifest.xml # Android permissions and manifest
│   ├── src/                # Java source code (MainActivity)
│   ├── res/                # App resources & launcher icons
│   └── assets/             # Synced web application bundle
├── portable-build/         # NSIS installer & portable launcher build scripts
│   ├── VantageSetup.nsi    # NSIS Windows installer script
│   └── VantagePortable.nsi # NSIS portable launcher script
├── scripts/                # Packaging, test, and build automation pipelines
│   ├── package_windows.py  # Builds Windows Setup, Portable, and Zip releases
│   ├── package_linux.py    # Builds Linux .deb, .tar.gz, and .zip releases
│   ├── build_apk.py        # Compiles, aligns, and signs Android APK
│   └── build_deb.py        # Debian packaging script
├── releases-v1.2.8/        # Prepared release packages organized for manual upload
├── .gitignore              # Git ignore rules for binaries and caches
└── README.md
```

---

## 💻 Running from Source

### Prerequisites
- [Node.js](https://nodejs.org/) (v16+)
- [Python 3](https://www.python.org/) (for packaging pipelines)

### Run with Electron
```bash
# Navigate to the app directory
cd resources/app

# Launch the desktop application
npx electron .
```

---

## 📦 Building Releases from Source

Pre-configured build scripts are located in `scripts/`:

```bash
# Build Windows packages (Setup installer, Portable .exe, and Zip)
python scripts/package_windows.py

# Build Linux packages (.deb package, .tar.gz, and .zip)
python scripts/package_linux.py

# Build Android APK (requires Android SDK and JDK)
python scripts/build_apk.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

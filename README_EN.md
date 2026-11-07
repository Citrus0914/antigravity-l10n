# Antigravity Chinese Localization Patch (antigravity-l10n)

<div align="center">

**🌏 English | [简体中文](README.md)**

A community-enhanced Chinese localization patch for Google Antigravity Desktop, based on upstream open-source work.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/Citrus0914/antigravity-l10n)](https://github.com/Citrus0914/antigravity-l10n/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/Citrus0914/antigravity-l10n/releases)

</div>

---

## 📖 Overview & Attribution

> [!NOTE]
> **Upstream Attribution & Credits**:
> This project is continuously maintained and enhanced based on the open-source repository [Antigravity-zh-CN](https://github.com/MIMICTE/Antigravity-zh-CN) by **[MIMICTE](https://github.com/MIMICTE)**.
> Because the official Antigravity client updates frequently, the upstream patch had incomplete translations across newer features, sidebars, and advanced configurations. This repository provides a **comprehensive supplemental localization**, fixes false translation bugs in code diff views, and includes a full CI/CD release workflow for long-term maintenance.

---

## ✨ Enhancements & Supplemental Features

Compared to the initial upstream release, this repository adds:

1. **Full Localization for Automations Module**:
   - Sidebar navigation, scheduled task dashboard, status filters.
   - New automation modals (frequency, recurrence, daily/weekly hour selectors, Cron expression input, prompt editor).
   - Card action menus (Permissions, Run Now, Restart, View Logs, Delete confirmation modal).
   - Automation detail views, prompt editors, historical event timelines, and task logs.
2. **Deep Settings & Permissions Localization**:
   - Permissions configuration headings, local/remote conversation permission scopes.
   - Branch context menus (`Work in a New Worktree`).
   - Execution environment selection modals (local vs. cloud descriptions and options).
3. **Code Diff & Syntax Protection**:
   - Isolates code blocks, Monaco/CodeMirror editors, and Git Diff View containers from translation, ensuring keywords (`open`, `update`, `search`, etc.) remain intact.
4. **Maintenance & Zero-Restart Hot Update Tools**:
   - `tools/extract_frontend.py` to extract new UI strings from running instances.
   - `tools/hot_update.py` for immediate dictionary hot-reloading with `Ctrl + R`.
5. **Cross-Platform CI/CD Automation**:
   - GitHub Actions workflow that builds Windows x64 and macOS (Apple Silicon / Intel) standalone packages and publishes GitHub Releases on tag push.

---

## 📦 Download & Usage

### Option 1: Standalone Version (Windows / macOS) ⭐ Recommended

No Python environment required:

- **Download:** [Download latest release from GitHub Releases](https://github.com/Citrus0914/antigravity-l10n/releases/latest)
  - Windows: `Antigravity-zh-CN-v*-windows-x64.zip`
  - macOS (Apple Silicon M1/M2/M3/M4 Series): `Antigravity-zh-CN-v*-macos-arm64-binaries.zip`
  - macOS (Intel Series): `Antigravity-zh-CN-v*-macos-x86_64-binaries.zip`

---

#### 🪟 Windows Instructions
1. Download and extract the zip archive;
2. Double-click `Antigravity-Patcher.exe` to apply the patch;
3. To restore the official English version, double-click `Restore.exe`.

---

#### 🍎 macOS Instructions
1. Download the archive for your Mac architecture (Apple Silicon vs. Intel) and extract it;
2. Open **Terminal**, navigate to the extracted directory, grant execution permissions and run:
   ```bash
   chmod +x Antigravity-Patcher-macOS-*
   ./Antigravity-Patcher-macOS-*
   ```
   *(To restore the official English version, run `./Restore-macOS-*`)*

> 💡 **macOS Common Troubleshooting**:
> - **`Permission denied`**: Since `/Applications` is a protected system directory, run with `sudo` if write permissions are restricted:
>   ```bash
>   sudo ./Antigravity-Patcher-macOS-*
>   ```
> - **"Developer cannot be verified" or "App is damaged"**: This is macOS Gatekeeper blocking unsigned open-source binaries. Run the following command in Terminal to clear quarantine attributes:
>   ```bash
>   # Clear quarantine for the patcher binary
>   xattr -cr ./Antigravity-Patcher-macOS-*
>   # If Antigravity fails to launch after patching
>   xattr -cr /Applications/Antigravity.app
>   ```
>   Alternatively, go to "System Settings -> Privacy & Security", scroll down and click "Open Anyway".

---

### Option 2: Run from Source ⭐ Recommended for Developers

Requires local Python 3.8+ environment:

```bash
git clone https://github.com/Citrus0914/antigravity-l10n.git
cd antigravity-l10n

# Run patcher (Windows uses python, macOS uses python3)
python Antigravity-Patcher.py   # Windows
python3 Antigravity-Patcher.py  # macOS

# Restore official English version
python Restore.py   # Windows
python3 Restore.py  # macOS
```

---

## 💡 Technical Implementation

This project operates through Electron mechanisms:
1. **Unpacked Injection**: Unpacks the official `app.asar` and injects lightweight dictionary mapping via `preload.js`;
2. **Dynamic DOM Monitoring**: Uses `MutationObserver` to intercept DOM node mutations and translate text while strictly whitelisting code containers (`.font-mono`, `.token`, diff views, etc.);
3. **Zero Dependencies**: Pure Python standard library implementation with no external runtime requirements.

---

## ⚠️ Notes & Known Limitations

- **Thought Process in English**: Due to streaming model output architecture, agent thinking logs remain in English; all final responses and UI strings are localized.
- **Official Software Updates**: Official updates may overwrite patched files. Simply re-run the patcher script/executable after an update to re-apply the patch.

---

## 🙏 Credits & Attribution

- **Upstream Repository**: [MIMICTE / Antigravity-zh-CN](https://github.com/MIMICTE/Antigravity-zh-CN)
- **Original Author**: [MIMICTE](https://github.com/MIMICTE)
- **License**: Inherits the [MIT License](LICENSE) from the upstream repository, preserving all original copyright notices. Special thanks to MIMICTE for the foundational localization architecture!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). For educational and personal use only.

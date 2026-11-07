# Antigravity 简体中文汉化补丁 (antigravity-l10n)

<div align="center">

**🌏 [English](README_EN.md) | 简体中文**

基于开源项目深度扩充与持续维护的 Google Antigravity 桌面端中文汉化补丁

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/Citrus0914/antigravity-l10n)](https://github.com/Citrus0914/antigravity-l10n/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/Citrus0914/antigravity-l10n/releases)

</div>

---

## 📖 项目简介与溯源

> [!NOTE]
> **开源溯源与原作者致谢**：
> 本项目基于原作者 **[MIMICTE](https://github.com/MIMICTE)** 开源的 [Antigravity-zh-CN](https://github.com/MIMICTE/Antigravity-zh-CN) 项目二次开发。
> 由于 Antigravity 官方客户端更新频繁，原版汉化存在较多新功能、侧边栏及深层设置未汉化完全的情况。本项目在继承原版底层架构的同时，对这些未完全汉化的界面进行了**全量补充与深度校对**，修复了代码高亮区域误汉化等问题，并搭建了自动化跨平台构建与发布流水线，以便长期跟进官方版本。

---

## ✨ 本项目的主要补充与增强

相比于初始版本，本项目重点补充和优化了以下内容：

1. **Automations（自动化）模块全量汉化**：
   - 补全侧边栏“自动化（Automations）”入口、计划任务列表及状态筛选；
   - 补全新建自动化模态弹窗（执行频率、周期、时间时刻下拉框、Cron 表达式、提示词区域）；
   - 补全自动化卡片操作菜单（权限管理、立即运行、重启、查看日志、删除确认弹窗等）；
   - 补全自动化详情页面、调度提示词编辑器、历史事件面板与任务日志。
2. **常规设置与权限管理深度汉化**：
   - 补全设置中心 Permissions 标题及本地/远程对话权限说明；
   - 补全分支切换菜单（`Work in a New Worktree` 等保留专有名词的合规汉化）；
   - 补全运行环境选择弹窗（本地/云端环境说明与选项）。
3. **代码容器防误汉化隔离保护**：
   - 修复了 Git 差异对比面板（Diff View）穿透汉化的缺陷，防止代码中的关键词（如 `open`、`update`、`search` 等）被错误翻译为中文，确保代码语法高亮与等宽容器保持原貌。
4. **长效维护与免重启热调试工具链**：
   - 内置 `tools/extract_frontend.py`：新版本更新时自动从本地运行实例中抓取最新前端 Bundle 并快速检索未汉化词条；
   - 内置 `tools/hot_update.py`：编辑词典后秒级热同步至 `preload.js`，按 `Ctrl+R` 免重启即时验证。
5. **跨平台 CI/CD 自动化构建**：
   - 引入 GitHub Actions 多架构矩阵，推送 Tag 即可全自动构建 Windows x64、macOS (Apple Silicon / Intel) 免安装离线包并发布 GitHub Release。

---

## 📦 下载与使用

### 方式一：独立免安装版 (Windows / macOS) ⭐ 推荐普通用户

无需安装 Python 环境，开箱即用：

- **下载地址**：[前往 Releases 下载最新版本](https://github.com/Citrus0914/antigravity-l10n/releases/latest)
  - Windows 用户下载：`Antigravity-zh-CN-v*-windows-x64.zip`
  - macOS (Apple Silicon M系列) 下载：`Antigravity-zh-CN-v*-macos-arm64-binaries.zip`
  - macOS (Intel系列) 下载：`Antigravity-zh-CN-v*-macos-x86_64-binaries.zip`

**【Windows 使用方法】**
1. 下载并解压压缩包；
2. 双击运行 `Antigravity-Patcher.exe` 即可自动完成汉化并重启软件；
3. 如需还原官方原版英文，双击运行 `Restore.exe` 即可。

**【macOS 使用方法】**
1. 下载对应架构的压缩包并解压；
2. 打开终端（Terminal），进入解压目录，赋予执行权限后运行：
   ```bash
   chmod +x Antigravity-Patcher-macOS-*
   ./Antigravity-Patcher-macOS-*
   ```
> 🍎 **macOS 提示**：若系统提示“无法验证开发者”，前往「系统设置 -> 隐私与安全性」向下滑动点击「仍要打开」，或在终端执行 `xattr -cr Antigravity-Patcher-macOS-*` 即可解除限制。

---

### 方式二：源码运行 ⭐ 推荐开发者与二开

**克隆仓库：**
```bash
git clone https://github.com/Citrus0914/antigravity-l10n.git
cd antigravity-l10n
python Antigravity-Patcher.py
```

如需还原官方原版英文，运行：
```bash
python Restore.py
```

---

## 💡 技术实现原理

本项目基于 Electron 桌面端机制运作：
1. **解包注入**：解包官方 `app.asar`，在前端启动生命周期中通过 `preload.js` 注入轻量汉化匹配逻辑；
2. **DOM 动态拦截**：通过 `MutationObserver` 监听前端 DOM 节点变动，精准匹配并替换界面文本，同时对代码容器（如 `.font-mono`、`.token`、diff 视图等）进行严格的白名单隔离；
3. **零外部依赖**：ASAR 解析与重构逻辑采用纯原生 Python 标准库实现，不依赖 Node.js 或第三方网络请求。

---

## ⚠️ 已知限制与注意事项

- **AI 思考过程（Thought）保持英文**：受限于大模型即时流式输出机制，智能体后台生成的思考链日志无法且不建议进行实时中文干预；所有最终生成的回复和软件前端界面均已汉化。
- **软件自动更新**：官方版本升级可能会覆盖汉化。若升级后汉化失效，重新运行一次补丁程序即可自动适配重新注入。

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q: 杀毒软件报毒怎么办？</b></summary>

A: 免安装版本使用开源工具 [PyInstaller](https://pyinstaller.org/) 打包，内嵌了精简 Python 运行时，部分安全软件可能误报。您可以：
- 将程序添加到杀毒软件信任区；
- 或者直接使用 Python 源码版（代码完全透明）。
</details>

<details>
<summary><b>Q: 执行汉化后软件无法启动怎么办？</b></summary>

A: 请尝试以下步骤：
1. 运行 `Restore.exe` 或 `python Restore.py` 还原到官方原版；
2. 确保原版 Antigravity 能正常启动；
3. 以管理员身份重新运行汉化补丁。
</details>

<details>
<summary><b>Q: 如何参与贡献或反馈遗漏的英文？</b></summary>

A: 欢迎在 [GitHub Issues](https://github.com/Citrus0914/antigravity-l10n/issues) 中提交反馈，或通过 `tools/extract_frontend.py` 提取词条后提交 Pull Request。
</details>

---

## 🙏 致谢与原作者 (Credits & Attribution)

- **上游原项目**：[MIMICTE / Antigravity-zh-CN](https://github.com/MIMICTE/Antigravity-zh-CN)
- **初始作者**：[MIMICTE](https://github.com/MIMICTE)
- **开源协议**：本项目继承原项目之 [MIT License](LICENSE)，保留原作者著作权声明与原始授权条款。特别感谢原作者为社区提供的初始汉化原型与基础架构！

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。仅供个人学习、研究与交流使用。

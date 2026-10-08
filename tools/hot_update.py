# coding: utf-8
"""
Antigravity 免重启热更新调试脚本
在修改 Antigravity-Patcher.py 的词典或正则后直接运行本脚本，
无需关闭 Antigravity 软件，在软件中按 Ctrl + R 即可立即生效！
"""
import os
import sys
import importlib.util

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
patcher_file = os.path.join(parent_dir, "Antigravity-Patcher.py")

if not os.path.exists(patcher_file):
    print(f"[错误] 未找到补丁文件: {patcher_file}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("patcher", patcher_file)
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)

if sys.platform == "win32":
    preload_path = os.path.join(os.getenv('LOCALAPPDATA', ''), 'Programs', 'antigravity', 'resources', 'app', 'dist', 'preload.js')
elif sys.platform == "darwin":
    preload_path = "/Applications/Antigravity.app/Contents/Resources/app/dist/preload.js"
else:
    print("[错误] 不支持的操作系统。")
    sys.exit(1)

if not os.path.exists(preload_path):
    print(f"[错误] 未检测到解包注入目录，请先运行一次 一键汉化.bat 进行初始化解包。")
    sys.exit(1)

print("[执行] 正在热同步最新的词典代码至 preload.js...")
patcher.append_once(preload_path, patcher.DOM_TRANSLATOR_INJECTION, "Antigravity Chinese Localization Engine", "Web UI Injection")
print("==================================================================")
print("  [成功] 词典热注入完毕！")
print("  请回到 Antigravity 软件界面，按键盘快捷键 [Ctrl + R] 刷新即可生效！")
print("==================================================================")

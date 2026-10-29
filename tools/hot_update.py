# coding: utf-8
"""
Antigravity 免重启热更新调试脚本
在修改 Antigravity-Patcher.py 的词典或正则后直接运行本脚本，
1. 自动热更新 preload.js 词典代码；
2. 自动通过 DevTools 协议即时重载运行中的窗口；
3. 同时已支持在窗口中直接按 Ctrl + R 或 F5 快捷刷新。
"""
import os
import sys
import importlib.util

def trigger_auto_reload():
    """尝试通过 DevTools CDP 协议自动刷新运行中的 Antigravity 窗口"""
    appdata = os.getenv('APPDATA', '')
    port_file = os.path.join(appdata, 'Antigravity', 'DevToolsActivePort')
    if not os.path.exists(port_file):
        return False
    try:
        import socket
        import base64
        import urllib.request
        import json
        with open(port_file, 'r', encoding='utf-8') as f:
            port = f.readline().strip()
        req = urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=2)
        targets = json.loads(req.read().decode('utf-8'))
        reloaded = 0
        for t in targets:
            if t.get('type') == 'page' and '127.0.0.1' in t.get('url', ''):
                ws_url = t.get('webSocketDebuggerUrl', '')
                path = ws_url.replace(f'ws://127.0.0.1:{port}', '')
                s = socket.socket()
                s.settimeout(2.0)
                s.connect(('127.0.0.1', int(port)))
                sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
                handshake = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: 127.0.0.1:{port}\r\n"
                    f"Upgrade: websocket\r\n"
                    f"Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Key: {sec_key}\r\n"
                    f"Sec-WebSocket-Version: 13\r\n\r\n"
                )
                s.sendall(handshake.encode('utf-8'))
                resp = s.recv(1024)
                if b"101" in resp:
                    payload = json.dumps({'id': 1, 'method': 'Page.reload', 'params': {'ignoreCache': True}}).encode('utf-8')
                    mask = os.urandom(4)
                    header = bytearray([0x81, 0x80 | len(payload)]) + mask
                    masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
                    s.sendall(header + masked)
                    s.recv(1024)
                    reloaded += 1
                s.close()
        return reloaded > 0
    except Exception:
        return False

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

reloaded = trigger_auto_reload()
print("==================================================================")
print("  [成功] 词典热注入完毕！")
if reloaded:
    print("  [自动刷新] 已通过 DevTools 协议自动触发前端热重载！")
else:
    print("  请回到 Antigravity 软件界面，按键盘快捷键 [Ctrl + R] 或 [F5] 刷新即可生效！")
print("==================================================================")

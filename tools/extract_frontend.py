# coding: utf-8
"""
Antigravity 前端资源提取与未汉化词条检索工具
用于在 Antigravity 官方发布新版本后，自动获取最新前端代码并分析新字符串。
"""
import os
import re
import urllib.request
import json
import ssl

def get_devtools_info():
    appdata = os.getenv('APPDATA', '')
    port_file = os.path.join(appdata, 'Antigravity', 'DevToolsActivePort')
    if not os.path.exists(port_file):
        print(f"[提示] 未找到 DevToolsActivePort 文件 ({port_file})，请确保 Antigravity 正在运行。")
        return None
    with open(port_file, 'r', encoding='utf-8') as f:
        port = f.readline().strip()
    return port

def fetch_frontend_bundle():
    port = get_devtools_info()
    if not port:
        return None
    
    # 允许自签名证书
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        url = f"http://127.0.0.1:{port}/json"
        req = urllib.request.urlopen(url, context=ctx)
        targets = json.loads(req.read().decode('utf-8'))
        
        main_page_url = None
        for t in targets:
            u = t.get('url', '')
            if '127.0.0.1' in u and 'section=' in u:
                main_page_url = u
                break
            if '127.0.0.1' in u and not main_page_url:
                main_page_url = u

        if not main_page_url:
            print("[错误] 未能定位到当前运行的前端主页面 URL。")
            return None

        # 提取基准地址，如 https://127.0.0.1:11105/
        base_url = re.match(r"(https?://127\.0\.0\.1:\d+)", main_page_url).group(1)
        bundle_url = f"{base_url}/main.js"
        print(f"[执行] 正在下载前端 Bundle: {bundle_url}")

        output_path = os.path.join(os.path.dirname(__file__), "latest_frontend.js")
        with urllib.request.urlopen(bundle_url, context=ctx) as response, open(output_path, 'wb') as out_file:
            out_file.write(response.read())
        
        print(f"[成功] 最新前端已保存至: {output_path} (大小: {os.path.getsize(output_path)} 字节)")
        return output_path
    except Exception as e:
        print(f"[错误] 提取失败: {e}")
        return None

def search_untranslated(keyword):
    bundle_path = os.path.join(os.path.dirname(__file__), "latest_frontend.js")
    if not os.path.exists(bundle_path):
        bundle_path = fetch_frontend_bundle()
        if not bundle_path:
            return
    
    with open(bundle_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n[搜索] 正在检索关键词: '{keyword}'...")
    matches = [m.start() for m in re.finditer(re.escape(keyword), content, re.IGNORECASE)]
    print(f"[结果] 共找到 {len(matches)} 处匹配。")
    for i, idx in enumerate(matches[:10]):
        start = max(0, idx - 150)
        end = min(len(content), idx + 150)
        snippet = content[start:end].replace('\n', ' ')
        print(f"\n--- 匹配 #{i+1} ---")
        print(snippet)

if __name__ == "__main__":
    print("=" * 60)
    print("       Antigravity 前端资源提取与词条分析工具")
    print("=" * 60)
    path = fetch_frontend_bundle()
    if path:
        kw = input("\n请输入想要搜索的英文关键词 (按回车退出): ").strip()
        if kw:
            search_untranslated(kw)

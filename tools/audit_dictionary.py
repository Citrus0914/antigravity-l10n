# coding: utf-8
"""
Antigravity 汉化词条质量与技术专有名词审查脚本
分析哪些词条存在“过度汉化”、“有争议”或“更适合保留英文”。
"""
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
patcher_path = os.path.join(parent_dir, "Antigravity-Patcher.py")
with open(patcher_path, "r", encoding="utf-8") as f:
    code = f.read()

# 提取 dictionary 和 coreWords
dict_match = re.search(r'const dictionary = \{([\s\S]*?)\};', code)
dict_str = dict_match.group(1) if dict_match else ''

core_match = re.search(r'const coreWords = \{([\s\S]*?)\};', code)
core_str = core_match.group(1) if core_match else ''

pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', dict_str)
core_pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', core_str)

print(f"主字典词条数: {len(pairs)}, 短词字典数: {len(core_pairs)}")

# 规则分类审查
# 1. 软件/产品生态专有名词 (比如 Piper, JJ, Cog, Fig, Gemini, Google, MCP, IDE)
brand_names = []
# 2. 开发者领域大家几乎习惯看英文的技术词 (比如 Commit, Fork, Diff, Prompt, Agent, Token, Branch)
dev_jargon = []
# 3. 极短词 (单个常见单词，可能在某些意外场景下产生歧义)
single_words = []
# 4. 模型版本/档位名称 (如 Flash, Pro, Ultra)
model_tiers = []

for k, v in pairs:
    # 品牌/专有工具
    if any(b in k for b in ["Piper", "JJ", "Cog", "Fig", "Gemini", "MCP", "Supabase", "GitLab", "Firebase", "BigQuery"]):
        brand_names.append((k, v))
    # 常用开发行话
    if any(j in k for j in ["Commit", "Fork", "Diff", "Prompt", "Token", "Branch", "Worktree", "Shell", "CLI", "IDE", "API"]):
        dev_jargon.append((k, v))
    # 模型名/档位
    if any(m in k for m in ["Flash", "Pro", "Ultra", "High", "Low"]):
        model_tiers.append((k, v))
    # 纯单字英语单词
    if len(k.split()) == 1 and len(k) <= 5:
        single_words.append((k, v))

print("\n=== 1. 品牌/专有工具/架构名词 ===")
for k, v in brand_names[:15]:
    print(f"  {k} -> {v}")

print("\n=== 2. 开发者高频术语 (中文 vs 英文习惯) ===")
for k, v in dev_jargon[:20]:
    print(f"  {k} -> {v}")

print("\n=== 3. 模型版本/推理档位 ===")
for k, v in model_tiers[:10]:
    print(f"  {k} -> {v}")

# 检查一些开发者高频敏感词
suspects = []
dev_keywords = ['fork', 'diff', 'merge', 'pull', 'push', 'branch', 'checkout', 'commit', 'stash', 'patch',
                'debug', 'build', 'deploy', 'run', 'test', 'lint', 'format', 'bundle', 'asset', 'hook',
                'pipeline', 'endpoint', 'server', 'client', 'proxy', 'middleware', 'runtime', 'sdk', 'api',
                'cli', 'gui', 'tui', 'ui', 'ux', 'prompt', 'token', 'embedding', 'rag', 'agent',
                'tab', 'pane', 'split', 'raw', 'preview', 'tree', 'worktree', 'workspace', 'session']

for k, v in pairs:
    if k.lower() in dev_keywords:
        suspects.append((k, v))

print("\n=== 5. 开发者敏感词/专业行话 (可能有些人更喜欢英文) ===")
for k, v in sorted(set(suspects)):
    print(f"  {k:15} -> {v}")

# 检查是否有专有名词被误译 (例如包含 MCP, Token, SemVer, Cron 等被过度汉化的情况)
over_translations = []
for k, v in pairs:
    if "Token" in k and "代币" in v:
        over_translations.append((k, v))
    if "MCP" in k and "MCP" not in v:
        over_translations.append((k, v))
    if "Cron" in k and "Cron" not in v:
        over_translations.append((k, v))
    if "Git" in k and "Git" not in v:
        over_translations.append((k, v))

print("\n=== 6. 疑似被过度翻译/破坏专有名词的词条 ===")
if over_translations:
    for k, v in over_translations:
        print(f"  [警告] {k} -> {v}")
else:
    print("  [完美] 未发现 MCP/Token/Cron/Git 等核心专有名词被破坏的情况！")


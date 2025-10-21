#!/usr/bin/env python3
"""
创建数据处理指南 Jupyter Notebook
"""
import json

notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_markdown(text):
    """添加 markdown 单元格"""
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.split("\n")
    })

def add_code(code):
    """添加代码单元格"""
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.split("\n")
    })

# ============= 标题和目录 =============
add_markdown("""# 📦 NanoChat 数据处理指南

> **写给小白的话**：这个 Notebook 会手把手教你如何准备训练数据，不需要任何专业背景，跟着运行每个单元格就行！

---

## 📚 目录

1. [核心概念：3 分钟快速理解](#核心概念)
2. [第一阶段：预训练数据](#预训练数据)
3. [第二阶段：中期训练数据](#中期训练数据)
4. [第三阶段：微调数据](#微调数据)
5. [实战：准备中文数据](#准备中文数据)
6. [数据质量检查工具](#数据质量检查)
7. [数据量计算器](#数据量计算器)
8. [完整流程检查清单](#检查清单)""")

# ============= 第1章：核心概念 =============
add_markdown("""---

## <a id="核心概念"></a>1. 核心概念：3 分钟快速理解

### 训练 AI 需要什么数据？

想象一下教小孩学说话的过程：

```
👶 第一阶段：听大量日常对话 → 学会基本语言能力
👧 第二阶段：学习问答方式 → 懂得对话结构  
👨 第三阶段：学习回答问题 → 能按要求回答
```

训练 AI 模型也是一样的 **三个阶段**：""")

add_code("""import pandas as pd

# 创建训练阶段对比表
training_stages = pd.DataFrame({
    '阶段': ['1️⃣', '2️⃣', '3️⃣'],
    '名称': ['预训练 (Pretraining)', '中期训练 (Midtraining)', '微调 (Fine-tuning)'],
    '数据类型': ['海量网页文本', '对话记录', '指令对话对'],
    '学什么': ['语言的基本规律、语法、词汇、常识', '对话的格式、一问一答的结构', '理解和执行指令、做个好助手'],
    '数据量': ['超级大 (几十 GB)', '中等 (几百 MB)', '较小 (几十 MB)']
})

print("\\n🎯 AI 训练的三个阶段\\n")
display(training_stages)
print("\\n" + "="*80)""")

add_markdown("""### 💡 为什么要分三个阶段？

**类比：就像学英语**

- **预训练** = 大量阅读英文书籍（学语法和词汇）
- **中期训练** = 学习英语对话（学怎么交流）
- **微调** = 学习回答面试问题（学特定任务）

如果直接让 AI 学习回答问题而不先学语言，就像让完全不懂英语的人直接参加英语面试，肯定学不好！""")

# ============= 第2章：预训练数据 =============
add_markdown("""---

## <a id="预训练数据"></a>2. 第一阶段：预训练数据

### 用什么数据？

项目默认使用 **FineWeb-Edu** 数据集：

- 📖 来源：HuggingFace 整理的高质量网页内容
- 📊 规模：约 1000 亿个单词（是的，1000 亿！）
- ✨ 质量：经过筛选，去掉了垃圾内容
- 🎁 免费：完全开源，直接下载

### 📊 我需要下载多少数据？

取决于你要训练多大的模型：""")

add_code("""# 不同模型规模的数据需求对比表
data_requirements = pd.DataFrame({
    '模型规模': ['d10 (迷你)', 'd12 (小)', 'd20 (默认)', 'd26 (大)', 'd32 (超大)'],
    '参数量': ['42M', '123M', '561M', '1.2B', '2.1B'],
    '需要下载': ['16 个分片', '48 个分片', '215 个分片', '460 个分片', '806 个分片'],
    '磁盘空间': ['~2GB', '~5GB', '~21GB', '~45GB', '~79GB'],
    '训练时间': ['30 分钟', '1-2 小时', '4 小时', '12 小时', '24 小时']
})

print("\\n📊 模型规模与数据需求对照表\\n")
display(data_requirements)
print("\\n💡 新手建议：先用 d10 或 d12 练手，熟悉流程后再训练大模型！")
print("="*80)""")

add_markdown("""### 🚀 如何下载？

**一条命令搞定！** 运行下面的代码单元格：""")

add_code("""# 下载 8 个分片用于训练分词器（约 800MB）
# 这是最小下载量，适合快速测试

!python -m nanochat.dataset -n 8""")

add_code("""# 如果要训练 d20 模型，需要下载更多数据
# ⚠️ 警告：这会下载约 21GB 数据，需要较长时间！
# 如果不需要，请不要运行这个单元格

# !python -m nanochat.dataset -n 215""")

add_markdown("""### 📁 数据下载到哪了？

所有数据自动保存到 `~/.cache/nanochat/base_data/`

让我们检查一下：""")

add_code("""import os
from pathlib import Path

# 获取数据目录
data_dir = Path.home() / ".cache" / "nanochat" / "base_data"

print(f"📁 数据目录: {data_dir}\\n")

if data_dir.exists():
    # 统计已下载的文件
    parquet_files = list(data_dir.glob("*.parquet"))
    
    if parquet_files:
        print(f"✅ 找到 {len(parquet_files)} 个数据文件")
        
        # 计算总大小
        total_size = sum(f.stat().st_size for f in parquet_files)
        print(f"💽 总大小: {total_size / (1024**3):.2f} GB")
        
        # 显示前 5 个文件
        print("\\n前 5 个文件:")
        for f in sorted(parquet_files)[:5]:
            size_mb = f.stat().st_size / (1024**2)
            print(f"  📄 {f.name:25s} ({size_mb:.1f} MB)")
    else:
        print("⚠️ 数据目录存在，但没有找到 .parquet 文件")
        print("   请先运行上面的下载命令！")
else:
    print("⚠️ 数据目录不存在，请先下载数据！")
    print(f"   运行: python -m nanochat.dataset -n 8")""")

add_markdown("""### 🔍 查看数据内容

让我们打开一个文件看看里面是什么：""")

add_code("""import pyarrow.parquet as pq

# 读取第一个分片
data_dir = Path.home() / ".cache" / "nanochat" / "base_data"
parquet_files = list(data_dir.glob("*.parquet")) if data_dir.exists() else []

if parquet_files:
    first_file = sorted(parquet_files)[0]
    print(f"📖 正在读取: {first_file.name}\\n")
    
    # 读取 Parquet 文件
    table = pq.read_table(first_file)
    
    print(f"📊 文件信息:")
    print(f"   行数: {len(table):,}")
    print(f"   列名: {table.column_names}")
    
    # 显示前 3 条数据
    print("\\n📝 前 3 条数据示例:\\n")
    print("=" * 80)
    
    for i in range(min(3, len(table))):
        text = table['text'][i].as_py()
        # 只显示前 200 个字符
        preview = text[:200] + "..." if len(text) > 200 else text
        print(f"\\n第 {i+1} 条 (长度: {len(text)} 字符)")
        print("-" * 80)
        print(preview)
    
    print("\\n" + "=" * 80)
else:
    print("⚠️ 找不到数据文件，请先下载数据！")""")

# ============= 第3章：中期训练数据 =============
add_markdown("""---

## <a id="中期训练数据"></a>3. 第二阶段：中期训练数据

### 用什么数据？

项目默认使用 **SmolTalk** 对话数据集：

- 🗣️ 内容：真实的人类对话记录
- 📝 格式：一问一答的对话形式
- 🎯 目的：让模型学会对话的格式

### 数据格式示例""")

add_code("""import json

# 对话数据格式示例
dialogue_example = {
    "messages": [
        {
            "role": "user",
            "content": "你好！请介绍一下自己"
        },
        {
            "role": "assistant",
            "content": "你好！我是一个 AI 助手，可以回答问题、提供建议..."
        },
        {
            "role": "user",
            "content": "你会说中文吗？"
        },
        {
            "role": "assistant",
            "content": "是的，我可以使用中文交流。"
        }
    ]
}

print("📝 对话数据格式示例：\\n")
print(json.dumps(dialogue_example, ensure_ascii=False, indent=2))

print("\\n💡 重要字段说明：")
print("   • role: 说话的角色，'user'(用户) 或 'assistant'(助手)")
print("   • content: 说话的内容")

print("\\n✅ 好消息：训练脚本会自动下载 SmolTalk 数据集，无需手动操作！")""")

# ============= 第4章：微调数据 =============
add_markdown("""---

## <a id="微调数据"></a>4. 第三阶段：微调数据

### 用什么数据？

微调阶段混合使用多个任务数据集：""")

add_code("""# 微调数据集概览
sft_datasets = pd.DataFrame({
    '数据集': ['ARC-Easy', 'ARC-Challenge', 'GSM8K', 'SmolTalk'],
    '内容': ['简单选择题', '困难选择题', '小学数学题', '日常对话'],
    '数量': ['2,300 条', '1,100 条', '8,000 条', '10,000 条'],
    '学什么能力': ['常识推理', '深度推理', '数学计算', '闲聊能力']
})

print("\\n🎯 微调阶段的数据集\\n")
display(sft_datasets)
print("\\n📊 总计：约 21,400 条训练样本")
print("="*80)""")

add_markdown("""### 数据格式示例""")

add_code("""# 数学题示例 (GSM8K)
math_example = {
    "messages": [
        {
            "role": "user",
            "content": "小明有8个苹果，吃掉了3个，还剩几个？"
        },
        {
            "role": "assistant",
            "content": "让我来算一下：\\n8 - 3 = 5\\n所以小明还剩5个苹果。"
        }
    ]
}

# 选择题示例 (ARC)
arc_example = {
    "messages": [
        {
            "role": "user",
            "content": "哪个物体会浮在水面上？\\nA. 石头\\nB. 铁钉\\nC. 木头\\nD. 玻璃球"
        },
        {
            "role": "assistant",
            "content": "答案是C. 木头。因为木头的密度比水小，所以会浮在水面上。"
        }
    ]
}

print("📝 数学题示例 (GSM8K)：\\n")
print(json.dumps(math_example, ensure_ascii=False, indent=2))

print("\\n" + "="*80 + "\\n")

print("📝 选择题示例 (ARC)：\\n")
print(json.dumps(arc_example, ensure_ascii=False, indent=2))

print("\\n✅ 这些数据集会在运行微调脚本时自动下载！")""")

# ============= 第5章：准备中文数据 =============
add_markdown("""---

## <a id="准备中文数据"></a>5. 实战：准备中文数据

> 如果你想训练中文模型，需要准备中文数据。下面是一个完整的示例！

### 方法一：使用 HuggingFace 中文数据集""")

add_code("""# 设置 HuggingFace 镜像（可选，如果下载太慢）
import os

# 使用国内镜像加速下载
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("✅ 已设置 HuggingFace 镜像：https://hf-mirror.com")
print("   这会加速数据集下载速度")""")

add_code("""# 下载中文维基百科数据（示例）
# ⚠️ 警告：这会下载较大的数据集，需要时间！
# 如果不需要，请不要运行这个单元格

from datasets import load_dataset

print("📥 正在下载中文维基百科（前 1000 条用于演示）...\\n")

try:
    # 只下载前 1000 条用于演示
    wiki = load_dataset(
        "wikipedia",
        "20220301.zh",  # 中文版本
        split="train[:1000]",  # 只取前 1000 条
        trust_remote_code=True
    )
    
    print(f"✅ 成功下载：{len(wiki):,} 条数据\\n")
    
    # 显示第一条
    print("📝 第一条数据示例：")
    print("="*80)
    first_text = wiki[0]['text'][:300] + "..."
    print(first_text)
    print("="*80)
    
except Exception as e:
    print(f"❌ 下载失败：{e}")
    print("   可能需要检查网络连接或尝试使用镜像")""")

add_markdown("""### 方法二：转换自己的文本数据

如果你有自己收集的中文文本，可以使用项目提供的转换工具：""")

add_code("""# 使用内置工具转换自定义数据
# 详细说明请查看 data_check/convert_custom_data.py

print("🛠️ 转换自定义文本数据的步骤：\\n")
print("1. 准备你的文本数据（.txt 文件）")
print("2. 运行转换命令：")
print("   python -m data_check.convert_custom_data")
print("\\n支持的输入格式：")
print("   • 单个文本文件（每行一条数据）")
print("   • 目录（包含多个 .txt 文件）")
print("\\n详细代码请查看：data_check/convert_custom_data.py")""")

# ============= 第6章：数据质量检查 =============
add_markdown("""---

## <a id="数据质量检查"></a>6. 数据质量检查工具

项目提供了完整的数据检查工具集：""")

add_code("""# 数据检查工具概览
tools = pd.DataFrame({
    '工具': [
        'check_data.py',
        'check_length_distribution.py',
        'check_content_quality.py',
        'check_char_distribution.py',
        'convert_custom_data.py'
    ],
    '用途': [
        '验证数据文件完整性',
        '检查文本长度分布',
        '抽样检查内容质量',
        '检查字符分布统计',
        '转换自定义文本数据'
    ],
    '命令': [
        'python -m data_check.check_data',
        'python -m data_check.check_length_distribution',
        'python -m data_check.check_content_quality',
        'python -m data_check.check_char_distribution',
        'python -m data_check.convert_custom_data'
    ]
})

print("\\n🛠️ 数据检查工具总览\\n")
display(tools)
print("\\n💡 所有工具的详细代码都在 data_check/ 目录下")
print("="*80)""")

add_markdown("""### 快速检查数据完整性""")

add_code("""# 运行数据完整性检查
!python -m data_check.check_data""")

add_markdown("""### 检查文本长度分布""")

add_code("""# 分析数据的长度分布
# 这有助于了解数据质量

!python -m data_check.check_length_distribution""")

# ============= 第7章：数据量计算器 =============
add_markdown("""---

## <a id="数据量计算器"></a>7. 数据量计算器

### Chinchilla 定律

**数据 token 数 = 模型参数量 × 20**

让我们计算不同模型需要多少数据：""")

add_code("""def calculate_data_requirement(model_params_million):
    \"\"\"
    计算训练所需的数据量
    
    参数:
        model_params_million: 模型参数量(百万)，如123表示123M参数
    
    返回:
        字典，包含各种数据量信息
    \"\"\"
    
    # 1. 需要的 token 数（参数量 × 20）
    tokens_billion = model_params_million / 1000 * 20
    
    # 2. 需要的字符数（1 token ≈ 4.8 字符）
    chars_billion = tokens_billion * 4.8
    
    # 3. 需要的分片数（每个分片 250M 字符）
    num_shards = int(chars_billion * 1000 / 250)
    
    # 4. 磁盘空间（每个分片约 100MB）
    disk_gb = num_shards * 100 / 1024
    
    return {
        'model_params': f"{model_params_million}M",
        'tokens': f"{tokens_billion:.1f}B",
        'chars': f"{chars_billion:.0f}B",
        'shards': num_shards,
        'disk': f"{disk_gb:.1f}GB"
    }

# 不同规模模型
models = {
    'd10': 42,
    'd12': 123,
    'd20': 561,
    'd26': 1200,
    'd32': 2100
}

results = []
for name, params in models.items():
    req = calculate_data_requirement(params)
    results.append({
        '模型': name,
        '参数量': req['model_params'],
        'Token数': req['tokens'],
        '字符数': req['chars'],
        '分片数': req['shards'],
        '磁盘': req['disk']
    })

df_results = pd.DataFrame(results)

print("\\n📊 模型数据需求计算表\\n")
display(df_results)
print("\\n💡 提示：数据量基于 Chinchilla 定律计算（参数量 × 20）")""")

add_markdown("""### 自定义计算

输入你的模型参数量，计算需要多少数据：""")

add_code("""# 自定义模型参数量（单位：百万）
my_model_params = 100  # 修改这里！

result = calculate_data_requirement(my_model_params)

print(f"\\n🎯 您的模型（{my_model_params}M 参数）需要：\\n")
print(f"   Token 数量：{result['tokens']}")
print(f"   字符数量：{result['chars']}")
print(f"   数据分片：{result['shards']} 个")
print(f"   磁盘空间：{result['disk']}")
print("\\n下载命令：")
print(f"   python -m nanochat.dataset -n {result['shards']}")""")

# ============= 第8章：检查清单 =============
add_markdown("""---

## <a id="检查清单"></a>8. 完整流程检查清单

准备好数据了吗？对照这个清单检查：""")

add_code("""import shutil

def check_data_readiness():
    \"\"\"检查数据准备情况\"\"\"
    
    print("\\n🔍 数据准备状态检查\\n")
    print("="*80)
    
    checks = []
    
    # 1. 检查预训练数据
    base_data_dir = Path.home() / ".cache" / "nanochat" / "base_data"
    if base_data_dir.exists():
        parquet_files = list(base_data_dir.glob("*.parquet"))
        if len(parquet_files) >= 8:
            checks.append(("✅", f"预训练数据：找到 {len(parquet_files)} 个分片"))
        else:
            checks.append(("⚠️", f"预训练数据：只有 {len(parquet_files)} 个分片（建议至少 8 个）"))
    else:
        checks.append(("❌", "预训练数据：未下载"))
    
    # 2. 检查分词器
    tokenizer_dir = Path.home() / ".cache" / "nanochat" / "tokenizer"
    if tokenizer_dir.exists() and list(tokenizer_dir.glob("*.model")):
        checks.append(("✅", "分词器：已训练"))
    else:
        checks.append(("⚠️", "分词器：未训练（需要运行 tok_train）"))
    
    # 3. 检查磁盘空间
    cache_dir = Path.home() / ".cache"
    if cache_dir.exists():
        try:
            stat = shutil.disk_usage(cache_dir)
            free_gb = stat.free / (1024**3)
            if free_gb > 30:
                checks.append(("✅", f"磁盘空间：剩余 {free_gb:.1f} GB"))
            else:
                checks.append(("⚠️", f"磁盘空间：剩余 {free_gb:.1f} GB（建议至少 30GB）"))
        except:
            checks.append(("ℹ️", "磁盘空间：无法检测"))
    
    # 4. 检查环境变量
    if 'HF_ENDPOINT' in os.environ:
        checks.append(("✅", f"HuggingFace 镜像：{os.environ['HF_ENDPOINT']}"))
    else:
        checks.append(("ℹ️", "HuggingFace 镜像：未设置（国内用户建议设置）"))
    
    # 显示结果
    for status, msg in checks:
        print(f"{status} {msg}")
    
    print("="*80)
    
    # 总结
    ready_count = sum(1 for s, _ in checks if s == "✅")
    total_count = len(checks)
    
    print(f"\\n📊 就绪状态：{ready_count}/{total_count}")
    
    if ready_count >= 2:  # 至少有数据和空间就算基本就绪
        print("\\n🎉 数据基本准备完成，可以开始训练了！")
    else:
        print("\\n💡 还有一些准备工作需要完成，请查看上面的提示")

# 运行检查
check_data_readiness()""")

# ============= 下一步和总结 =============
add_markdown("""---

## 🚀 下一步

数据准备好了！接下来：

### 1. 训练分词器""")

add_code("""# 训练分词器
# ⚠️ 警告：这可能需要较长时间！

# !python -m scripts.tok_train --max_chars=2000000000""")

add_markdown("""### 2. 开始预训练""")

add_code("""# 开始预训练（需要 GPU）
# ⚠️ 警告：这需要大量时间和计算资源！

# !torchrun --standalone --nproc_per_node=8 -m scripts.base_train --depth=20""")

add_markdown("""---

## 📚 扩展阅读

想深入了解？推荐阅读：

- 📄 [README.md](README.md) - 项目整体介绍
- 📄 [数据.md](数据.md) - 更详细的数据文档
- 🌐 [FineWeb-Edu 数据集](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- 📚 [Chinchilla 论文](https://arxiv.org/abs/2203.15556) - 理解数据量和模型规模的关系

---

## 💬 需要帮助？

遇到问题了？

1. 先查看本文档的各个章节
2. 运行数据检查工具诊断问题
3. 查看 `数据.md` 文档获取更详细的信息
4. 查看项目的 GitHub Issues

---

**祝你训练顺利！** 🎉

> 💡 记住：数据质量比数量更重要！不要盲目追求大数据，先用小模型验证流程，再逐步扩大规模。""")

# 保存 notebook
output_file = "数据处理指南.ipynb"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ 成功创建 Jupyter Notebook: {output_file}")
print(f"📊 共 {len(notebook['cells'])} 个单元格")
print(f"\\n使用方法：")
print(f"  jupyter notebook {output_file}")
print(f"  或使用 VS Code / JupyterLab 打开")



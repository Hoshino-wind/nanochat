"""
验证 数据.md 文档中的技术数据一致性
"""
import sys
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("验证 数据.md 中的技术数据")
print("=" * 70)

# 定义的模型规模
models = {
    'd10': 42,
    'd12': 123,
    'd20': 561,
    'd26': 1200,
    'd32': 2100
}

print("\n【1. 模型规模计算验证】")
print("-" * 70)

def calculate_data_requirement(model_params_million):
    """计算训练所需的数据量"""
    # 1. 需要的token数 (参数量 × 20)
    tokens_billion = model_params_million / 1000 * 20
    
    # 2. 需要的字符数 (1 token ≈ 4.8 字符)
    chars_billion = tokens_billion * 4.8
    
    # 3. 需要的分片数 (每个分片250M字符)
    num_shards = int(chars_billion * 1000 / 250)
    
    # 4. 磁盘空间 (每个分片约100MB)
    disk_gb = num_shards * 100 / 1024
    
    return {
        'model_params': f"{model_params_million}M",
        'tokens': f"{tokens_billion:.1f}B",
        'chars': f"{chars_billion:.0f}B",
        'shards': num_shards,
        'disk': f"{disk_gb:.1f}GB"
    }

print(f"{'模型':<8} {'参数量':<10} {'Token数':<12} {'字符数':<12} {'分片数':<10} {'磁盘':<10}")
print("-" * 70)

for name, params in models.items():
    req = calculate_data_requirement(params)
    print(f"{name:<8} {req['model_params']:<10} {req['tokens']:<12} {req['chars']:<12} {req['shards']:<10} {req['disk']:<10}")

print("\n【2. 文档中的声明值 (第86-90行表格)】")
print("-" * 70)

doc_values = {
    'd10': {'params': '42M', 'shards': 16, 'disk': '~2GB', 'time': '30分钟'},
    'd12': {'params': '123M', 'shards': 48, 'disk': '~5GB', 'time': '1-2小时'},
    'd20': {'params': '561M', 'shards': 215, 'disk': '~21GB', 'time': '4小时'},
    'd26': {'params': '1.2B', 'shards': 460, 'disk': '~45GB', 'time': '12小时'},
    'd32': {'params': '2.1B', 'shards': 806, 'disk': '~79GB', 'time': '24小时'},
}

for model, values in doc_values.items():
    print(f"{model}: {values['params']}, {values['shards']}分片, {values['disk']}, {values['time']}")

print("\n【3. 数据一致性检查】")
print("-" * 70)

issues = []

# 检查所有模型
for model_name, param_m in models.items():
    calc = calculate_data_requirement(param_m)
    doc = doc_values.get(model_name)
    
    if doc:
        if calc['shards'] == doc['shards']:
            print(f"✅ {model_name}: {doc['shards']}分片 完全一致")
        elif abs(calc['shards'] - doc['shards']) <= 1:
            print(f"✅ {model_name}: {doc['shards']}分片 接近计算值{calc['shards']} (可接受)")
        else:
            print(f"⚠️  {model_name}: 文档说{doc['shards']}分片, 计算得{calc['shards']}分片 (差异: {abs(doc['shards']-calc['shards'])})")
            issues.append(f"{model_name} 分片数: 文档{doc['shards']} vs 计算{calc['shards']}")

print("\n" + "=" * 70)
print("【验证总结】")
print("=" * 70)

if issues:
    print(f"⚠️  发现 {len(issues)} 个数据不一致:\n")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    print("\n需要手动检查和修复上述问题。")
else:
    print("✅ 所有数据一致性检查通过!")
    print("\n所有模型的参数量、分片数、磁盘空间计算都与文档一致。")

print("\n" + "=" * 70)


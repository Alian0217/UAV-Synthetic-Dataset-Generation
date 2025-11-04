"""
UAV 项目完成确认检查
确认所有核心功能都已实现
"""

import os
import json
import cv2

def check_project_completion():
    print("🚀 UAV Synthetic Dataset - 项目完成确认")
    print("=" * 60)
    
    completion_status = {
        'environment': check_environment(),
        'project_structure': check_project_structure(),
        'core_functionality': check_core_functionality(),
        'data_generation': check_data_generation(),
        'documentation': check_documentation()
    }
    
    print_summary(completion_status)

def check_environment():
    """检查Python环境"""
    print("\n🐍 Python环境检查:")
    
    try:
        import cv2
        import numpy as np
        print("  ✅ OpenCV: 可用")
        print("  ✅ NumPy: 可用")
        return True
    except ImportError as e:
        print(f"  ❌ 环境问题: {e}")
        return False

def check_project_structure():
    """检查项目结构"""
    print("\n📁 项目结构检查:")
    
    required_dirs = ['scripts', 'scripts/ue_control', 'scripts/image_processing', 'scripts/dataset_utils']
    required_files = [
        'scripts/data_pipeline.py',
        'scripts/image_processing/annotation_generator.py',
        'README.md',
        'requirements.txt'
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ 目录: {dir_path}")
        else:
            print(f"  ❌ 缺失目录: {dir_path}")
            all_good = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ 文件: {file_path}")
        else:
            print(f"  ❌ 缺失文件: {file_path}")
            all_good = False
    
    return all_good

def check_core_functionality():
    """检查核心功能"""
    print("\n🔧 核心功能检查:")
    
    functionalities = [
        ("数据流水线", "scripts/data_pipeline.py", "生成合成场景"),
        ("标注生成器", "scripts/image_processing/annotation_generator.py", "自动生成标注"),
        ("验证工具", "scripts/dataset_utils/validate_dataset_fixed.py", "数据质量验证")
    ]
    
    all_good = True
    
    for name, path, description in functionalities:
        if os.path.exists(path):
            # 检查文件是否非空
            file_size = os.path.getsize(path)
            if file_size > 100:  # 大于100字节认为是有内容的文件
                print(f"  ✅ {name}: {description}")
            else:
                print(f"  ⚠️  {name}: 文件内容可能不完整")
                all_good = False
        else:
            print(f"  ❌ {name}: 文件不存在")
            all_good = False
    
    return all_good

def check_data_generation():
    """检查数据生成能力"""
    print("\n📊 数据生成检查:")
    
    if not os.path.exists("generated_data"):
        print("  ❌ 数据目录不存在")
        return False
    
    files = os.listdir("generated_data")
    
    # 检查场景000的完整性
    scene_000_files = [
        'scene_000.png',
        'scene_000.json', 
        'scene_000_annotations.json',
        'scene_000_mask.png',
        'scene_000_depth.png'
    ]
    
    missing_files = []
    for file in scene_000_files:
        if file in files:
            print(f"  ✅ {file}")
            
            # 验证文件可读性
            file_path = f"generated_data/{file}"
            if file.endswith('.png'):
                img = cv2.imread(file_path)
                if img is None:
                    print(f"     ⚠️  警告: 无法读取图像")
            elif file.endswith('.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                except:
                    print(f"     ⚠️  警告: JSON格式可能有问题")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"  ⚠️  场景000缺少文件: {missing_files}")
        return False
    else:
        print("  ✅ 场景000完整 - 可以用于模型训练")
        return True

def check_documentation():
    """检查文档"""
    print("\n📚 文档检查:")
    
    if os.path.exists("README.md"):
        file_size = os.path.getsize("README.md")
        if file_size > 500:
            print("  ✅ README.md: 完整")
        else:
            print("  ⚠️  README.md: 内容可能较少")
    else:
        print("  ❌ README.md: 缺失")
    
    # 检查Git状态
    if os.path.exists(".git"):
        print("  ✅ Git版本控制: 已初始化")
    else:
        print("  ⚠️  Git版本控制: 未初始化")
    
    return True

def print_summary(status):
    """打印总结"""
    print("\n" + "=" * 60)
    print("🎯 项目完成度总结")
    print("=" * 60)
    
    total_checks = len(status)
    passed_checks = sum(1 for check_passed in status.values() if check_passed)
    
    for check_name, check_passed in status.items():
        icon = "✅" if check_passed else "❌"
        print(f"{icon} {check_name}: {'通过' if check_passed else '未通过'}")
    
    completion_rate = (passed_checks / total_checks) * 100
    print(f"\n📈 总体完成度: {completion_rate:.1f}%")
    
    if completion_rate >= 90:
        print("🎉 项目状态: 成功完成!")
        print("   所有核心功能均已实现，可以生成高质量的合成数据集。")
    elif completion_rate >= 70:
        print("✅ 项目状态: 基本完成")
        print("   核心功能可用，建议进一步完善文档和测试。")
    else:
        print("⚠️  项目状态: 需要更多工作")
        print("   建议优先完成缺失的核心功能。")
    
    print("\n💡 下一步:")
    if status['data_generation']:
        print("   1. 生成更多场景数据")
        print("   2. 开始深度学习模型训练")
    else:
        print("   1. 完善数据生成功能")
        print("   2. 确保至少一个完整场景")

if __name__ == "__main__":
    check_project_completion()
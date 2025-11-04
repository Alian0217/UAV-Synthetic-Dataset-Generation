"""
数据集验证工具 - 修复版
验证生成的数据集完整性和质量
"""

import os
import json
import cv2
import numpy as np

class DatasetValidator:
    """数据集验证器"""
    
    def __init__(self, data_dir="generated_data"):
        self.data_dir = data_dir
        self.validation_results = {}
    
    def validate_all(self):
        """验证整个数据集"""
        print("🔍 开始验证数据集...")
        
        results = {
            'directory_structure': self.validate_directory_structure(),
            'image_files': self.validate_image_files(),
            'metadata_files': self.validate_metadata_files(),
            'annotation_files': self.validate_annotation_files(),
            'data_consistency': self.validate_data_consistency()
        }
        
        self.print_validation_summary(results)
        return results
    
    def validate_directory_structure(self):
        """验证目录结构"""
        print("📁 验证目录结构...")
        
        if not os.path.exists(self.data_dir):
            return {
                'status': False,
                'summary': '数据目录不存在'
            }
        
        required_files = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.png') or file.endswith('.json'):
                required_files.append(file)
        
        has_scene_images = any(f.startswith('scene_') and f.endswith('.png') and not f.startswith(('mask_', 'depth_')) for f in required_files)
        has_metadata = any(f.startswith('scene_') and f.endswith('.json') and 'annotations' not in f for f in required_files)
        has_annotations = any('annotations' in f for f in required_files)
        has_masks = any(f.startswith('mask_') for f in required_files)
        has_depth = any(f.startswith('depth_') for f in required_files)
        
        status = has_scene_images and has_metadata and has_annotations
        summary = f"目录结构: {len(required_files)} 个文件"
        
        return {
            'status': status,
            'summary': summary,
            'details': {
                'scene_images': has_scene_images,
                'metadata': has_metadata,
                'annotations': has_annotations,
                'masks': has_masks,
                'depth_maps': has_depth,
                'total_files': len(required_files)
            }
        }
    
    def validate_image_files(self):
        """验证图像文件"""
        print("🖼️ 验证图像文件...")
        
        if not os.path.exists(self.data_dir):
            return {
                'status': False,
                'summary': '数据目录不存在'
            }
        
        image_files = [f for f in os.listdir(self.data_dir) 
                      if f.endswith('.png') and not f.startswith(('mask_', 'depth_'))]
        
        if not image_files:
            return {
                'status': False,
                'summary': '没有找到图像文件'
            }
        
        results = []
        for img_file in image_files:
            try:
                img_path = os.path.join(self.data_dir, img_file)
                img = cv2.imread(img_path)
                if img is not None:
                    results.append({
                        'file': img_file,
                        'status': '✅',
                        'size': img.shape,
                        'channels': img.shape[2] if len(img.shape) > 2 else 1
                    })
                else:
                    results.append({
                        'file': img_file,
                        'status': '❌',
                        'error': '无法读取图像'
                    })
            except Exception as e:
                results.append({
                    'file': img_file,
                    'status': '❌',
                    'error': str(e)
                })
        
        valid_count = len([r for r in results if r['status'] == '✅'])
        status = valid_count == len(image_files)
        summary = f'{valid_count}/{len(image_files)} 个图像文件有效'
        
        return {
            'status': status,
            'summary': summary,
            'details': results
        }
    
    def validate_metadata_files(self):
        """验证元数据文件"""
        print("📋 验证元数据文件...")
        
        if not os.path.exists(self.data_dir):
            return {
                'status': False,
                'summary': '数据目录不存在'
            }
        
        metadata_files = [f for f in os.listdir(self.data_dir) 
                         if f.endswith('.json') and 'annotations' not in f]
        
        if not metadata_files:
            return {
                'status': False,
                'summary': '没有找到元数据文件'
            }
        
        results = []
        for meta_file in metadata_files:
            try:
                meta_path = os.path.join(self.data_dir, meta_file)
                with open(meta_path, 'r') as f:
                    metadata = json.load(f)
                
                # 检查必需字段
                required_fields = ['scene_id', 'scene_type', 'camera_parameters', 'objects']
                has_required = all(field in metadata for field in required_fields)
                
                results.append({
                    'file': meta_file,
                    'status': '✅' if has_required else '❌',
                    'scene_id': metadata.get('scene_id', '缺失'),
                    'scene_type': metadata.get('scene_type', '缺失'),
                    'object_count': len(metadata.get('objects', [])),
                    'missing_fields': [f for f in required_fields if f not in metadata]
                })
            except Exception as e:
                results.append({
                    'file': meta_file,
                    'status': '❌',
                    'error': str(e)
                })
        
        valid_count = len([r for r in results if r['status'] == '✅'])
        status = valid_count == len(metadata_files)
        summary = f'{valid_count}/{len(metadata_files)} 个元数据文件有效'
        
        return {
            'status': status,
            'summary': summary,
            'details': results
        }
    
    def validate_annotation_files(self):
        """验证标注文件"""
        print("📝 验证标注文件...")
        
        if not os.path.exists(self.data_dir):
            return {
                'status': False,
                'summary': '数据目录不存在'
            }
        
        annotation_files = [f for f in os.listdir(self.data_dir) if 'annotations' in f and f.endswith('.json')]
        
        if not annotation_files:
            return {
                'status': False,
                'summary': '没有找到标注文件'
            }
        
        results = []
        for ann_file in annotation_files:
            try:
                ann_path = os.path.join(self.data_dir, ann_file)
                with open(ann_path, 'r') as f:
                    annotations = json.load(f)
                
                # 检查必需字段
                required_fields = ['image_file', 'bounding_boxes', 'camera_pose']
                has_required = all(field in annotations for field in required_fields)
                
                results.append({
                    'file': ann_file,
                    'status': '✅' if has_required else '❌',
                    'image_file': annotations.get('image_file', '缺失'),
                    'bbox_count': len(annotations.get('bounding_boxes', [])),
                    'missing_fields': [f for f in required_fields if f not in annotations]
                })
            except Exception as e:
                results.append({
                    'file': ann_file,
                    'status': '❌',
                    'error': str(e)
                })
        
        valid_count = len([r for r in results if r['status'] == '✅'])
        status = valid_count == len(annotation_files)
        summary = f'{valid_count}/{len(annotation_files)} 个标注文件有效'
        
        return {
            'status': status,
            'summary': summary,
            'details': results
        }
    
    def validate_data_consistency(self):
        """验证数据一致性"""
        print("🔗 验证数据一致性...")
        
        if not os.path.exists(self.data_dir):
            return {
                'status': False,
                'summary': '数据目录不存在'
            }
        
        # 检查图像和元数据的对应关系
        scene_images = [f for f in os.listdir(self.data_dir) 
                       if f.startswith('scene_') and f.endswith('.png') and not f.startswith(('mask_', 'depth_'))]
        metadata_files = [f for f in os.listdir(self.data_dir) 
                         if f.startswith('scene_') and f.endswith('.json') and 'annotations' not in f]
        
        consistency_issues = []
        
        for img_file in scene_images:
            base_name = img_file.replace('.png', '')
            corresponding_meta = base_name + '.json'
            corresponding_ann = base_name + '_annotations.json'
            corresponding_mask = 'mask_' + img_file
            corresponding_depth = 'depth_' + img_file
            
            missing_files = []
            if corresponding_meta not in metadata_files:
                missing_files.append(corresponding_meta)
            if corresponding_ann not in os.listdir(self.data_dir):
                missing_files.append(corresponding_ann)
            if corresponding_mask not in os.listdir(self.data_dir):
                missing_files.append(corresponding_mask)
            if corresponding_depth not in os.listdir(self.data_dir):
                missing_files.append(corresponding_depth)
            
            if missing_files:
                consistency_issues.append({
                    'image': img_file,
                    'missing_files': missing_files
                })
        
        status = len(consistency_issues) == 0
        summary = f'一致性检查: {len(consistency_issues)} 个问题' if consistency_issues else '所有文件对应关系正确'
        
        return {
            'status': status,
            'summary': summary,
            'details': consistency_issues
        }
    
    def print_validation_summary(self, results):
        """打印验证总结"""
        print("\n" + "="*60)
        print("                   数据集验证总结")
        print("="*60)
        
        all_passed = all(result['status'] for result in results.values())
        
        for check_name, result in results.items():
            status_icon = "✅" if result['status'] else "❌"
            # 确保每个结果都有 summary 字段
            summary = result.get('summary', '无总结信息')
            print(f"{status_icon} {check_name}: {summary}")
        
        print("\n" + "="*60)
        if all_passed:
            print("🎉 数据集验证通过！所有检查项均成功。")
        else:
            print("⚠️  数据集存在一些问题，请查看详细报告。")
        
        return all_passed

def main():
    """主验证函数"""
    print("🚀 UAV Synthetic Dataset - 数据验证")
    print("="*60)
    
    validator = DatasetValidator()
    results = validator.validate_all()
    
    # 保存验证报告
    report_path = "generated_data/validation_report.json"
    with open(report_path, 'w') as f:
        # 确保所有结果都可序列化
        serializable_results = {}
        for key, value in results.items():
            if 'details' in value:
                # 简化 details 以便序列化
                value['details_count'] = len(value['details'])
            serializable_results[key] = value
        
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n📄 详细验证报告已保存: {report_path}")

if __name__ == "__main__":
    main()
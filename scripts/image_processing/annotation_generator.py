"""
标注生成模块
使用 OpenCV 生成合成数据的标注
"""

import cv2
import numpy as np
import json
import os

class AnnotationGenerator:
    """标注生成器"""
    
    def __init__(self):
        print("🖊️ 标注生成器初始化")
    
    def generate_annotations(self, image_path, metadata_path):
        """为图像生成标注"""
        # 读取图像和元数据
        image = cv2.imread(image_path)
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # 生成分割掩码
        segmentation_mask = self._create_segmentation_mask(image, metadata)
        
        # 生成边界框
        bounding_boxes = self._create_bounding_boxes(metadata)
        
        # 生成深度图（模拟）
        depth_map = self._create_depth_map(image.shape, metadata)
        
        annotations = {
            'image_file': os.path.basename(image_path),
            'metadata_file': os.path.basename(metadata_path),
            'image_size': [image.shape[1], image.shape[0]],  # [width, height]
            'segmentation_mask': 'mask_' + os.path.basename(image_path),
            'bounding_boxes': bounding_boxes,
            'depth_map': 'depth_' + os.path.basename(image_path),
            'camera_pose': metadata['camera_parameters']
        }
        
        # 保存标注文件
        annotation_path = image_path.replace('.png', '_annotations.json')
        with open(annotation_path, 'w') as f:
            json.dump(annotations, f, indent=2)
        
        # 保存分割掩码和深度图
        mask_path = image_path.replace('.png', '_mask.png')
        depth_path = image_path.replace('.png', '_depth.png')
        cv2.imwrite(mask_path, segmentation_mask)
        cv2.imwrite(depth_path, depth_map)
        
        print(f"✅ 标注生成完成: {annotation_path}")
        return annotations
    
    def _create_segmentation_mask(self, image, metadata):
        """创建分割掩码"""
        height, width = image.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # 根据元数据在掩码上标记不同物体类型
        for i, obj in enumerate(metadata['objects']):
            obj_type = obj['type']
            obj_value = self._get_object_class_value(obj_type)
            
            # 简化：在图像中心区域绘制标记
            center_x, center_y = width // 2, height // 2
            obj_x = center_x + (i - len(metadata['objects'])//2) * 80
            obj_y = center_y
            
            if obj_type == 'building':
                cv2.rectangle(mask, (obj_x-30, obj_y-50), (obj_x+30, obj_y), obj_value, -1)
            elif obj_type == 'tree':
                cv2.circle(mask, (obj_x, obj_y), 25, obj_value, -1)
            else:
                cv2.rectangle(mask, (obj_x-20, obj_y-20), (obj_x+20, obj_y+20), obj_value, -1)
        
        return mask
    
    def _get_object_class_value(self, obj_type):
        """获取物体类型的分类值"""
        class_map = {
            'building': 1,
            'tree': 2,
            'obstacle': 3
        }
        return class_map.get(obj_type, 0)
    
    def _create_bounding_boxes(self, metadata):
        """创建边界框标注"""
        bboxes = []
        
        for i, obj in enumerate(metadata['objects']):
            bbox = {
                'object_id': i,
                'class': obj['type'],
                'bbox': [  # [x, y, width, height] 归一化坐标
                    0.3 + (i * 0.1), 0.4, 0.1, 0.2
                ],
                'position': obj['position']
            }
            bboxes.append(bbox)
        
        return bboxes
    
    def _create_depth_map(self, image_shape, metadata):
        """创建深度图（模拟）"""
        height, width = image_shape[:2]
        depth_map = np.ones((height, width), dtype=np.uint8) * 128
        
        # 根据物体位置添加深度变化
        for i, obj in enumerate(metadata['objects']):
            center_x, center_y = width // 2, height // 2
            obj_x = center_x + (i - len(metadata['objects'])//2) * 80
            
            # 深度值与高度相关
            depth_value = max(50, min(200, 150 - i * 20))
            cv2.circle(depth_map, (obj_x, center_y), 40, depth_value, -1)
        
        return depth_map

def process_all_scenes():
    """处理所有生成的场景"""
    data_dir = "generated_data"
    generator = AnnotationGenerator()
    
    processed_count = 0
    for file in os.listdir(data_dir):
        if file.endswith('.png') and not file.startswith(('mask_', 'depth_')):
            image_path = os.path.join(data_dir, file)
            metadata_path = image_path.replace('.png', '.json')
            
            if os.path.exists(metadata_path):
                generator.generate_annotations(image_path, metadata_path)
                processed_count += 1
    
    print(f"\n🎉 标注处理完成! 处理了 {processed_count} 个场景")

if __name__ == "__main__":
    process_all_scenes()
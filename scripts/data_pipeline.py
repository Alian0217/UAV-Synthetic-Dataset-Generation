"""
UAV 数据流水线框架
纯 Python 实现，不依赖 UE4.27 API
"""

import cv2
import numpy as np
import json
import os
from datetime import datetime

class UAVDataPipeline:
    """UAV 数据生成流水线"""
    
    def __init__(self):
        self.output_dir = "generated_data"
        os.makedirs(self.output_dir, exist_ok=True)
        print("🚀 UAV 数据流水线初始化完成")
    
    def generate_synthetic_scenes(self, num_scenes=5):
        """生成合成场景数据"""
        print(f"\n🎨 生成 {num_scenes} 个合成场景...")
        
        scenes = []
        for i in range(num_scenes):
            scene_data = self._create_scene(i)
            scenes.append(scene_data)
            
            # 生成场景图像
            scene_image = self._render_scene(scene_data)
            image_path = f"{self.output_dir}/scene_{i:03d}.png"
            cv2.imwrite(image_path, scene_image)
            
            # 保存场景元数据
            meta_path = f"{self.output_dir}/scene_{i:03d}.json"
            with open(meta_path, 'w') as f:
                json.dump(scene_data, f, indent=2)
            
            print(f"✅ 场景 {i} 生成完成: {image_path}")
        
        return scenes
    
    def _create_scene(self, scene_id):
        """创建场景数据"""
        scene_types = ['urban', 'forest', 'open_field', 'industrial', 'residential']
        scene_type = scene_types[scene_id % len(scene_types)]
        
        return {
            'scene_id': scene_id,
            'scene_type': scene_type,
            'timestamp': datetime.now().isoformat(),
            'camera_parameters': {
                'position': [0, 0, 100 + scene_id * 50],  # 递增高度
                'rotation': [-90, 0, 0],  # 向下看
                'fov': 90,
                'resolution': [640, 480]
            },
            'objects': self._generate_objects(scene_type),
            'lighting_conditions': 'daylight'
        }
    
    def _generate_objects(self, scene_type):
        """根据场景类型生成物体"""
        objects = []
        
        if scene_type == 'urban':
            # 城市场景：建筑物
            for i in range(5):
                objects.append({
                    'type': 'building',
                    'position': [i * 200 - 400, 0, 0],
                    'size': [100, 100, 150 + i * 50],
                    'color': [100, 100, 100]
                })
        elif scene_type == 'forest':
            # 森林场景：树木
            for i in range(8):
                objects.append({
                    'type': 'tree',
                    'position': [np.random.randint(-300, 300), np.random.randint(-300, 300), 0],
                    'size': [40, 40, 100 + np.random.randint(0, 50)],
                    'color': [0, 100 + np.random.randint(0, 50), 0]
                })
        else:
            # 开阔地：少量随机物体
            for i in range(3):
                objects.append({
                    'type': 'obstacle',
                    'position': [np.random.randint(-200, 200), np.random.randint(-200, 200), 0],
                    'size': [50, 50, 30 + np.random.randint(0, 70)],
                    'color': [np.random.randint(50, 150) for _ in range(3)]
                })
        
        return objects
    
    def _render_scene(self, scene_data):
        """渲染场景为图像"""
        height, width = 480, 640
        img = np.ones((height, width, 3), dtype=np.uint8) * 200  # 灰色背景
        
        # 根据场景类型设置基础颜色
        if scene_data['scene_type'] == 'forest':
            img = np.ones((height, width, 3), dtype=np.uint8) * (0, 80, 0)
        elif scene_data['scene_type'] == 'open_field':
            img = np.ones((height, width, 3), dtype=np.uint8) * (100, 150, 100)
        
        # 渲染物体
        for obj in scene_data['objects']:
            self._draw_object(img, obj)
        
        # 添加场景信息文本
        text = f"Scene: {scene_data['scene_type']} - Alt: {scene_data['camera_parameters']['position'][2]}m"
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return img
    
    def _draw_object(self, img, obj):
        """在图像上绘制物体"""
        height, width = img.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # 将物体位置转换为图像坐标
        obj_x = int(center_x + obj['position'][0] / 10)
        obj_y = int(center_y + obj['position'][1] / 10)
        obj_size = int(obj['size'][2] / 5)  # 高度决定大小
        
        color = tuple(obj['color'])
        
        if obj['type'] == 'building':
            # 绘制矩形建筑物
            cv2.rectangle(img, 
                         (obj_x - obj_size//2, obj_y - obj_size),
                         (obj_x + obj_size//2, obj_y), 
                         color, -1)
        elif obj['type'] == 'tree':
            # 绘制圆形树木
            cv2.circle(img, (obj_x, obj_y), obj_size, color, -1)
        else:
            # 绘制矩形障碍物
            cv2.rectangle(img, 
                         (obj_x - obj_size//2, obj_y - obj_size//2),
                         (obj_x + obj_size//2, obj_y + obj_size//2), 
                         color, -1)

def main():
    """主函数"""
    print("=" * 50)
    print("   UAV Synthetic Dataset - 数据流水线")
    print("=" * 50)
    
    # 创建流水线实例
    pipeline = UAVDataPipeline()
    
    # 生成合成数据
    scenes = pipeline.generate_synthetic_scenes(5)
    
    print(f"\n🎉 数据生成完成!")
    print(f"生成了 {len(scenes)} 个场景")
    print(f"数据保存在: {pipeline.output_dir}/")
    print(f"包含: PNG图像 + JSON元数据")

if __name__ == "__main__":
    main()
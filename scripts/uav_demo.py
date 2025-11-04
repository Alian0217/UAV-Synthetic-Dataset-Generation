import cv2
import numpy as np
import os

print("UAV Synthetic Dataset - Demo")
print("=" * 40)

# Check environment
print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")

# Create sample data
os.makedirs('demo_output', exist_ok=True)

# Generate sample UAV images
for i in range(3):
    # Create different scenarios
    if i == 0:
        img = np.ones((400, 600, 3), dtype=np.uint8) * 150  # Urban
        cv2.rectangle(img, (100, 200), (200, 350), (100, 100, 100), -1)
        scene = "urban"
    elif i == 1:
        img = np.ones((400, 600, 3), dtype=np.uint8) * (0, 100, 0)  # Forest
        cv2.circle(img, (300, 200), 50, (0, 150, 0), -1)
        scene = "forest"
    else:
        img = np.ones((400, 600, 3), dtype=np.uint8) * (100, 150, 100)  # Field
        scene = "field"
    
    # Add text
    cv2.putText(img, f'Scene: {scene}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, f'Altitude: {50 + i * 25}m', (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Save image
    filename = f'demo_output/{scene}_sample_{i:02d}.png'
    cv2.imwrite(filename, img)
    print(f"Generated: {filename}")

print("Demo completed successfully!")

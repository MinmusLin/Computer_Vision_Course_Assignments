# Qusetion 9

In some vision-based ADAS systems, walking pedestrian detection and distance measurement are required. Suppose that you are confronted with such a task. The only sensor supplied to you is a monocular camera. Please give your solutions and provide as many details as possible.

在一些基于视觉的先进驾驶辅助系统（ADAS）中，需要对行人进行检测并测量其距离。假设你面临这样的任务，而唯一提供的传感器是一个单目摄像头。请给出你的解决方案，并尽可能提供更多细节。

## Answer

1. **相机校准**：相机校准通过检测棋盘格角点并利用已知的 3D 世界坐标，计算相机的内参和外参，为后续图像校正和距离测量提供基础。
2. **目标检测**：使用 YOLOv8 等深度学习模型检测图像中的行人，获取其边界框和中心点坐标，确保检测的准确性和实时性，为距离测量提供目标位置信息。
3. **单应性矩阵估计**：通过选择地面上的特征点并计算其图像坐标与世界坐标的对应关系，利用 OpenCV 求解单应性矩阵，建立图像平面到地面平面的映射关系。
4. **距离测量**：将行人边界框中心点转换为齐次坐标，应用单应性矩阵映射到世界坐标，对坐标归一化并提取 Y 轴值并转换为实际距离，实现相机与行人之间距离的精确测量。
5. **系统集成与优化**：将上述步骤集成到 ADAS 系统中，优化算法以提高实时性，并通过多帧融合和误差校正提升检测和距离测量的精度与稳定性。
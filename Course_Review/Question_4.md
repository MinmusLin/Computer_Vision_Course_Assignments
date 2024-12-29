# Qusetion 4

RANSAC (random sample sonsensus) is a framework commonly used for fitting models from observations with potential outliers. Suppose that $I_1$ and $I_2$ are two images, captured from the same physical plane. $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$ are correspondence pairs, where $\mathbf{x}_i$ and $\mathbf{y}_i$ are the positions of the key points in $I_1$ and $I_2$ , respectively. What are the steps for estimating the homography matrix between $I_1$ and $I_2$ based on $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$ using RANSAC?

RANSAC（随机抽样一致性）是一种常用于从包含潜在异常值的观测数据中拟合模型的框架。假设 $I_1$ 和 $I_2$ 是从同一物理平面捕获的两幅图像， $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$ 是对应点对，其中 $\mathbf{x}_i$ 和 $\mathbf{y}_i$ 分别是关键点在 $I_1$ 和 $I_2$ 中的位置。基于 $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$ ，使用 RANSAC 估计 $I_1$ 和 $I_2$ 之间的单应性矩阵的步骤是什么？

## Answer

### Step 0: 问题定义

单应性矩阵 $H$ 是一个 $3 \times 3$ 的矩阵，用于描述两幅图像之间的投影变换关系。对于对应点对 $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$，满足：

$$
\mathbf{y}_i \sim H \mathbf{x}_i
$$

其中 $\mathbf{x}_i = (x_i, y_i, 1)^T$ 和 $\mathbf{y}_i = (x'_i, y'_i, 1)^T$ 是齐次坐标。

### Step 1：随机采样

从对应点对 $\{\mathbf{x}_i, \mathbf{y}_i\}_{i=1}^n$ 中随机选择 $m$ 对点（因为单应性矩阵有 8 个自由度，至少需要 4 对点来求解）。

### Step 2：模型估计

使用选中的 $m$ 个点对估计单应性矩阵 $H$ 。对于每个点对 $(\mathbf{x}_i, \mathbf{y}_i)$ ，有：

$$
\begin{bmatrix}
x'_i \\
y'_i \\
1
\end{bmatrix}
\sim
\begin{bmatrix}
h_{11} & h_{12} & h_{13} \\
h_{21} & h_{22} & h_{23} \\
h_{31} & h_{32} & h_{33}
\end{bmatrix}
\begin{bmatrix}
x_i \\
y_i \\
1
\end{bmatrix}
$$

展开后得到两个方程：

$$
x'_i = \frac{h_{11} x_i + h_{12} y_i + h_{13}}{h_{31} x_i + h_{32} y_i + h_{33}}, \quad
y'_i = \frac{h_{21} x_i + h_{22} y_i + h_{23}}{h_{31} x_i + h_{32} y_i + h_{33}}
$$

将方程线性化，得到：

$$
\begin{bmatrix}
x_i & y_i & 1 & 0 & 0 & 0 & -x'_i x_i & -x'_i y_i & -x'_i \\
0 & 0 & 0 & x_i & y_i & 1 & -y'_i x_i & -y'_i y_i & -y'_i
\end{bmatrix}
\begin{bmatrix}
h_{11} \\
h_{12} \\
h_{13} \\
h_{21} \\
h_{22} \\
h_{23} \\
h_{31} \\
h_{32} \\
h_{33}
\end{bmatrix}
= \mathbf{0}
$$

对于每个点对 $(\mathbf{x}_i, \mathbf{y}_i)$ ，可以得到两个方程。因此，对于 $m$ 个点对，可以构建一个 $2m \times 9$ 的矩阵 $A$ ：

$$
A = \begin{bmatrix}
x_1 & y_1 & 1 & 0 & 0 & 0 & -x'_1 x_1 & -x'_1 y_1 & -x'_1 \\
0 & 0 & 0 & x_1 & y_1 & 1 & -y'_1 x_1 & -y'_1 y_1 & -y'_1 \\
x_2 & y_2 & 1 & 0 & 0 & 0 & -x'_2 x_2 & -x'_2 y_2 & -x'_2 \\
0 & 0 & 0 & x_2 & y_2 & 1 & -y'_2 x_2 & -y'_2 y_2 & -y'_2 \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
x_m & y_m & 1 & 0 & 0 & 0 & -x'_m x_m & -x'_m y_m & -x'_m \\
0 & 0 & 0 & x_m & y_m & 1 & -y'_m x_m & -y'_m y_m & -y'_m
\end{bmatrix}
$$

目标是求解 $A\mathbf{h} = 0$ ，其中 $\mathbf{h} = \begin{bmatrix}h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33}\end{bmatrix}^T $ 。

通过奇异值分解（SVD）来求解单应性矩阵 $H$ ，为了保证单应性矩阵 $H$ 的唯一性，通常将 $H$ 的最后一个元素 $h_{33}$ 归一化为 1。

### Step 3：计算误差

对于所有对应点对，计算投影误差：

$$
\text{error} = \|\mathbf{y}_i - H \mathbf{x}_i\|_2
$$

设定一个阈值 $\epsilon$ ，将误差小于 $\epsilon$ 的点对标记为内点，否则标记为外点。

### Step 4：评估模型

统计内点的数量。如果当前模型的内点数量大于之前的最佳模型，则更新最佳模型和内点集合。

### Step 5：迭代

重复步骤 1 到步骤 4，直到达到预设的迭代次数 $N$。迭代次数 $N$ 可以根据内点比例动态调整：

$$
N = \frac{\log(1 - p)}{\log(1 - (1 - \eta)^m)}
$$

其中 $p$ 是置信度（通常取 0.99），$\eta$ 是内点比例，$m$ 是每次采样所需的点对数。

### Step 6：重新估计模型

使用最终的内点集合，重新估计单应性矩阵 $H$ 。
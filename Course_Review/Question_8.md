# Qusetion 8

Camera intrinsics calibration. Suppose that we have a calibration board with chessboard patterns. Altogether, there are $N$ cross-points on the calibration board. For calibration, $M$ images of the calibration board are taken.

相机内参标定。假设我们有一个带有棋盘图案的标定板。标定板上总共有 $N$ 个交叉点。为了进行标定，拍摄了标定板的 $M$ 张图像。

## Qusetion 8.1

In our lecture, we formulated the intrinsics calibration problem as a nonlinear least-squares problem. Please write down the objective function of such a nonlinear least-squares problem and try to explain its physical meaning in detail.

在我们的讲座中，我们将内参标定问题表述为一个非线性最小二乘问题。请写出该非线性最小二乘问题的目标函数，并尝试详细解释其物理意义。

## Qusetion 8.2

Nonlinear least-squares. Suppose that $f(x)=(f_{1}(x),f_{2}(x),...,f_{m}(x))：\mathbb{R}^{n} \rightarrow \mathbb{R}^{m}, x \in \mathbb{R}^{n}, f \in \mathbb{R}^{m}$ and some $f_{i}(x)：\mathbb{R}^{n} \rightarrow \mathbb{R}$ is a (are) non-linear function(s). Then, the problem,

$$
x^{*}= \arg \min_{x} \frac{1}{2} \| f(x) \|_{2}^{2} = \arg \min_{x} \frac{1}{2} (f(x))^{T} f(x)
$$

is a nonlinear least-squares problem. In our lecture, we mentioned that Levenberg-Marquardt algorithm is a typical method to solve this problem. In L-M algorithm, for each updating step, at the current x, a local approximation model is constructed as,

$$
L(h) = \frac{1}{2} (f(x+h))^{T} f(x+h) + \frac{1}{2} \mu h^{T} h = \frac{1}{2} (f(x))^{T} f(x)+h^{T} (J(x))^{T} f(x) + \frac{1}{2} h^{T} (J(x))^{T} J(x) h + \frac{1}{2} \mu h^{T} h
$$

where $J(x)$ is $f(x)$ 's Jacobian matrix, and $\mu > 0$ is the damped coefficient. Please prove that $L(h)$ is a strictly convex function. (**Hint**：If a function $L(h)$ is differentiable up to at least second order, $L$ is strictly convex if its Hessian matrix is positive definite.)

非线性最小二乘法。假设 $f(x)=(f_{1}(x),f_{2}(x),...,f_{m}(x))：\mathbb{R}^{n} \rightarrow \mathbb{R}^{m}, x \in \mathbb{R}^{n}, f \in \mathbb{R}^{m}$ 且某些 $f_{i}(x)：\mathbb{R}^{n} \rightarrow \mathbb{R}$ 是非线性函数。那么，问题

$$
x^{*}= \arg \min_{x} \frac{1}{2} \| f(x) \|_{2}^{2} = \arg \min_{x} \frac{1}{2} (f(x))^{T} f(x)
$$

是一个非线性最小二乘问题。在我们的讲座中，我们提到 Levenberg-Marquardt 算法是解决这个问题的典型方法。在 L-M 算法中，对于每个更新步骤，在当前 $x$ 处，构建一个局部近似模型为

$$
L(h) = \frac{1}{2} (f(x+h))^{T} f(x+h) + \frac{1}{2} \mu h^{T} h = \frac{1}{2} (f(x))^{T} f(x)+h^{T} (J(x))^{T} f(x) + \frac{1}{2} h^{T} (J(x))^{T} J(x) h + \frac{1}{2} \mu h^{T} h
$$

其中 $J(x)$ 是 $f(x)$ 的雅可比矩阵，且 $\mu > 0$ 是阻尼系数。请证明 $L(h)$ 是一个严格凸函数。（**提示**：如果一个函数 $L(h)$ 至少可微到二阶，且其 Hessian 矩阵是正定的，则 $L$ 是严格凸的。）

## Answer

### Answer 1

目标函数为：

$$
\Theta^{*}=\arg\min_{\Theta}\sum_{i=1}^{M}\sum_{j=1}^{N}\frac{1}{2}\Vert\mathbf{K}\cdot\mathcal{D}\left\{\frac{1}{Z_{Cij}}\left[\mathcal{R}\left(\mathbf{d}_{i}\right)\mathbf{t}_{i}\right]\mathbf{P}_{j}\right\}-\mathbf{u}_{ij}\Vert_{2}^{2}
$$

### 参数定义

* **$\Theta$**：待优化的参数集合
* **$\mathbf{K}$**：相机的内参矩阵
* **$\mathcal{D}$**：畸变模型
* **$Z_{Cij}$**：标定板上第 $j$ 个交叉点在相机坐标系下的深度
* **$\mathcal{R}(\mathbf{d}_{i})$ 和 $\mathbf{t}_{i}$**：第 $i$ 张图像对应的外参，其中 $\mathcal{R}(\mathbf{d}_{i})$ 是旋转矩阵，$\mathbf{t}_{i}$ 是平移向量。$\mathbf{d}_{i}$ 是旋转向量
* **$\mathbf{P}_{j}$**：标定板上第 $j$ 个交叉点的三维坐标，通常假设标定板位于 $Z=0$ 平面，因此 $\mathbf{P}_{j} = [X_j, Y_j, 0]^T$
* **$\mathbf{u}_{ij}$**：标定板上第 $j$ 个交叉点在第 $i$ 张图像中的二维像素坐标

### 物理意义

#### 投影过程

1. **$\frac{1}{Z_{Cij}}\left[\mathcal{R}\left(\mathbf{d}_{i}\right)\mathbf{t}_{i}\right]\mathbf{P}_{j}$**：这部分表示将标定板上的三维点 $\mathbf{P}_{j}$ 转换到相机坐标系下。$\mathcal{R}\left(\mathbf{d}_{i}\right)$ 和 $\mathbf{t}_{i}$ 是外参，用于将世界坐标系下的点转换到相机坐标系。$\frac{1}{Z_{Cij}}$ 是归一化因子，将点投影到归一化图像平面（即 $Z=1$ 平面）。
2. **$\mathcal{D}\{...\}$**：畸变校正步骤，用于校正镜头畸变。
3. **$\mathbf{K}\cdot\mathcal{D}\{...\}$**：将归一化图像平面上的点通过内参矩阵 $\mathbf{K}$ 投影到像素坐标系，得到最终的像素坐标。

#### 误差项

**$\Vert\mathbf{K}\cdot\mathcal{D}\left\{\frac{1}{Z_{Cij}}\left[\mathcal{R}\left(\mathbf{d}_{i}\right)\mathbf{t}_{i}\right]\mathbf{P}_{j}\right\}-\mathbf{u}_{ij}\Vert_{2}^{2}$**：重投影误差，表示通过相机模型计算得到的像素坐标与实际观测到的像素坐标 $\mathbf{u}_{ij}$ 之间的欧氏距离的平方。这个误差项衡量了相机模型的准确性。

#### 目标函数

**$\sum_{i=1}^{M}\sum_{j=1}^{N}\frac{1}{2}\Vert...\Vert_{2}^{2}$**：这是对所有图像和所有标定板交叉点的重投影误差求和。目标是通过优化参数 $\Theta$，使得这个总误差最小。$\frac{1}{2}$ 是为了在求导时简化计算。

#### 物理意义

这个目标函数的物理意义是通过最小化重投影误差，找到一组最优的相机内参和外参，使得相机模型能够准确地描述实际成像过程。

### Answer 2

根据问题已知：

$$
L(h) = \frac{1}{2} (f(x+h))^{T} f(x+h) + \frac{1}{2} \mu h^{T} h
$$

$$
= \frac{1}{2} (f(x))^{T} f(x)+h^{T} (J(x))^{T} f(x) + \frac{1}{2} h^{T} (J(x))^{T} J(x) h + \frac{1}{2} \mu h^{T} h
$$

首先，对 $L(h)$ 关于 $h$ 求梯度：

$$
\nabla L(h) = (J(x))^{T}f(x) + (J(x))^{T}J(x)h + \mu h
$$

对 $\nabla L(h)$ 再次关于 h 求导，得到 Hessian 矩阵：

$$
\nabla^{2} L(h) = (J(x))^{T}J(x) + \mu I
$$

其中 $I$ 是单位矩阵。

要证明 Hessian 矩阵是正定的，需要证明对于任意非零向量 $v \in \mathbb{R}^{n} $ ， $v^T\nabla^{2} L(h)v > 0$ 。

$$
v^T\nabla^{2} L(h)v = v^T((J(x))^{T}J(x) + \mu I)v = v^T(J(x))^{T}J(x)v + \mu v^T v
$$

由于 $\mu > 0$ 且 $v^T v > 0$ ，因此只需证明 $v^T(J(x))^{T}J(x)v \geq 0$ 。

$$
v^T(J(x))^{T}J(x)v = (J(x)v)^{T}(J(x)v) \geq 0
$$

所以 $v^T\nabla^{2} L(h)v = v^T(J(x))^{T}J(x)v + \mu v^T v > 0$ ，因此 Hessian 矩阵是正定的，所以 $L(h)$ 是一个严格凸函数。
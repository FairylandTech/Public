# coding: utf8
""" 
@File: Kriging.py
@Editor: PyCharm
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@OS: Windows 11 Professional Workstation 22H2
@Environment: Python3.9 (FairyAdministrator)
@CreatedTime: 2023/3/9 16:26
"""

from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
import numpy as np
import matplotlib.pyplot as plt

# 创建样本点和目标变量
X = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
y = np.array([0, 1, 2, 3])

# 指定半方差函数并使用高斯过程回归器进行拟合
kernel = ConstantKernel() + RBF()
model = GaussianProcessRegressor(kernel=kernel)
model.fit(X, y)

# 使用回归器对新数据进行预测
X_new = np.array([[0.5, 0.5], [1.5, 1.5], [2.5, 2.5], [3.5, 3.5]])
y_pred = model.predict(X_new)

# 绘制原始数据和预测结果
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.scatter(X_new[:, 0], X_new[:, 1], c=y_pred, marker='x')
plt.show()

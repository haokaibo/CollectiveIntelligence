import numpy as np


def computerCost(X, y, theta):
    m = len(y)
    J = 0
    J = (np.transpose(X * theta - y)) * (X * theta - y) / (2 * m)  # compute the cost J

    return J


def gradientDescent(X, y, theta, alpha, num_iters):
    m = len(y)

    n = len(theta)

    temp = np.matrix(np.zeros((n, num_iters)))  # 暂存每次迭代计算的theta，转化为矩阵形式

    J_history = np.zeros((num_iters, 1))  # 记录每次迭代计算的代价值

    for i in range(num_iters):  # 遍历迭代次数

        h = np.dot(X, theta)  # 计算内积，matrix可以直接乘

        temp[:, i] = theta - ((alpha / m) * (np.dot(np.transpose(X), h - y)))  # 梯度的计算

        theta = temp[:, i]

        J_history[i] = computerCost(X, y, theta)  # 调用计算代价函数

        print '.',

    return theta, J_history
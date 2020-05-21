# 文件介绍

sourceCode下的文件都是flask部分所需要的。其中

[func.py](../sourceCode/func.py)是一些备调用的函数，包括将`list`转化为html标签的`gethtml`函数，作图的`create_*_figure`函数,与绘制协方差矩阵的`get_corr`函数

[linear_reg.py](../sourceCode/linear_reg.py)对应于一般的线性回归模型，衡量解释变量变化一个单位导致被解释变量变化多少单位。

[exp_reg_model.py](../sourceCode/exp_reg_model.py)对应于双对数模型，用来度量弹性，衡量解释变量到一个百分比变化导致被解释变量相对变化多少。

[lin_log_model.py](../sourceCode/lin_log_model.py)对应于线性到对数模型，用来度量增长率，衡量解释变量绝对变化一个单位导致被解释变量相对变化多少单位。

[log_lin_model.py](../sourceCode/log_lin_model.py)对应于对数到线性模型，衡量解释变量相对变化一个单位导致被解释变量绝对变化多少单位。
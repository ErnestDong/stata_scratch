# 文件介绍

sourceCode 下的文件都是 flask 部分所需要的。其中

[func.py](../sourceCode/func.py)是一些备调用的函数，包括将`list`转化为 html 标签的`gethtml`函数，作图的`create_*_figure`函数,与绘制协方差矩阵的`get_corr`函数

[code.py](../sourceCode/code.py)利用Huffman树用于编码和解码用户的敏感信息。

[linear_reg.py](../sourceCode/linear_reg.py)对应于一般的线性回归模型，衡量解释变量变化一个单位导致被解释变量变化多少单位。

[exp_reg_model.py](../sourceCode/exp_reg_model.py)对应于双对数模型，用来度量弹性，衡量解释变量到一个百分比变化导致被解释变量相对变化多少。

[lin_log_model.py](../sourceCode/lin_log_model.py)对应于线性到对数模型，用来度量增长率，衡量解释变量绝对变化一个单位导致被解释变量相对变化多少单位。

[log_lin_model.py](../sourceCode/log_lin_model.py)对应于对数到线性模型，衡量解释变量相对变化一个单位导致被解释变量绝对变化多少单位。

[logit.py](../sourceCode/logit.py)对应于 logit 回归。

[probit.py](../sourceCode/probit.py)对应于 probit 回归。

[Colinearity.py](../sourceCode/Colinearity.py)检验多重共线性。

[White.py](../sourceCode/White.py)检验异方差性。

[Hausman.py](../sourceCode/Hausman.py)检验内生性。

# 调用

## **NOTE**

flask部分由于比较特化，调用难以实现。此处所指的调用为调用sourceCode下的文件

## 调用方式

选择适当的模型，这里以线性回归为例

```python
import sourceCode.lin_log_model as linear
ans = linear.getAns("age",["male","wage"],{"filename":"path-to-file"})
# 得到类似的ans，详见./about_sourceCode.md
figures = linear.showAns(ans)
# 得到二进制保存的t值图片、系数值图片、p值图片
# ....
```
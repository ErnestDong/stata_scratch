# 加入扩展操作

## sourceCode设置

如果要加入新的回归模型foo，需要在sourceCode下新建一个foo.py。在foo.py中必须含有以下三个函数

1. `getAns(dependent: str, independent: list, session: dict) -> dict`

2. `showAns(dependent: str, ans: dict, session: dict) -> str:`

3. `showFigure(ans: dict) -> dict`

### `getAns`

传入参数为被解释变量的名字、解释变量的名字组成的列表与session，传出结果为一个`dict`，其内容被`showAns`与`showFigure`所使用，目的是在调用这两个函数时，不必重复进行回归

### `showAns`

传入参数为`getAns`的返回值，进行处理后返回一个html标签的格式，为展示在/result界面的文字内容

### `showFigure`

传入参数为`getAns`的返回值，进行处理后返回一个字典，内容为{图片名称:二进制保存的图片}

**important**：在画图过程中，flask不能在matplotlib保存图片的同时正常运行，需要以二进制方式保存。e.g.

```python
import base64
from io import BytesIO
import matplotlib.pyplot as plt
# 画图过程省略
buffer = BytesIO()
plt.savefig(buffer)
plot_data = buffer.getvalue()
imb = base64.b64encode(plot_data)
ims = imb.decode()
imd = "data:image/png;base64," + ims
```



## flask设置

需要在文件开始时导入相应的sourceCode文件，并在`commandList`中加入相应名字，即可在flask中应用

# Stata by Python

flask.py 文件利用 flask 框架搭建了一个网页，计划网页的根目录作为首页传递用户上传的文件，/result 返回试验结果,/error 错误处理

提交文件采取csv格式

## Rule

所有文件编码utf-8

sourceCode 文件夹下，存放命令，如 test。由于引用都是相对路径，最好先在/目录下完成之后在放到 sourceCode 文件夹下，以免太乱

test 中的命令要留出来两个，一个是 showAns，参数为因变量(str)，自变量(list)，用于保存下处理的数据，返回值为字符串，内容是展示在结果页的内容，用 html 标签的形式；一个是 create_figure，参数为因变量(str)，自变量(list)，用于处理图片，返回值为 matplotlib.figure

为了在网页中呈现，在 commandList 里面添加命令并 import

## About files

./static/downloads/ans.csv：用于储存结果与下载

./static/uploads/\*：用于储存上传结果

./static/commandhis.txt：用于储存历史命令（美化时加上历史命令窗口）

./static/loadfile.txt：储存文件路径

./static/var.txt：显示选择的因变量自变量，格式为：因变量str，自变量list，读的时候直接读最后两个就好

# TODO
- [ ] TODO1
- [ ] TODO2
- [ ] TODO3

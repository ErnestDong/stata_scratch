# app.py 内容

## 用户登陆

网页根目录是用户登陆，通过若干个在根目录下的 redirect，实现用户输入正确的用户名密码可以进入上传文件页，否则仍留在/目录，或进入[register](../static/re.html)界面，并实现用户没有非法输入。登陆后用户进入/data 目录，密码存放在 passwd 文件，形式是 json

## 提交数据

用户在/data 目录提交 csv 文件，csv 文件存放于/static/username/upload/

之后跳转到/check 目录，清洗数据并查看前 20 行

## 用户操作

/upload 中，用户可以首先获得一个对数据的直观认识，然后选择数据的处理方法与因变量自变量，跳转到/result 目录

## 结果展示

/result 获得数据分析结果与图片，并可下载相应数据，或再次进行分析，或前往/classic 判断古典假定是否成立。

## 其他

`session`中包括了当前登陆的用户名`username`，用户上传文件的绝对路径`filename`当前的回归模型`command`，当前解释变量名字组成的列表`dependent`，被解释变量名字`independent`，错误描述`error`等

数据浏览器位于/browser

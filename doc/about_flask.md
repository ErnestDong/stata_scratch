# flask_with_login内容

## 用户登陆

网页根目录是用户登陆，通过若干个在根目录下的redirect，实现用户输入正确的用户名密码可以进入上传文件页，否则仍留在/目录，或进入[register](../static/re.html)界面，并实现用户没有非法输入。登陆后用户进入/data目录，密码存放在passwd文件，形式是json

## 提交数据

用户在/data目录提交csv文件，csv文件存放于/static/username/upload/，并有一系列的文件支持后续操作，其中

1. loadfile.txt：用户上传的文件列表
2. commandhis.txt：用户的命令历史
3. whoami：当前用户名
4. var.txt：用户选择的因变量（str格式）与自变量（list(*str))的格式

之后跳转到/upload目录

## 用户操作

/upload中，用户可以首先获得一个对数据的直观认识，然后选择数据的处理方法与因变量自变量，跳转到/result目录

## 结果展示

/result获得数据分析结果与图片，并可下载相应数据。

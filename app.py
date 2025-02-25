"""
web app
"""
import os
import pickle
import shutil
from os import path

import pandas as pd
from flask import Flask, redirect, render_template, request
from werkzeug.utils import secure_filename

from sourceCode import (exp_reg_model, lin_log_model, linear_reg,
                        log_lin_model, logit, probit)
from sourceCode.code import decode, encode
from sourceCode.Colinearity import auxiliary_regression
from sourceCode.func import get_corr, gethtml
from sourceCode.Hausman import hausmantest
from sourceCode.White import whitetest

app = Flask(__name__)
commandList = [
    "linear_reg", "exp_reg_model", "log_lin_model", "lin_log_model", "logit",
    "probit"
]
session = {"error": ""}


@app.route("/", methods=['GET', 'POST'])
def passwd():
    """
    login page
    0.0.0.0/: 前往注册界面或上传界面。逻辑见数字
    """
    # logout
    global session
    if "username" in session:
        if os.path.exists("./static/" + session["username"]):
            shutil.rmtree("./static/" + session["username"])
    session = {"error": ""}
    try:
        # 2. 如果已经输入了账户密码，那么在这里检验用户是否已经注册，如果注册就前往/data目录
        """if redirected from /"""
        name = request.form["username"]
        passwd = request.form["passwd"]
        try:
            with open("users_info.pickle", "rb") as f:
                data = decode(pickle.load(f))
        except FileNotFoundError:
            with open("users_info.pickle", "wb") as f:
                data = {'admin': 'admin'}
                pickle.dump(encode(data), f)
        if name not in data:
            """if not registered"""
            return render_template("login.html",
                                   script="alert('Not Registered!')")
        if data[name] != passwd:
            """if password is wrong"""
            return render_template("login.html",
                                   script="alert('Wrong Password!')")
        """if all is well"""
        session["username"] = name
        if os.path.exists("./static/" + name):
            shutil.rmtree("./static/" + name)
        return redirect("data")
    except:
        """if redirected from register"""
        # 3. 如果用户从注册界面回来
        try:
            name = request.form["addUser"]
            passwd = request.form["addpwd"]
            legalstr = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
            if name == "" or passwd == "":
                return render_template(
                    "login.html",
                    script="alert('please check your name or password')")
            for i in name + passwd:
                if i not in legalstr:
                    return render_template(
                        "login.html",
                        script="alert('name or password is illegal')")
            with open("users_info.pickle", "rb") as f:
                data = decode(pickle.load(f))
            if name in data:
                """if username exists"""
                return render_template(
                    "login.html",
                    script="alert('name is registered!Try another name.')")
            data[name] = passwd
            with open("users_info.pickle", "wb") as f:
                pickle.dump(encode(data), f)
            return render_template("login.html", script="alert('registered!')")
        except:
            """if user just clicks the button"""
            # 1. 当用户刚刚打开界面，在login.html里面输入用户密码，并前往 / 目录
            return render_template("login.html", scipt="alert('Input')")


@app.route("/data", methods=['GET', 'POST'])
def upload():
    """
    upload file to ./static/username/uploads/*
    write the filename into ./static/username/loadfile.txt
    jump to upload page to preview data and choose method
    """
    # 上传文件
    # try:
    name = session["username"]
    if not os.path.exists("./static/" + name):
        os.mkdir("./static/" + name)
        os.mkdir("./static/{}/uploads".format(name))
        os.mkdir("./static/{}/downloads".format(name))
    if request.method == 'POST':
        f = request.files["file"]
        base_path = path.abspath(path.dirname(__file__))
        upload_path = path.join(base_path, 'static/{}/uploads/'.format(name))
        if f.filename[-4:] != ".csv":
            session["error"] = "csv needed"
            return redirect("error")
        file_name = upload_path + secure_filename(f.filename)
        session["filename"] = file_name
        f.save(file_name)
        return redirect("check")
    return render_template('upload.html')
    # except Exception:
    #     session["error"] = "please check your data"
    #     return redirect("error")


@app.route("/check", methods=['GET', 'POST'])
def checkResult():
    """
    show about 20 lines of data
    clean data
    """
    # 展示数据的一小部分并选择清洗数据的方法
    try:
        # name = session["username"]
        filename = session["filename"]
        uploadFile = open(filename, "r", encoding="utf-8")
        fileinfo = uploadFile.readlines()[:20]
        fileinfo = gethtml(fileinfo)
        uploadFile.close()
        return render_template("show.html", file=fileinfo)
    except Exception:
        session["error"] = "utf-8 is required"
        return redirect("error")


@app.route("/upload", methods=['GET', 'POST'])
def showResult():
    """
    show corr
    let user to choose command, dependent variable
    """
    try:
        # name = session["username"]
        nullMethod = request.form["isnull"]
        filename = session["filename"]
        # session["command"].append(nullMethod)
        data = pd.read_csv(filename)
        if nullMethod[0] == "d":
            data = data.dropna()
        else:
            data = data.fillna(0)
        commandStr = "<h2 align=\"center\">协方差矩阵</h2>" + get_corr(data)
        data.to_csv(filename, encoding="utf-8")
        commandStr += """
        <div
            style="
              height: 400px;
              width: 8%;
              float: left;"></div><div
            style="
              height: 400px;
              width: 28%;
              float: left;">
            <h2>请选择处理方法</h2>
        """
        title = list(data.columns)
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(
                i, i)
        commandStr += """</div>
        <div
            style="
              height: 400px;
              width: 28%;
              float: left;">
            <h2>请选择因变量</h2>"""
        for i in title:
            commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(
                i, i)
        commandStr += """</div>
        <div
            style="
              width: 28%;
              display: block;
              text-align: left;
              float: right;">
            <h2>请选择自变量</h2>"""
        for i in title:
            commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(
                i, i)
        commandStr += """</div>
        <div
            style="
              height: 400px;
              width: 8%;
              float: left;"></div><br><br>"""
        return render_template("clean.html", command=commandStr)
    except Exception:
        session["error"] = "please check your data"
        return redirect("error")


@app.route("/result", methods=['GET', 'POST'])
def show():
    """
    show the result
    """
    try:
        name = session["username"]
        filename = session["filename"]
        tmp = request.form["command"]
        dependentVariable = request.form["dependent"]
        independentVariable = request.form.getlist("independent")
        session["dependent"] = dependentVariable
        session["independent"] = independentVariable
        independentVariable[-1] = independentVariable[-1]
        try:
            ans = eval(tmp + ".getAns('{}',{},{})".format(
                dependentVariable, independentVariable, session))
            gdnfile = eval(
                tmp +
                ".showAns('{}',{},{})".format(dependentVariable, ans, session))
            content = "<br>"
            figure = eval(tmp + ".showFigure({})".format(ans))
            img = ""
            for i in figure:
                img += """<h3>{}</h3><div><img src="{}"/><br/></div>
                     """.format(i, figure[i])
            data = pd.read_csv(filename)
            commandStr = """<div>
        <form action="/result" method="post">
            <div style="
                    width: 19%;
                    float: left;
                    height: 4px;"></div>
            <div style="
                    width: 27%;
                    float: left;">
                    <h2>请选择处理方法</h2>
                    """
            title = list(data.columns)
            for i in commandList:
                commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(
                    i, i)
            commandStr += """</div>
            <div style="
                width: 27%;
                float: left;">
            <h2>请选择因变量</h2>"""
            for i in title:
                commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(
                    i, i)
            commandStr += """</div>
            <div style="
                    width: 27%;
                    display: block;
                    text-align: left;
                    float: left;">
                <h2>请选择自变量</h2>"""
            for i in title:
                commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(
                    i, i)
            commandStr += """ </div><br /><br/>
                <center><input type="submit" value="next" style="height: 40px; font-size: 24px; color: #000000;"/></center>
            </form></div><br>"""
            session["ans"] = ans
            return """<html>
                        <head>
                            <title>ans</title>
                        </head>
                        <body>
                        <a href="/classic" target="_blank">test hypothesis</a><br><a href="/">退出登录</a>
                        <center>
                            <h1>结果</h1>
                            <p>{}</p>
                            <a href="/datainfo">Click to Download the Result</a>
                            <div>{}</div>
                            {}
                            <a href="./check">preview again</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <a href="./static/{}/uploads/{}">download your raw data</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <a href="./browse" target="_blank">view data</a></center>
                            {}<br>
                        </body>
                        </html>
                    """.format(gdnfile, img, content, name,
                               filename.split('/')[-1], commandStr)
        except:
            session["error"] = "please check your data"
            return redirect("error")
    except:
        session[
            "error"] = "please choose method/independent variable/dependent variable"
        return redirect("error")


@app.route("/classic")
def testClassic():
    # 检验假定：无共线性、同方差、内生性
    script = """<script>
      function help() {
        alert("检验是否满足古典假定");
      }
    </script>"""
    helpfunction = """
    <script>
      function help() {
        alert("检验古典假定是否被满足");
      }
    </script>"""
    html = """
            <!DOCTYPE html>
                <html lang="zh">
                  <head>
                    <meta charset="UTF-8" />
                        {}
                    <title>Test Hypothesis</title>
                  </head>
                  <body>
                    <button onclick="help()">help</button><br><a href="/">退出登录</a>
                    <center><img src="./static/pic/classic.jpg" height="300px" /></center>
                    <br />
                    {}{}{}
                  </body>
                </html>
        """.format(script, auxiliary_regression(session), whitetest(session),
                   hausmantest(session))
    return html


@app.route("/datainfo")
def forDownloads():
    # 下载结果
    try:
        name = session["username"]
        return redirect("/static/{}/downloads/ans.csv".format(name))
    except:
        return """Check Your Data"""


@app.route("/error")
def cerr():
    # 如果有错误，在本页提示错误类型
    html = """
<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="UTF-8" />
    <title>Error</title>
  </head>
    <script>
      alert('{}');
      </script>
      <center>
    An error occured. Please check again.<br>
    <a href="/">return to login page</a><br>
    <img src="/static/pic/logo.png" style="height: 300px;" /></center>
  </body>
</html>
    """.format(session["error"])
    return html


@app.route("/browse")
def data_broser():
    # 数据浏览器，查看全部数据
    filename = session["filename"]
    uploadFile = open(filename, "r", encoding="utf-8")
    fileinfo = uploadFile.readlines()
    fileinfo = gethtml(fileinfo)
    uploadFile.close()
    return """
        <!DOCTYPE html>
        <html lang="zh">
          <head>
            <meta charset="UTF-8" />
            <title>Browse</title>
          </head>
          <body>
            {}
          </body>
        </html>
    """.format(fileinfo)


if __name__ == "__main__":
    app.run()

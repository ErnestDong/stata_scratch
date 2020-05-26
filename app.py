"""
web app
"""
import os
from os import path
import shutil
import pickle
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import pandas as pd
from sourceCode import linear_reg
from sourceCode import exp_reg_model
from sourceCode import log_lin_model
from sourceCode import lin_log_model
from sourceCode import logit
from sourceCode import probit
from sourceCode.Colinearity import auxiliary_regression
from sourceCode.Hausman import hausmantest
from sourceCode.White import whitetest
from sourceCode.func import get_corr, gethtml

app = Flask(__name__)
commandList = [
    "linear_reg", "exp_reg_model", "log_lin_model", "lin_log_model", "logit",
    "probit"
]
session = {"error":""}


@app.route("/", methods=['GET', 'POST'])
def passwd():
    """
    login page
    0.0.0.0/: 前往注册界面或上传界面。逻辑见数字
    """
    try:
        # 2. 如果已经输入了账户密码，那么在这里检验用户是否已经注册，如果注册就前往/data目录
        """if redirected from /"""
        name = request.form["username"]
        passwd = request.form["passwd"]
        try:
            with open("users_info.pickle", "rb") as f:
                data = pickle.load(f)
        except FileNotFoundError:
            with open("users_info.pickle", "wb") as f:
                data = {'admin': 'admin'}
                pickle.dump(data, f)
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
        session["command"] = []
        if os.path.exists("./static/" + name):
            shutil.rmtree("./static/" + name)
        return redirect("data")
    except:
        """if redirected from register"""
        # 3. 如果用户从注册界面回来
        try:
            name = request.form["addUser"]
            passwd = request.form["addpwd"]
            with open("users_info.pickle", "rb") as f:
                data = pickle.load(f)
            if name in data:
                """if username exists"""
                return render_template(
                    "login.html",
                    script="alert('name is registered!Try another name.')")
            data[name] = passwd
            with open("users_info.pickle", "wb") as f:
                pickle.dump(data, f)
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
    try:
        name = session["username"]
        if not os.path.exists("./static/" + name):
            os.mkdir("./static/" + name)
            os.mkdir("./static/{}/uploads".format(name))
            os.mkdir("./static/{}/downloads".format(name))
        if request.method == 'POST':
            f = request.files["file"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path,
                                    'static/{}/uploads/'.format(name))
            file_name = upload_path + secure_filename(f.filename)
            if file_name[-4:] != ".csv":
                return redirect("data")
            session["filename"] = file_name
            f.save(file_name)
            return redirect("check")
        return render_template('upload.html')
    except Exception:
        session["error"] = "please check your data"
        return redirect("error")


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
        session["error"] = "please check your data"
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
        commandStr = "<h2>协方差矩阵为</h2>" + get_corr(data)
        data.to_csv(filename, encoding="utf-8")
        commandStr += """<div
        style="
          height: 400px;
          width: 40%;
          float: left;"><h2>请选择处理方法</h2>
        """
        title = list(data.columns)
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(
                i, i)
        commandStr += """</div><div
        style="
          height: 400px;
          width: 30%;
          float: left;
        "
      ><h2>请选择因变量</h2>"""
        for i in title:
            commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(
                i, i)
        commandStr += """</div><div
        style="
          width: 30%;
          display: block;
          text-align: left;
          float: right;
        "
      ><h2>请选择自变量</h2>"""
        for i in title:
            commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(
                i, i)
        commandStr += "</div><br><a href=./browse target=\"_blank\">view data</a>"
        return render_template("clean.html", command=commandStr)
    except ValueError:
        return redirect("VE")
    except Exception:
        session["error"] = "please check your data"
        return redirect("error")


@app.route("/result", methods=['GET', 'POST'])
def show():
    """
    show the result
    """
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
            img += """<h3>{}</h3><div><img src="{}"/><br/>
                 """.format(i, figure[i])
        data = pd.read_csv(filename)
        commandStr = """<div>
    <form action="/result" method="post">
      <div
                style="
                  height: 400px;
                  width: 40%;
                  float: left;"><h2>请选择处理方法</h2>
                """
        title = list(data.columns)
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(
                i, i)
        commandStr += """</div><div
                style="
                  height: 400px;
                  width: 30%;
                  float: left;
                "
              ><h2>请选择因变量</h2>"""
        for i in title:
            commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(
                i, i)
        commandStr += """</div><div
                style="
                  width: 30%;
                  display: block;
                  text-align: left;
                  float: right;
                "
              ><h2>请选择自变量</h2>"""
        for i in title:
            commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(
                i, i)
        commandStr += """</div><br><a href=./browse target=\"_blank\">view data</a><br />
      <input
        type="submit"
        value="next"
      />
    </form></div><br>"""
        session["ans"] = ans
        return """<html>
                    <head>
                        <title>ans</title>
                    </head>
                    <body>
                    <a href="/classic" target="_blank">test hypothesis</a>
                        <h1>结果</h1>
                        <p>{}</p>
                        <a href="/datainfo">Click to Download the Result</a>
                        <div>{}</div>
                        {}
                        <a href="./check">preview again</a>
                        <a href="./static/{}/uploads/{}">download your raw data</a>
                        <a href="./browse" target="_blank">view data</a>
                        {}<br>
                    </body>
                    </html>
                """.format(gdnfile, img, content, name, filename, commandStr)
    except:
        session["error"] = "please check your data"
        return redirect("error")


@app.route("/classic")
def testClassic():
    # 检验假定：无共线性、同方差、内生性
    script = """<script>
      function help() {
        alert("检验是否满足古典假定");
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
                    <button onclick="help()">help</button>
                    <center><img src="./static/pic/classic.jpg" height="300px" /></center>
                    <br />
                    {}{}{}
                  </body>
                </html>
        """.format(script,auxiliary_regression(session), whitetest(session),
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
            <title>Title</title>
          </head>
          <body>
          <script>
          alert({})
          </script>
            <a href="/check">return to check page</a>
          </body>
        </html>
    """.format(session["error"])
    return html


@app.route("/VE")
def valerr():
    html = """
        <!DOCTYPE html>
        <html lang="zh">
          <head>
            <meta charset="UTF-8" />
            <title>Title</title>
          </head>
          <body>
          <script>
          alert("Please Check Your Data Or Login")
          </script>
            <a href="/">return to login page</a>
          </body>
        </html>
        """
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
            <title>Title</title>
          </head>
          <body>
            {}
          </body>
        </html>
    """.format(fileinfo)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

from sourceCode import test
from sourceCode import tests
from flask import Flask, request, render_template, redirect, Response
from werkzeug.utils import secure_filename
from os import path
import io
import os
import re
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
# functions to be used

def gethtml(lst):
    lenth = len(lst)
    html = "<table border='1'><tr>"
    for line in range(lenth):
        if line == 0:
            tmp = lst[line].split(',')
            for i in tmp:
                html += "<th>{}</th>".format(i)
            html += "</tr>"
        else:
            html += "<tr>"
            tmp = lst[line].split(',')
            for i in tmp:
                html += "<td>{}</td>".format(i)
            html += "</tr>"
    return html + "</table>"

def whoami():
    """
    get who am i
    :return: last username
    """
    rfile = open("whoami", "r", encoding="utf-8")
    name = rfile.readlines()[-1][:-1]
    rfile.close()
    return name


app = Flask(__name__)
commandList = ['test', 'tests']


# add command in commandList


@app.route("/", methods=['GET', 'POST'])
def passwd():
    """
    login page
    """
    try:
        """if redirected from /"""
        name = request.form["username"]
        passwd = request.form["passwd"]
        passwd_file = open("./passwd", "r", encoding='utf-8')
        data = eval(passwd_file.read())
        passwd_file.close()
        if name not in data:
            """if not registered"""
            return render_template("login.html", script="alert('Not Registered!')")
        if data[name] != passwd:
            """if password is wrong"""
            return render_template("login.html", script="alert('Wrong Password!')")
        """if all is well"""
        tmp = open("whoami", "a", encoding="utf-8")
        print(name, file=tmp)
        tmp.close()
        return redirect("data")
    except:
        """if redirected from register"""
        try:
            name = request.form["addUser"]
            passwd = request.form["addpwd"]
            passwd_file = open("./passwd", "r", encoding='utf-8')
            data = eval(passwd_file.read())
            # print(type(data))
            passwd_file.close()
            # print(type(name))
            if name in data:
                """if username exists"""
                return render_template("login.html", script="alert('name is registered!Try another name.')")
            data[name] = passwd
            passwd_file = open("./passwd", "w", encoding='utf-8')
            print(data, file=passwd_file)
            passwd_file.close()
            return render_template("login.html", script="alert('registered!')")
        except:
            """if user just clicks the button"""
            return render_template("login.html", scipt="")


@app.route("/data", methods=['GET', 'POST'])
def upload():
    """
    upload file to ./static/username/uploads/*
    write the filename into ./static/username/loadfile.txt
    jump to upload page to preview data and choose method
    """
    try:
        tmp = open("whoami", "r", encoding="utf-8")
        name = tmp.readlines()[-1][:-1]
        tmp.close()
        if not os.path.exists("./static/" + name):
            os.mkdir("./static/" + name)
            os.mkdir("./static/{}/uploads".format(name))
            os.mkdir("./static/{}/downloads".format(name))
        if request.method == 'POST':
            f = request.files["file"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path, 'static/{}/uploads/'.format(name))
            file_name = upload_path + secure_filename(f.filename)
            uploadFileName = open("./static/{}/loadfile.txt".format(name), "a", encoding="utf-8")
            print(file_name, file=uploadFileName)
            uploadFileName.close()
            f.save(file_name)
            return redirect("check")
        return render_template('upload.html')
    except Exception:
        return redirect("error")


@app.route("/check", methods=['GET', 'POST'])
def checkResult():
    """
    show about 20 lines of data
    let user to choose command, dependent variable 
    """
    name = whoami()
    try:
        with open("./static/{}/loadfile.txt".format(name)) as f:
            filename = f.readlines()[-1][:-1]
        uploadFile = open(filename, "r", encoding="utf-8")
        fileinfo = uploadFile.readlines()[:20]
        uploadFile.close()
        title = re.split(r'[,]', fileinfo[0])
        commandStr = "<h2>please choose your command</h2>"
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(i, i)
        commandStr += "<br><h2>please choose your dependent variable</h2>"
        return render_template("show.html", file=gethtml(fileinfo))
    except Exception:
        return redirect("error")
@app.route("/upload", methods=['GET', 'POST'])
def showResult():
    """
    show about 20 lines of data
    let user to choose command, dependent variable
    """
    name = whoami()
    try:
        nullMethod=request.form["isnull"]
        with open("./static/{}/loadfile.txt".format(name)) as f:
            filename = f.readlines()[-1][:-1]
        data=pd.read_csv(filename)
        if nullMethod[0] == "d":
            data=data.dropna()
        else:
            data=data.fillna(0)
        data.to_csv(filename,encoding="utf-8")
        commandStr = "<h2>please choose your command</h2>"
        title=list(data.columns)
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(i, i)
        commandStr += "<br><h2>please choose your dependent variable</h2>"
        for i in title:
            commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(i, i)
        commandStr += "<br><h2>please choose your independent variable(s)</h2>"
        for i in title:
            commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(i, i)
        return render_template("clean.html", command=commandStr)
    except Exception:
        return redirect("error")




@app.route("/result", methods=['GET', 'POST'])
def show():
    name = whoami()
    """
    show the result
    """
    wfile = open("./static/{}/commandhis.txt".format(name), "a", encoding="utf-8")
    tmp = request.form["command"]
    dependentVariable = request.form["dependent"]
    independentVariable = request.form.getlist("independent")
    independentVariable[-1] = independentVariable[-1]
    varFiles = open("./static/{}/var.txt".format(name), "a", encoding="utf-8")
    print(dependentVariable, '\t', independentVariable, file=varFiles)
    varFiles.close()
    gdnfile = eval(tmp + ".showAns('{}',{},'{}')".format(dependentVariable, independentVariable, name))
    print(tmp, file=wfile)
    wfile.close()
    rfile = open("./static/{}/commandhis.txt".format(name), "r", encoding="utf-8")
    content = rfile.read().replace('\n', '<br>')
    rfile.close()
    return """<html>
                <head>
                    <title>ans</title>
                </head>
                <body>
                    <h1>datainfo</h1>
                    <p>{}</p>
                    <img src="/plot.png"><br>
                    <a href="/datainfo">Click to Download the Result</a>
                    <h2>command history</h2>
                    <p>{}</p>
                    <a href="/check">preview again</a>
                </body>
                </html>
            """.format(gdnfile, content)


@app.route("/plot.png")
def showplot():
    name = whoami()
    with open("./static/{}/var.txt".format(name)) as f:
        lst = f.readlines()[-1][:-1].split('\t')
    with open("./static/{}/commandhis.txt".format(name)) as f:
        command = f.readlines()[-1][:-1]
        fig = eval(command + ".create_figure('{}',{},'{}')".format(lst[0], lst[1], name))
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/datainfo")
def forDownloads():
    name = whoami()
    return redirect("/static/{}/downloads/ans.csv".format(name))


@app.route("/error")
def cerr():
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


if __name__ == "__main__":
    app.run()

from sourceCode import test
from sourceCode import tests
from flask import Flask, request, render_template, redirect, Response
from werkzeug.utils import secure_filename
from os import path
import io
import re
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
app = Flask(__name__)
commandList = ['test', 'tests']
@app.route("/", methods=['GET', 'POST'])
def upload():
    """
    upload file to ./static/uploads/*
    write the filename into ./static/loadfile.txt
    jump to upload page to preview data and choose method
    """
    try:
        if request.method == 'POST':
            f = request.files["file"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path, 'static/uploads/')
            file_name = upload_path + secure_filename(f.filename)
            uploadFileName = open("./static/loadfile.txt", "a", encoding="utf-8")
            print(file_name, file=uploadFileName)
            uploadFileName.close()
            f.save(file_name)
            return redirect("upload")
        return render_template('upload.html')
    except Exception:
        return redirect("error")


@app.route("/upload", methods=['GET', 'POST'])
def showResult():
    """
    show about 50 lines of data
    let user to choose command, dependent variable and independent variable(s)
    """
    try:
        with open("./static/loadfile.txt") as f:
            filename = f.readlines()[-1][:-1]
        uploadFile = open(filename, "r", encoding="utf-8")
        fileinfo = uploadFile.readlines()[:50]
        uploadFile.close()
        title = re.split(r'[,]', fileinfo[0])
        commandStr = "<h2>please choose your command</h2>"
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(i, i)
        commandStr += "<br><h2>please choose your dependent variable</h2>"
        for i in title:
            commandStr += "<input type='radio' value='{}' name='dependent'>{}<br>".format(i, i)
        commandStr += "<br><h2>please choose your independent variable(s)</h2>"
        for i in title:
            commandStr += "<input type='checkbox' value='{}' name='independent'>{}<br>".format(i, i)
        return render_template("show.html", file="<br>".join(fileinfo), command=commandStr)
    except Exception:
        return redirect("error")


@app.route("/result", methods=['GET', 'POST'])
def show():
    """
    show the result
    """
    wfile = open("./static/commandhis.txt", "a", encoding="utf-8")
    tmp = request.form["command"]
    dependentVariable = request.form["dependent"]
    independentVariable = request.form.getlist("independent")
    independentVariable[-1] = independentVariable[-1]
    varFiles = open("./static/var.txt", "a", encoding="utf-8")
    print(dependentVariable, '\t', independentVariable,file=varFiles)
    varFiles.close()
    gdnfile = eval(tmp + ".showAns({},'{}')".format(independentVariable, dependentVariable))
    print(tmp, file=wfile)
    wfile.close()
    rfile = open("./static/commandhis.txt", "r", encoding="utf-8")
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
                </body>
                </html>
            """.format(gdnfile, content)


@app.route("/plot.png")
def showplot():
    with open("./static/var.txt") as f:
        lst = f.readlines()[-2][:-1].split('\t')
    with open("./static/commandhis.txt") as f:
        command = f.readlines()[-1][:-1]
        fig = eval(command + ".create_figure('{}',{})".format(lst[0], lst[1]))
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/datainfo")
def forDownloads():
    return redirect("/static/downloads/ans.csv")


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
          alert("Please Check Your Data!")
          </script>
            <form action="" method="post" enctype="multipart/form-data">
              <input type="file" name="file" />
              <input type="submit" value="upload" />
            </form>
          </body>
        </html>
    """
    return html


if __name__ == "__main__":
    app.run()

from sourceCode import test
from flask import Flask, request, render_template, redirect, Response
from werkzeug.utils import secure_filename
from os import path
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
app = Flask(__name__)
commandList = ['test']
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
    except:
        return redirect("error")


@app.route("/upload", methods=['GET', 'POST'])
def showResult():
    try:
        with open("./static/loadfile.txt") as f:
            filename = f.readlines()[-1][:-1]
        uploadFile = open(filename, "r", encoding="utf-8")
        fileinfo = uploadFile.readlines()[:50]
        uploadFile.close()
        commandStr = ""
        for i in commandList:
            commandStr += "<input type='radio' value='{}' name='command'>{}<br>".format(i, i)
        return render_template("show.html", file="<br>".join(fileinfo), command=commandStr)
    except:
        return redirect("error")


@app.route("/result", methods=['GET', 'POST'])
def show():
    wfile = open("./static/commandhis.txt", "a", encoding="utf-8")
    tmp = request.form["command"]
    gdnfile = eval(tmp+".showAns()")
    print(tmp, file=wfile)
    wfile.close()

    return """<html>
                <head>
                    <title>ans</title>
                </head>
                <body>
                    <h1>datainfo</h1>
                    <p>{}</p>
                    <img src="/plot.png">
                    <a href="/datainfo">Click to Download the Result</a>
                </body>
                </html>
            """.format(gdnfile)


@app.route("/plot.png")
def showplot():
    with open("./static/commandhis.txt") as f:
        command = f.readlines()[-1][:-1]
        fig = eval(command+".create_figure()")
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

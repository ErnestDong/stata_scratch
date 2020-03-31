
from flask import Flask, request,make_response,render_template, redirect
from werkzeug.utils import secure_filename
from os import path
app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def upload():
    try:
        if request.method=='POST':
            f = request.files["file"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path,'static/uploads/')
            file_name = upload_path + secure_filename(f.filename)
            f.save(file_name)
            return redirect("result")
        return render_template('upload.html')
    except:
        return redirect("error")

@app.route("/result")
def getResult():
    return """
0
"""

@app.route("/error")
def cerr():
    html="""
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
      <select name="model_id">
        <option value="0">OLS</option>
        <option value="1">ML</option>
      </select>
      <input type="file" name="file" />
      <input type="submit" value="upload" />
    </form>
  </body>
</html>
    """
    return html
if __name__=="__main__":
    app.run()

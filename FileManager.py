from flask import Flask, request, render_template, send_file, send_from_directory
import os
app = Flask(__name__)

defaultDir = "/var/server"
uploadDir = defaultDir
validLogin = "mylogin"
validPassword = "mypassword"

class dir_info():
   def __init__(self, path, dirList, fileList):
      self.path = path
      self.parentPath = os.path.join(self.path, os.pardir)
      self.dirs = dirList
      self.files = fileList

class item_info():
   def __init__(self, name, link):
      self.name = name
      self.link = link

def make_fs_info(path):
   dirs = []
   files = []

   if path[0] != '/':
    path = "/" + path

   if not os.path.isabs(path):
      path = os.path.join(defaultDir, path)

   for name in os.listdir(path):
      item = os.path.join(path, name)
      relative_name = os.path.join(path, name)
      if os.path.isdir(item):
         dirs.append(item_info(name, f"{name}/"))
      else:
         files.append(item_info(name, f"/download/{relative_name}"))
   return dir_info(path, dirs, files)

@app.route('/')
def render_main_page():
   return render_template('interface.html', dir_info = make_fs_info(defaultDir))

@app.route('/<path:directory>')
def render_page(directory):
   return render_template('interface.html', dir_info = make_fs_info(directory))

@app.route('/download/<path:name>', methods=['GET'])
def download_file(name):
   return send_file("/" + name)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   login = request.form.get("login")
   password = request.form.get("password")
   path = request.form.get("path")

   if not path:
      outputMsg = "No file selected"
   elif login == validLogin and password == validPassword:
      file = request.files['file']
      file.save(os.path.join(uploadDir, path, file.filename))
      outputMsg = 'File uploaded'
   else:
      outputMsg = "Invalid login or password"
   
   outputPath = os.path.join(request.base_url, path)
   return outputMsg + "<br> <a href=\"" + outputPath + "\">Go back</a>"

if __name__ == '__main__':
   app.run(host='0.0.0.0')

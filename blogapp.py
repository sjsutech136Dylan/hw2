import os
from flask import Flask, flash, render_template, request, redirect, url_for, session

UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    if len(session) == 0:
        return render_template("login.html")
    else:
        return redirect(url_for("homepage"))

@app.route("/homepage_action",methods = ["POST","GET"])
def homepage_action():
    if request.method == "POST":
        inputtext = request.form["inputtext"]
        blogfile = open("blog.txt", "a")
        blogfile.write(":"+inputtext+"\n")
        blogfile.close()
    return homepage()

@app.route("/homepage")
def homepage():
    webpage = '''
    <html>
    <head>
    <title>Home</title>
    </head>
    <body>
    <p style='text-align:left;'>
    <h1>Welcome to the TECH 136 blog by LAM
    <span style='float:right;'>
    Username:
    ''' + session["username"] + " <a href='" + url_for("logout") + "'>Logout</a></h1></span></p>"

    webpage += '''
    <form action = 'homepage_action' method = 'post'>
    Enter your comment here:
    <br>
    <textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
    <br>
    <input type = 'submit' value = 'Submit' />
      <a href='/upload'>OR Upload image</a><br>
    '''   
    with open("blog.txt", "r") as blogfile:
        blog = blogfile.read().rstrip()
    blogfile.close()
    bloglist = blog.split("\n")

    for i in range(len(bloglist)-1,-1,-1):
        if bloglist[i][0] == ':':
            webpage += \
            "<br><textarea id='blogtext"+str(i)+"' name='blogtext"+str(i)+"' rows='2' cols='100'>"+bloglist[i][1:]+"</textarea><br>"
        else:
            webpage += "<img src='" + bloglist[i][1:] + "'height=100> <br>"
        
    return webpage

@app.route("/login_action",methods = ["POST","GET"])
def login_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Dummy user validation
        with open("users.txt", "r") as usersfile:
            users = usersfile.read().rstrip()
        usersfile.close()
        userslist = users.split("\n")
        
        for i in range(len(userslist)):
            if username == userslist[i] and password == userslist[i+1]:
                session["username"] = username
                return redirect(url_for("homepage"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

@app.route("/signup_action",methods = ["POST","GET"])
def signup_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("users.txt", "a") as usersfile:
            usersfile.write("\n" + username + "\n")
            usersfile.write(password)
        usersfile.close()
        return render_template("login.html")
    return render_template("signup.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        blogfile = open("blog.txt", "a")
        blogfile.write(";/static/"+file.filename+"\n")
        blogfile.close()
        return redirect(url_for("homepage"))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
        app.run(host="0.0.0.0",port=5002)
from flask import Flask, request, redirect, render_template, session, url_for
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="19831228",
    database="testdb",
    auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

app = Flask(
    __name__,
    static_url_path="/",
)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/member")
def member():
    if "username" not in session:
        return redirect("/")
    else:
        return render_template("member.html", username=session['username'])


@app.route("/error")
def error():
    errormessage = request.args.get("message", "")
    return render_template("error.html", errormessage=errormessage)


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form['name']
    username = request.form['username']
    pin = request.form['pin']

    mycursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
    result = mycursor.fetchall()
    count = len(result)

    if count > 0:
        return redirect(url_for("error", message="帳號已被註冊過"))
    else:
        mycursor.execute(
            "INSERT INTO user (name,username,password) VALUES (%s,%s,%s)", (name, username, pin))
        mydb.commit()
        return render_template("week06.html")


@app.route("/signin", methods=["POST"])
def signin():
    username = request.form['username']
    pin = request.form['pin']

    mycursor.execute(
        f"SELECT * FROM user WHERE username = '{username}'and password='{pin}'")
    result = mycursor.fetchall()
    count = len(result)

    if count > 0:
        session['username'] = request.form['username']
        return redirect("/member")
    else:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))


@ app.route("/signout")
def signout():
    session.pop("username", None)
    return redirect("/")


@app.route("/api/users")
def apiusers():
    username = request.args.get("username", "")

    mycursor.execute(
        f"SELECT * FROM user WHERE username = '{username}'")
    result = mycursor.fetchall()
    count = len(result)

    class create_dict(dict):
        def __init__(self):
            self = dict()

        def add(self, key, value):
            self[key] = value

    userdict = create_dict()

    if count > 0:
        for row in result:
            userdict.add(
                "data", ({"id": row[0], "name": row[1], "username": row[2]}))
            return json.dumps(userdict, indent=4, sort_keys=True, ensure_ascii=False)

    else:
        userdict.add("data", (None))
        return json.dumps(userdict, sort_keys=True, ensure_ascii=False)


app.run(port=3000)

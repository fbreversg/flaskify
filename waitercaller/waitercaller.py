from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import redirect
from flask_login import url_for
from flask_login import request

from mockdbhelper import MockDBHelper
from user import User
from passwordhelper import PasswordHelper

DB = MockDBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxV2342fdsfasQeEXf1Ao2C8upz4addf34s4dasdfasdasbdvsfvass+s+fGQXKsM'
login_manager = LoginManager(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)         # persistencia de login
        return redirect(url_for('account'))
    return home()


@login_manager.user_loader  # handle users with assigned cookie
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/account")
@login_required
def account():
    return "You are logged in."


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=7000, debug=True)

# package level dependencies :
from ndlp import app, db
from ndlp.models import Team, Student, Mentor
from ndlp.views_utils import encrypt_password, send_team_uid_mail, generate_random_int

# flask related dependencies :
from flask import render_template, redirect, url_for, request


# other dependencies :


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user_type = request.form.get('user_type')
        if user_type == 'student':
            return redirect(url_for('student_login'))
        elif user_type == 'mentor':
            return redirect(url_for('mentor_login'))
        elif user_type == 'team':
            return redirect(url_for('team_login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        user_type = request.form.get('user_type')
        if user_type == 'student':
            return redirect(url_for('student_register'))
        elif user_type == 'mentor':
            return redirect(url_for('mentor_register'))
        elif user_type == 'team':
            return redirect(url_for('team_register'))


@app.route("/t_n_c")
def t_n_c():
    return render_template("t_n_c.html")


# flask related dependencies :
from flask_login import logout_user, login_required
from flask import flash


# package level dependencies :
from npl import app, db
from npl.models import Team, Student, Mentor, Project
from npl.views_utils import encrypt_password, generate_random_int

# flask related dependencies :
from flask import render_template, redirect, url_for, request


# other dependencies :


@app.route("/")
@app.route("/home")
def home():
    try:
        projects = Project.query.all()
        num_hard_projs = Project.query.filter_by(category='Hardware').count()
        num_soft_projs = Project.query.filter_by(category='Software').count()
        return render_template("home.html", num_hard_projs=num_hard_projs, num_soft_projs=num_soft_projs, projects=projects)
    except:
        return redirect(url_for('register'))


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


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are Logged Out!", category="danger")
    return redirect(url_for('login'))


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


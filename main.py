from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

import hashlib
import random


app = Flask(__name__)

app.config['SECRET_KEY'] = "my_super_secret_key"

# configuration of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = 'testmail20210101@gmail.com'
app.config['MAIL_USERNAME'] = 'testmail20210101@gmail.com'
app.config['MAIL_PASSWORD'] = 'sbxnibunkcmmcohn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db = SQLAlchemy(app)


mail = Mail(app)


class Users(db.Model):
    user_id = db.Column(db.String(255), primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(25), nullable=False)
    user_institute = db.Column(db.String(255), nullable=False)


class Teams(db.Model):
    team_id = db.Column(db.String(255), primary_key=True)
    team_name = db.Column(db.String(255), unique=True, nullable=False)
    team_institute = db.Column(db.String(255), nullable=False)
    team_leader_email = db.Column(db.String(255), nullable=False)


class Mentors(db.Model):
    mentor_id = db.Column(db.String(255), primary_key=True)
    mentor_name = db.Column(db.String(255), nullable=False)
    mentor_institute = db.Column(db.String(255), nullable=False)
    mentor_email = db.Column(db.String(255), unique=True, nullable=False)


class Admins(db.Model):
    admin_id = db.Column(db.String(255), primary_key=True)
    admin_email = db.Column(db.String(255), unique=True, nullable=False)
    admin_name = db.Column(db.String(255), nullable=False)


# class TeamMembers(db.Model):
    # create a relation b/w users and teams.


class Projects(db.Model):
    project_id = db.Column(db.String(255), primary_key=True)
    project_title = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.String(255), nullable=False)
    project_theme = db.Column(db.String(255))
    project_category = db.Column(db.String(255))
    project_tech_stack = db.Column(db.String(255))
    project_ppt_link = db.Column(db.String(255))
    project_report_link = db.Column(db.String(255), nullable=False)

    # create relation b/w projects, teams, mentors


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/team/<int:team_id>/dashboard")
def team_dashboard(team_id):
    team_dict = Teams.query.get_or_404(team_id)
    return render_template("team_dashboard.html", team_dict=team_dict)


@app.route("/team/<int:team_id>/upload_project")
def upload_project(team_id):
    if request.method == "GET":
        return render_template("upload_project.html", team_id=team_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        team_id = request.form.get("team_id")
        password = request.form.get("password")
        enc_password = encrypt_password(password)
        if enc_password == Teams.query.filter_by(team_id=team_id).first().password:
            print(enc_password == Teams.query.filter_by(team_id=team_id).first().password)
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register(data_dict={}):
    if request.method == "GET":
        return render_template("register.html", data_dict=data_dict)
    elif request.method == "POST":
        team_id = random.randint(1, pow(10, 10))

        while Teams.query.filter_by(team_id=team_id).first():
            team_id = random.randint(1, pow(10, 10))

        team_name = request.form.get("team_name")
        data_dict["team_name"] = team_name
        team_leader_email = request.form.get("team_leader_email")
        data_dict["team_leader_email"] = team_leader_email
        team_mem1_email = request.form.get("team_mem1_email")
        data_dict["team_mem1_email"] = team_mem1_email
        team_mem2_email = request.form.get("team_mem2_email")
        data_dict["team_mem2_email"] = team_mem2_email

        password = request.form.get("password")
        data_dict["password"] = password
        confirm_password = request.form.get("confirm_password")
        data_dict["confirm_password"] = confirm_password
        if Teams.query.filter_by(team_name=team_name).first():
            flash(message="Team Name is Taken", category="warning")
            return redirect(url_for('register', data_dict=data_dict))
        if password == confirm_password:
            enc_password = encrypt_password(password)

            teams = Teams(team_id=team_id,
                          team_name=team_name,
                          team_leader_email=team_leader_email,
                          team_mem1_email=team_mem1_email,
                          team_mem2_email=team_mem2_email,
                          password=enc_password)

            db.session.add(teams)
            db.session.commit()
            send_team_id_mail(team_id, team_leader_email)
            flash(message="You are registered successfully!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('register', data_dict=data_dict))


@app.route("/t_n_c")
def t_n_c():
    return render_template("t_n_c.html")


def encrypt_password(password):
    h = hashlib.new('sha256')
    return h.hexdigest()


def send_team_id_mail(team_id, team_leader_email):
    msg = Message(f"Your Team Id : {team_id}. Use it to login with your password.",
                  recipients=[team_leader_email])
    mail.send(msg)


if __name__ == "__main__":
    app.run(debug=True)

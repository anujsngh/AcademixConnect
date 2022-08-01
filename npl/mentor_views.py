# package level dependencies :
from npl import app, db, mail
from npl.models import Team, Mentor, Project
from npl.views_utils import encrypt_password, send_ack_mail


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/mentor/<mentor_email>/dashboard")
def mentor_dashboard(mentor_email):
    mentor = Mentor.query.filter_by(email=mentor_email).first()
    return render_template("mentor_dashboard.html", mentor=mentor)


@app.route("/mentor/approve/team/<token>", methods=['GET', 'POST'])
def mentor_approve_team(token):
    mentor = Mentor.verify_mail_token(token)
    team_uid = request.args.get('team_uid')
    team = Team.query.filter_by(uid=team_uid).first()

    if mentor is None:
        flash('That is an Invalid or Expired Token', 'warning')
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("mentor_approve_team.html", team=team)

    if request.method == "POST":
        mentor_response = request.form.get('approve_reject_btn')
        if mentor_response == 'approve':
            team.is_approved += 1
            team = Team.query.filter_by(uid=team_uid).first()
            mentor.teams.append(team)
            db.session.commit()

            send_ack_mail(email=team.leader_email, ack_info=f"You are verified by your mentor : {mentor.name}.")

        return redirect(url_for('mentor_dashboard', mentor_email=mentor.email))


@app.route("/mentor/approve/project/<token>", methods=['GET', 'POST'])
def mentor_approve_project(token):
    mentor = Mentor.verify_mail_token(token)
    team_uid = request.args.get('team_uid')
    project_uid = request.args.get('project_uid')

    team = Team.query.filter_by(uid=team_uid).first()
    project = Project.query.filter_by(uid=project_uid).first()

    if mentor is None:
        flash('That is an Invalid or Expired Token', 'warning')
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("mentor_approve_project.html", team=team, project=project)

    if request.method == "POST":
        mentor_response = request.form.get('approve_reject_btn')
        if mentor_response == 'approve':
            project.is_approved += 1
            db.session.commit()
            send_ack_mail(email=team.leader_email, ack_info=f"Your project is verified by your mentor : {mentor.name}.")

        return redirect(url_for('mentor_dashboard', mentor_email=mentor.email))


@app.route("/register/mentor", methods=['GET', 'POST'])
def mentor_register():
    if request.method == "GET":
        return render_template("mentor_register.html")

    elif request.method == "POST":
        mentor_name = request.form.get("mentor_name")
        mentor_email = request.form.get("mentor_email")
        institute_name = request.form.get("institute_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if Mentor.query.filter_by(email=mentor_email).first():
            flash(message="This email is Taken", category="warning")
            return redirect(url_for('mentor_register'))

        if password == confirm_password:
            Mentor.add_mentor(
                mentor_name=mentor_name,
                mentor_email=mentor_email,
                institute_name=institute_name,
                password=password,
            )

            send_ack_mail(email=mentor_email, ack_info="You are successfully registered. You can login with your registered username and password.")

            flash(message="You are registered successfully, check your email for confirmation!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('mentor_register'))


@app.route("/login/mentor", methods=['GET', 'POST'])
def mentor_login():
    if request.method == "GET":
        return render_template("mentor_login.html")
    elif request.method == "POST":
        mentor_email = request.form.get("mentor_email")
        password = request.form.get("password")

        mentor = Mentor.query.filter_by(email=mentor_email).first()

        if mentor and check_password_hash(mentor.password, password):
            flash(message='Login Success!', category='success')
            return redirect(url_for('mentor_dashboard', mentor_email=mentor.email))

        flash('Please check your login details and try again.')
        return redirect(url_for('mentor_login'))

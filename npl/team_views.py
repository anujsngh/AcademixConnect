# package level dependencies :
from npl import app, db, mail
from npl.models import Student, Team, Mentor, Project
from npl.views_utils import encrypt_password, generate_uid, send_ack_mail, send_mentor_approve_team_mail, send_mentor_approve_project_mail

# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/register/team", methods=['GET', 'POST'])
def team_register():
    if request.method == "GET":
        return render_template("team_register.html")
    elif request.method == "POST":
        team_uid = generate_uid()
        while Team.query.filter_by(uid=team_uid).first():
            team_uid = generate_uid()

        team_name = request.form.get("team_name")
        team_institute = request.form.get("team_institute")
        team_leader_email = request.form.get("team_leader_email")

        team_mem1_email = request.form.get("team_mem1_email")
        team_mem2_email = request.form.get("team_mem2_email")
        team_mem3_email = request.form.get("team_mem3_email")

        team_mentor1_email = request.form.get("team_mentor1_email")
        team_mentor1 = Mentor.query.filter_by(email=team_mentor1_email).first()
        team_mentor2_email = request.form.get("team_mentor2_email")
        team_mentor2 = Mentor.query.filter_by(email=team_mentor2_email).first()

        if not team_leader_email:
            flash(message="Team leader is required for a team to register.", category="warning")
            return redirect(url_for('team_register'))

        mentor_count = 0
        if team_mentor1_email or team_mentor2_email:
            if team_mentor1_email:
                mentor_count += 1
            if team_mentor2_email:
                mentor_count += 1
        else:
            flash(message="At least one mentor is required for a team to register.", category="warning")
            return redirect(url_for('team_register'))

        if not ((team_mentor1_email and team_mentor1) or (team_mentor2_email and team_mentor2)):
            flash(message="Mentor with that email doesn't exist.", category="warning")
            return redirect(url_for('team_register'))

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if Team.query.filter_by(name=team_name).first():
            flash(message="Team Name is Taken", category="warning")
            return redirect(url_for('team_register'))

        if password == confirm_password:

            Team.add_team(
                team_uid=team_uid,
                team_name=team_name,
                team_institute=team_institute,
                team_leader_email=team_leader_email,
                password=password,
                team_mem1_email=team_mem1_email,
                team_mem2_email=team_mem2_email,
                team_mem3_email=team_mem3_email,
                mentor_count=mentor_count
            )

            send_ack_mail(email=team_leader_email, ack_info=f"You team is successfully registered. Your Team Id : {team_uid}. You can login with your registered team id and password after your mentor approves your team.")

            if team_mentor1_email:
                send_mentor_approve_team_mail(mentor_email=team_mentor1_email, team_uid=team_uid, team_name=team_name)
            if team_mentor2_email:
                send_mentor_approve_team_mail(mentor_email=team_mentor2_email, team_uid=team_uid, team_name=team_name)

            flash(message="Your team is registered successfully. You can login with your registered team id and password after your mentor approves your team.", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('team_register'))


@app.route("/login/team", methods=['GET', 'POST'])
def team_login():
    if request.method == "GET":
        return render_template("team_login.html")
    elif request.method == "POST":
        team_uid = request.form.get("team_uid")
        password = request.form.get("password")
        team = Team.query.filter_by(uid=team_uid).first()
        if check_password_hash(team.password, password):
            flash(message='Login Success!', category='success')
            return redirect(url_for('team_dashboard', team_uid=team_uid))


@app.route("/team/<string:team_uid>")
@app.route("/team/<string:team_uid>/dashboard")
def team_dashboard(team_uid):
    team = Team.query.filter_by(uid=team_uid).first()
    return render_template("team_dashboard.html", team=team)


@app.route("/team/<string:team_uid>/project/upload", methods=['GET', 'POST'])
def project_upload(team_uid):
    if request.method == "GET":
        return render_template("project_upload.html", team_uid=team_uid)

    elif request.method == "POST":
        team = Team.query.filter_by(uid=team_uid).first()
        project_uid = generate_uid()
        while Project.query.filter_by(uid=project_uid).first():
            project_uid = generate_uid()

        project_title = request.form.get("project_title")
        project_description = request.form.get("project_title")
        project_type = request.form.get("project_type")
        project_theme = request.form.get("project_theme")
        project_category = request.form.get("project_category")
        project_tech_stack = request.form.get("project_tech_stack")
        project_ppt_link = request.form.get("project_ppt_link")
        project_report_link = request.form.get("project_report_link")

        Project.add_project(
            project_uid=project_uid,
            project_title=project_title,
            project_description=project_description,
            project_type=project_type,
            project_theme=project_theme,
            project_category=project_category,
            project_tech_stack=project_tech_stack,
            project_ppt_link=project_ppt_link,
            project_report_link=project_report_link,
            team_id=team.id
        )

        send_ack_mail(
            email=team.leader_email,
            ack_info=f"Your project uploaded successfully with project uid : {project_uid}."
        )

        for mentor in team.mentors:
            send_mentor_approve_project_mail(mentor_email=mentor.email, team_uid=team_uid, team_name=team.name, project_uid=project_uid)

        flash(message="Your project is uploaded successfully and after your mentor's verification it will be listed!", category="success")
        return redirect(url_for('team_dashboard', team_uid=team_uid))


@app.route("/team/<string:team_uid>/project/<string:project_uid>")
def project_details(team_uid, project_uid):
    if request.method == "GET":
        return render_template("project_details.html", team_uid=team_uid, project_uid=project_uid)


@app.route("/team/<string:team_uid>/project/<string:project_uid>/edit")
def project_edit(team_uid, project_uid):
    if request.method == "GET":
        return render_template("project_edit.html", team_uid=team_uid, project_uid=project_uid)

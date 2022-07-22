# package level dependencies :
from ndlp import app, db, mail
from ndlp.models import Student, Team, Mentor, Project
from ndlp.views_utils import encrypt_password, send_team_uid_mail, generate_uid, send_ack_mail

# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash
from flask_mail import Message


def send_mentor_confirm_mail(mentor_email, team_uid, team_name):
    mentor = Mentor.query.filter_by(email=mentor_email).first()
    token = Mentor.get_mail_token(mentor)
    msg = Message("Alert !!!",
                  body=f"Are you mentor of this team, team id: {team_uid}, team name : {team_name}) ? \n To verify it's you, Visit the following link: {url_for('mentor_confirm', token=token, team_uid=[team_uid], _external=True)}",
                  recipients=[mentor_email])
    mail.send(msg)


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
        team_mem1 = Student.query.filter_by(email=team_mem1_email).first()
        team_mem2_email = request.form.get("team_mem2_email")
        team_mem2 = Student.query.filter_by(email=team_mem2_email).first()
        team_mem3_email = request.form.get("team_mem3_email")
        team_mem3 = Student.query.filter_by(email=team_mem3_email).first()

        team_mentor1_email = request.form.get("team_mentor1_email")
        team_mentor2_email = request.form.get("team_mentor2_email")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if Team.query.filter_by(name=team_name).first():
            flash(message="Team Name is Taken", category="warning")
            return redirect(url_for('team_register'))

        if password == confirm_password:
            enc_password = encrypt_password(password)

            team = Team(uid=team_uid,
                        name=team_name,
                        institute=team_institute,
                        leader_email=team_leader_email,
                        password=enc_password,
                    )

            team.members.append(team_mem1)
            team.members.append(team_mem2)
            team.members.append(team_mem3)

            db.session.add(team)
            db.session.commit()

            send_team_uid_mail(team_uid, team_leader_email)
            send_mentor_confirm_mail(mentor_email=team_mentor1_email, team_uid=team_uid, team_name=team_name)
            send_mentor_confirm_mail(mentor_email=team_mentor1_email, team_uid=team_uid, team_name=team_name)

            flash(message="You are registered successfully!", category="success")
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
        enc_password = encrypt_password(password)
        if enc_password == Team.query.filter_by(uid=team_uid).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('team_dashboard', team_uid=team_uid))


@app.route("/team/<string:team_uid>")
@app.route("/team/<string:team_uid>/dashboard")
def team_dashboard(team_uid):
    team_dict = Team.query.filter_by(uid=team_uid).first()
    return render_template("team_dashboard.html", team_dict=team_dict)


@app.route("/mentor/approve_project/<token>", methods=['GET', 'POST'])
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
        return render_template("mentor_project_approve.html", team_dict=team, project_dict=project)

    if request.method == "POST":
        mentor_response = request.form.get('confirm_reject_btn')
        if mentor_response == 'confirm':
            send_ack_mail(email=team.leader_email, ack_info=f"Your project is verified by your mentor : {mentor.name}.")

        return redirect(url_for('team_dashboard', team_uid=team_uid))


def send_mentor_project_approve_mail(mentor_email, team_uid, team_name, project_uid):
    mentor = Mentor.query.filter_by(email=mentor_email).first()
    token = Mentor.get_mail_token(mentor)
    msg = Message("Alert !!!",
                  body=f"Approve or Reject this project, team uid : {team_uid}, team name : {team_name}, project uid : {project_uid}) ? \n Visit the following link: {url_for('mentor_approve_project', token=token, team_uid=[team_uid], project_uid=[project_uid], _external=True)}",
                  recipients=[mentor_email])
    mail.send(msg)


@app.route("/team/<string:team_uid>/project_upload", methods=['GET', 'POST'])
def project_upload(team_uid):
    if request.method == "GET":
        return render_template("project_upload.html", team_uid=team_uid)

    elif request.method == "POST":
        team = Team.query.filter_by(uid=team_uid).first()
        project_uid = generate_uid()
        while Team.query.filter_by(uid=project_uid).first():
            project_uid = generate_uid()

        project_title = request.form.get("project_title")
        project_description = request.form.get("project_title")
        project_theme = request.form.get("project_theme")
        project_category = request.form.get("project_category")
        project_tech_stack = request.form.get("project_tech_stack")
        project_ppt_link = request.form.get("project_ppt_link")
        project_report_link = request.form.get("project_report_link")

        project = Project(
            uid=project_uid,
            title=project_title,
            description=project_description,
            theme=project_theme,
            category=project_category,
            tech_stack=project_tech_stack,
            ppt_link=project_ppt_link,
            report_link=project_report_link,
            team_id=team.id
        )

        db.session.add(project)
        db.session.commit()

        send_ack_mail(
            email=team.leader_email,
            ack_info=f"Your project uploaded successfully with project uid : {project_uid}."
        )

        for mentor in team.mentors:
            send_mentor_project_approve_mail(mentor_email=mentor.email, team_uid=team_uid, team_name=team.name, project_uid=project_uid)

        flash(message="Your project is uploaded successfully and after your mentor's verification it will be listed!", category="success")
        return redirect(url_for('team_dashboard', team_uid=team_uid))


@app.route("/team/<string:team_uid>/project_details/<string:project_uid>")
def project_details(team_uid, project_uid):
    if request.method == "GET":
        return render_template("project_details.html", team_uid=team_uid, project_uid=project_uid)


@app.route("/team/<string:team_uid>/project_edit/<string:project_uid>")
def project_edit(team_uid, project_uid):
    if request.method == "GET":
        return render_template("project_edit.html", team_uid=team_uid, project_uid=project_uid)

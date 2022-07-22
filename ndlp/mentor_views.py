# package level dependencies :
from ndlp import app, db, mail
from ndlp.models import Team, Mentor
from ndlp.views_utils import encrypt_password, send_register_confirm_mail, send_ack_mail


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash
from flask_mail import Message


@app.route("/mentor/<mentor_email>/dashboard")
def mentor_dashboard(mentor_email):
    return render_template("mentor_dashboard.html")


@app.route("/mentor/confirm/<token>", methods=['GET', 'POST'])
def mentor_confirm(token):
    mentor = Mentor.verify_mail_token(token)
    team_uid = request.args.get('team_uid')
    if mentor is None:
        flash('That is an Invalid or Expired Token', 'warning')
        return redirect(url_for('home'))

    if request.method == "GET":
        team = Team.query.filter_by(uid=team_uid).first()
        team_dict = {
            'team_uid': team_uid,
            'team_name': team.name
        }
        return render_template("mentor_confirm.html", team_dict=team_dict)

    if request.method == "POST":
        mentor_response = request.form.get('confirm_reject_btn')
        if mentor_response == 'confirm':
            team = Team.query.filter_by(uid=team_uid).first()
            mentor.teams.append(team)

            db.session.commit()

            send_ack_mail(email=team.leader_email, ack_info=f"You are verified by your mentor : {mentor.name}.")

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
            enc_password = encrypt_password(password)

            mentor = Mentor(name=mentor_name,
                            email=mentor_email,
                            institute=institute_name,
                            password=enc_password,
                        )

            db.session.add(mentor)
            db.session.commit()
            send_register_confirm_mail(mentor_email)
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
        enc_password = encrypt_password(password)
        if enc_password == Mentor.query.filter_by(email=mentor_email).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))

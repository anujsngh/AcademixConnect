# package level dependencies :
from ndlp import app, db
from ndlp.models import Team
from ndlp.views_utils import encrypt_password, send_team_id_mail, generate_random_int

# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash


@app.route("/register/team", methods=['GET', 'POST'])
def team_register(data_dict=None):
    if data_dict is None:
        data_dict = {}
    if request.method == "GET":
        return render_template("team_register.html", data_dict=data_dict)
    elif request.method == "POST":
        team_id = generate_random_int()

        while Team.query.filter_by(team_id=team_id).first():
            team_id =  generate_random_int()

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
        if Team.query.filter_by(team_name=team_name).first():
            flash(message="Team Name is Taken", category="warning")
            return redirect(url_for('team_register', data_dict=data_dict))
        if password == confirm_password:
            enc_password = encrypt_password(password)

            teams = Team(id=team_id,
                          name=team_name,
                          leader_email=team_leader_email,
                          mem1_email=team_mem1_email,
                          mem2_email=team_mem2_email,
                          password=enc_password)

            db.session.add(teams)
            db.session.commit()
            send_team_id_mail(team_id, team_leader_email)
            flash(message="You are registered successfully!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('team_register', data_dict=data_dict))


@app.route("/login/team", methods=['GET', 'POST'])
def team_login():
    if request.method == "GET":
        return render_template("team_login.html")
    elif request.method == "POST":
        team_id = request.form.get("team_id")
        password = request.form.get("password")
        enc_password = encrypt_password(password)
        if enc_password == Team.query.filter_by(team_id=team_id).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))


@app.route("/team/<int:team_id>/dashboard")
def team_dashboard(team_id):
    team_dict = Team.query.get_or_404(team_id)
    return render_template("team_dashboard.html", team_dict=team_dict)


@app.route("/team/<int:team_id>/project_upload")
def project_upload(team_id):
    if request.method == "GET":
        return render_template("project_upload.html", team_id=team_id)


@app.route("/team/<int:team_id>/project_details/<int:project_id>")
def project_details(team_id, project_id):
    if request.method == "GET":
        return render_template("project_details.html", team_id=team_id, project_id=project_id)


@app.route("/team/<int:team_id>/project_edit/<int:project_id>")
def project_edit(team_id, project_id):
    if request.method == "GET":
        return render_template("project_edit.html", team_id=team_id, project_id=project_id)


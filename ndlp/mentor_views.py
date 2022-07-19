# package level dependencies :
from ndlp import app, db
from ndlp.models import Team, Mentor
from ndlp.views_utils import encrypt_password


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash


@app.route("/register/mentor", methods=['GET', 'POST'])
def mentor_register(data_dict=None):
    if data_dict is None:
        data_dict = {}
    if request.method == "GET":
        return render_template("mentor_register.html", data_dict=data_dict)


@app.route("/login/mentor", methods=['GET', 'POST'])
def mentor_login():
    if request.method == "GET":
        return render_template("mentor_login.html")
    elif request.method == "POST":
        mentor_email = request.form.get("mentor_email")
        password = request.form.get("password")
        enc_password = encrypt_password(password)
        if enc_password == Team.query.filter_by(email=mentor_email).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))

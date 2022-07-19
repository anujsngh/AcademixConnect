# package level dependencies :
from ndlp import app, db
from ndlp.models import Team, Student
from ndlp.views_utils import encrypt_password, send_team_id_mail


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash


@app.route("/register/student", methods=['GET', 'POST'])
def student_register(data_dict=None):
    if data_dict is None:
        data_dict = {}
    if request.method == "GET":
        return render_template("student_register.html", data_dict=data_dict)
    elif request.method == "POST":
        student_name = request.form.get("student_name")
        data_dict["student_name"] = student_name
        student_email = request.form.get("student_email")
        data_dict["student_email"] = student_email

        password = request.form.get("password")
        data_dict["password"] = password
        confirm_password = request.form.get("confirm_password")
        data_dict["confirm_password"] = confirm_password

        institute_name = request.form.get("institute_name")
        data_dict["institute_name"] = institute_name

        if Team.query.filter_by(student_email=student_email).first():
            flash(message="This email is Taken", category="warning")
            return redirect(url_for('team_register', data_dict=data_dict))

        if password == confirm_password:
            enc_password = encrypt_password(password)

            student = Student(name=student_name,
                            email=student_email,
                            institute=institute_name,
                            password=enc_password,
                        )

            db.session.add(student)
            db.session.commit()
            send_team_id_mail(student_email)
            flash(message="You are registered successfully, check your email for confirmation!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('student_register', data_dict=data_dict))


@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == "GET":
        return render_template("student_login.html")
    elif request.method == "POST":
        student_email = request.form.get("student_email")
        password = request.form.get("password")
        enc_password = encrypt_password(password)
        if enc_password == Team.query.filter_by(email=student_email).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))

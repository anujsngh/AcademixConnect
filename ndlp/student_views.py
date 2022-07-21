# package level dependencies :
from ndlp import app, db
from ndlp.models import Team, Student
from ndlp.views_utils import encrypt_password, send_register_confirm_mail


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash


@app.route("/register/student", methods=['GET', 'POST'])
def student_register():
    if request.method == "GET":
        return render_template("student_register.html")

    elif request.method == "POST":
        student_name = request.form.get("student_name")
        student_email = request.form.get("student_email")
        institute_name = request.form.get("institute_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if Student.query.filter_by(email=student_email).first():
            flash(message="This email is Taken", category="warning")
            return redirect(url_for('student_register'))

        if password == confirm_password:
            enc_password = encrypt_password(password)

            student = Student(name=student_name,
                            email=student_email,
                            institute=institute_name,
                            password=enc_password,
                        )

            db.session.add(student)
            db.session.commit()
            send_register_confirm_mail(student_email)
            flash(message="You are registered successfully, check your email for confirmation!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('student_register'))


@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == "GET":
        return render_template("student_login.html")
    elif request.method == "POST":
        student_email = request.form.get("student_email")
        password = request.form.get("password")
        enc_password = encrypt_password(password)
        if enc_password == Student.query.filter_by(email=student_email).first().password:
            flash(message='Login Success!', category='success')
            return redirect(url_for('home'))

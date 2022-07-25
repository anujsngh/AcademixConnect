# package level dependencies :
from npl import app, db
from npl.models import Team, Student, Project


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash


@app.route("/project/<project_uid>/dashboard")
def project_dashboard(project_uid):
    project = Project.query.filter_by(uid=project_uid).first()
    return render_template("project_dashboard.html", project=project)

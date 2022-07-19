# package level dependencies :
from ndlp import db

# other dependencies :
import datetime


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    teams = db.relationship('Team', backref='mentors')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


team_member = db.Table('team_member',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
                )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    leader_email = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    mentor = db.Column(db.Integer, db.ForeignKey('mentor.id'))

    members = db.relationship('User', secondary=team_member, backref='members')

    projects = db.relationship('Project', backref='projects')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(255))
    category = db.Column(db.String(255))
    tech_stack = db.Column(db.String(255))
    ppt_link = db.Column(db.String(255))
    report_link = db.Column(db.String(255), nullable=False)

    team = db.Column(db.Integer, db.ForeignKey('team.id'))


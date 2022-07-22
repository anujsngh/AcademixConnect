# flask related dependencies :
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# package level dependencies :
from ndlp import db, app

# other dependencies :
import datetime


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


team_mentor = db.Table('team_mentor',
                    db.Column('mentor_id', db.Integer, db.ForeignKey('mentor.id')),
                    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
                )


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    teams = db.relationship('Team', secondary=team_mentor, backref='mentors')

    def get_mail_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'mentor_id': self.id}).decode('utf-8')


    def verify_mail_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            mentor_id = s.loads(token)['mentor_id']
        except:
            return None
        return Mentor.query.get(mentor_id)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


team_member = db.Table('team_member',
                    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
                )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    leader_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    members = db.relationship('Student', secondary=team_member, backref='teams')

    projects = db.relationship('Project', backref='team')


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

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    #todo: add is_approved and is_verified


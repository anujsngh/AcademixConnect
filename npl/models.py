# flask related dependencies :
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash
from flask_login import UserMixin


# package level dependencies :
from npl import db, app


# other dependencies :
import datetime



class Theme:
    pass


class Institute:
    pass


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    institute = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def add_student(student_name, student_email, institute_name, password):
        student = Student(
            name=student_name,
            email=student_email,
            institute=institute_name,
            password=generate_password_hash(password, "sha256"),
        )

        db.session.add(student)
        db.session.commit()

    def __repr__(self):
        return f"Student({self.name}, {self.email}, {self.institute})"


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

    @staticmethod
    def add_mentor(mentor_name, mentor_email, institute_name, password):
        mentor = Mentor(
                    name=mentor_name,
                    email=mentor_email,
                    institute=institute_name,
                    password=generate_password_hash(password, "sha256"),
                )

        db.session.add(mentor)
        db.session.commit()

    def __repr__(self):
        return f"Mentor({self.name}, {self.email}, {self.institute})"

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

    def add_admin(self):
        pass

    def __repr__(self):
        return f"Admin({self.name}, {self.email})"


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
    is_approved = db.Column(db.Integer, default=0)
    mentor_count = db.Column(db.Integer, nullable=False)

    members = db.relationship('Student', secondary=team_member, backref='teams')

    projects = db.relationship('Project', backref='team')

    @staticmethod
    def add_team(team_uid, team_name, team_institute, team_leader_email, password, team_mem1_email, team_mem2_email, team_mem3_email, mentor_count):

        if team_mem1_email:
            team_mem1 = Student.query.filter_by(email=team_mem1_email).first()
            if not team_mem1:
                Student.add_student(
                    student_name="default",
                    student_email=team_mem1_email,
                    institute_name="default",
                    password="default"
                )

        if team_mem2_email:
            team_mem2 = Student.query.filter_by(email=team_mem2_email).first()
            if not team_mem2:
                Student.add_student(
                    student_name="default",
                    student_email=team_mem2_email,
                    institute_name="default",
                    password="default"
                )

        if team_mem3_email:
            team_mem3 = Student.query.filter_by(email=team_mem3_email).first()
            if not team_mem3:
                Student.add_student(
                    student_name="default",
                    student_email=team_mem3_email,
                    institute_name="default",
                    password="default"
                )

        team = Team(
            uid=team_uid,
            name=team_name,
            institute=team_institute,
            leader_email=team_leader_email,
            password=generate_password_hash(password, "sha256"),
            mentor_count=mentor_count
        )

        team_leader = Student.query.filter_by(email=team_leader_email).first()
        team.members.append(team_leader)
        if team_mem1_email:
            team.members.append(team_mem1)
        if team_mem2_email:
            team.members.append(team_mem2)
        if team_mem3_email:
            team.members.append(team_mem3)

        db.session.add(team)
        db.session.commit()

    def __repr__(self):
        return f"Team({self.name}, {self.institute}, {self.leader_email})"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(255))
    category = db.Column(db.String(255))
    tech_stack = db.Column(db.String(255))
    ppt_link = db.Column(db.String(255))
    report_link = db.Column(db.String(255), nullable=False)
    youtube_link = db.Column(db.String(255))
    demo_link = db.Column(db.String(255))
    is_approved = db.Column(db.Integer, default=0)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))  # foreign key

    @staticmethod
    def add_project(project_uid, project_title, project_description, project_type, project_theme, project_category, project_tech_stack, project_ppt_link, project_report_link, project_youtube_link, project_demo_link, team_id):
        project = Project(
            uid=project_uid,
            title=project_title,
            description=project_description,
            type=project_type,
            theme=project_theme,
            category=project_category,
            tech_stack=project_tech_stack,
            ppt_link=project_ppt_link,
            report_link=project_report_link,
            youtube_link=project_youtube_link,
            demo_link=project_demo_link,
            team_id=team_id
        )

        db.session.add(project)
        db.session.commit()

    def __repr__(self):
        return f"Project({self.title}, {self.description}, {self.type})"


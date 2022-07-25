# package level dependencies :
from npl import mail
from npl.models import Mentor

# flask related dependencies :
from flask_mail import Message
from flask import url_for

# other dependencies :
import hashlib
import random
import secrets
import string


def generate_uid():
    # initializing size of string
    N = 16

    # using random.choices()
    # generating random strings
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(N))
    return str(res)


def generate_random_int():
    return random.randint(1, pow(10, 10))


def encrypt_password(password):
    h = hashlib.new('sha256')
    return h.hexdigest()


def send_mentor_approve_team_mail(mentor_email, team_uid, team_name):
    mentor = Mentor.query.filter_by(email=mentor_email).first()
    token = Mentor.get_mail_token(mentor)
    msg = Message("Alert !!!",
                  body=f"Are you mentor of this team, team id: {team_uid}, team name : {team_name}) ? \n To verify it's you, Visit the following link: {url_for('mentor_approve_team', token=token, team_uid=[team_uid], _external=True)}",
                  recipients=[mentor_email])
    mail.send(msg)


def send_mentor_approve_project_mail(mentor_email, team_uid, team_name, project_uid):
    mentor = Mentor.query.filter_by(email=mentor_email).first()
    token = Mentor.get_mail_token(mentor)
    msg = Message("Alert !!!",
                  body=f"Approve or Reject this project, team uid : {team_uid}, team name : {team_name}, project uid : {project_uid}) ? \n Visit the following link: {url_for('mentor_approve_project', token=token, team_uid=[team_uid], project_uid=[project_uid], _external=True)}",
                  recipients=[mentor_email])
    mail.send(msg)


def send_ack_mail(email, ack_info):
    msg = Message("Acknowledgement", body=ack_info, recipients=[email])
    mail.send(msg)


if __name__ == '__main__':
    generate_uid()

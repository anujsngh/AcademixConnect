# package level dependencies :
from ndlp import mail

# flask related dependencies :
from flask_mail import Message

# other dependencies :
import hashlib
import random


def generate_random_int():
    return random.randint(1, pow(10, 10))


def encrypt_password(password):
    h = hashlib.new('sha256')
    return h.hexdigest()


def send_team_id_mail(team_id, team_leader_email):
    msg = Message(f"Your Team Id : {team_id}. Use it to login with your password.",
                  recipients=[team_leader_email])
    mail.send(msg)


def send_register_confirm_mail(student_email):
    msg = Message(f"You are successfully registered. You can login with your registered username and password.",
                  recipients=[student_email])
    mail.send(msg)


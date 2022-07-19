# NDLP : National Digital Library of Projects. #


# flask related dependencies :
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


# initiating app object
app = Flask(__name__)


# configuring app object
if app.config["ENV"] == 'production':
    app.config.from_object('config.ProductionConfig')
elif app.config["ENV"] == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif app.config["ENV"] == 'testing':
    app.config.from_object('config.TestingConfig')


# initiating db object
db = SQLAlchemy(app)


# initiating mail object
mail = Mail(app)


from ndlp import models

from ndlp import views
from ndlp import student_views
from ndlp import mentor_views
from ndlp import team_views
from ndlp import project_views

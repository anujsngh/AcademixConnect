# NDLP : National Digital Library of Projects. #  - 0
# NPL : National Project's Library #


# flask related dependencies :
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


# initiating app object
app = Flask(__name__)


# configuring app object
app.config["ENV"] = 'development'

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


from npl import models

from npl import views
from npl import student_views
from npl import mentor_views
from npl import team_views
from npl import project_views

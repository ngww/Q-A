from application import db
from application.models import Questions, Answers, Users

db.drop_all()
db.create_all()

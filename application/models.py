from application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    questions = db.relationship('Questions', backref='creator', lazy=True)
    answers = db.relationship('Answers', backref='author', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Username: ', self.username, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name
        ])

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ask = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answers = db.relationship('Answers', backref='qans', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', self.user_id, '\r\n',
            'Question: ', self.ask
        ])

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ask_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    questions = db.relationship('Questions', backref='ansq', lazy=True)

    def __repr__(self):
        return ''.join([
            'Question ID: ', self.ask_id, '\r\n',
            'Answer: ', self.ans
        ])

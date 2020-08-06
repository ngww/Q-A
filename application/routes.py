from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt

from flask_login import login_user, current_user, login_required, logout_user
from application.forms import RegistrationForm, LoginForm, QuestionForm, AnswerForm, UpdateQuestionForm
from application.models import Questions, Users, Answers

@app.route('/')
@app.route('/home')
def home():
    questionData = Questions.query.all()
    return render_template('home.html', title='Home', questions=questionData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=hash_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('question'))
    return render_template('register.html', title='Register', form=form)

@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = QuestionForm()
    if form.validate_on_submit():
        questionData = Questions(
            ask = form.ask.data,
            creator = current_user
        )

        db.session.add(questionData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('question.html', title='Questions', form=form)

@app.route('/answers/<id>', methods=['GET', 'POST'])
@login_required
def answer(id):
    form = AnswerForm()
    question = Questions.query.filter_by(id=id).first()
    if form.validate_on_submit():
        answerData = Answers(
            ans = form.ans.data,
            author = current_user,
            qans = question
        )

        db.session.add(answerData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('answers.html', title='Answers', form=form, question=question)

@app.route('/response')
def response():
    answerData = Answers.query.all()
    return render_template('response.html', title='Answers', answers=answerData)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account/<id>')
@login_required
def account(id):
    questions = Questions.query.filter_by(user_id=id).all()
    return render_template('account.html', title='Account', questions=questions)

@app.route("/update/<id>", methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateQuestionForm()
    question = Questions.query.filter_by(id=id).first()
    if form.validate_on_submit():
        question.ask = form.ask.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.ask.data = question.ask
    return render_template('update.html', title='Update', form=form)

@app.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def question_delete(id):
    question = Questions.query.filter_by(id=id).first()
    answers = Answers.query.filter_by(ask_id=id)
    for answer in answers:
        db.session.delete(answer)
    db.session.delete(question)
    return redirect(url_for('account'))

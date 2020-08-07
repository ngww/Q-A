import unittest

from flask import url_for
from flask_testing import TestCase
from flask_login import login_user, current_user, logout_user, login_required

from application import app, db, bcrypt
from application.models import Users, Questions, Answers
from os import getenv

class TestBase(TestCase):

    def create_app(self):

        # pass in configurations for test database
        config_name = 'testing'
        app.config.update(SQLALCHEMY_DATABASE_URI=getenv('TEST_DB_URI'),
                SECRET_KEY=getenv('TEST_SECRET_KEY'),
                WTF_CSRF_ENABLED=False,
                DEBUG=True
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        hashed_pw = bcrypt.generate_password_hash('password1')
        admin = Users(first_name="admin", last_name="admin", username="admin", password=hashed_pw)

        # create test non-admin user
        hashed_pw_2 = bcrypt.generate_password_hash('password2')
        test = Users(first_name="test", last_name="user", username="test", password=hashed_pw_2)

        # create a test entry for questions
        question = Questions(ask="what clolour is the sky", user_id=1)

        # create a test entry for answers
        answer = Answers(ans="Blue", user_id=2, ask_id=1)

        # save users to database
        db.session.add(admin)
        db.session.add(test)
        db.session.add(question)
        db.session.add(answer)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_questions_view(self):
        self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
        response = self.client.get(url_for('question'))
        self.assertIn(b'Question', response.data)

    def test_answers_view(self):
        self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
        response = self.client.get('/answers/1')
        self.assertIn(b'Answer', response.data)

    def test_account_view(self):
        self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
        response = self.client.get('/account/1')
        self.assertIn(b'Account', response.data)

    def test_respose_view(self):
        self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
        response = self.client.get(url_for('response'))
        self.assertIn(b'Blue', response.data)

class TestPosts(TestBase):

    def test_add_question(self):
        """
        Test that when I add a new post, I am redirected to the homepage with the new post visible
        """
        with self.client:
            self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
            response = self.client.post(
                '/question',
                data=dict(
                    ask="how are you"
                ),
                follow_redirects=True
            )
            self.assertIn(b'how are you', response.data)

    def test_add_answer(self):
        with self.client:
            self.client.post(url_for('login'), data=dict(username="test", password="password2"), follow_redirects=True)
            response = self.client.post(
                '/answers/1',
                data=dict(
                    ans="purple"
                ),
                follow_redirects=True
            )
            answer = self.client.get(url_for('response'))
            # checks is user is redirected to home page
            self.assertIn(b'Home', response.data)
            self.assertIn(b'purple', answer.data)
            

    def test_update_question(self):
        with self.client:
            self.client.post(url_for('login'), data=dict(username="admin", password="password1"), follow_redirects=True)
            response = self.client.post(
                '/update/1',
                data=dict(
                    ask="What colour is the sky?"
                ),
                follow_redirects=True
            )
            self.assertNotIn(b'what clolour is the sky', response.data)
            self.assertIn(b'What colour is the sky?', response.data)

class TestLogin(TestBase):

    def test_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(
                    username="admin",
                    password="password1"
                ),
                follow_redirects=True
            )
            self.assertEqual(current_user.username, "admin")

    def test_logout(self):
        with self.client:
            response = self.client.get(
                '/logout',
                follow_redirects=True
            )
            self.assertFalse(current_user.is_authenticated)

    def test_register(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    first_name="Thembi",
                    last_name="Ngwenya",
                    username="ngw",
                    password="password3",
                    confirm_password="password3"
                ),
                follow_redirects=True
            )
            self.assertTrue(response.status_code, 200)

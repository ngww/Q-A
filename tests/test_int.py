import unittest
import time
from flask import url_for
from urllib.request import urlopen

from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db, bcrypt
from application.models import Users, Questions, Answers

# Set test variables for test admin user
test_admin_first_name = "admin"
test_admin_last_name = "admin"
test_admin_username = "admin"
test_admin_password = "password1"
test_question = "How are you?"
test_answer = "Great"
test_update_question = "What colour is the sky?"

class TestBase(LiveServerTestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = str(getenv('TEST_DB_URI'))
        app.config['SECRET_KEY'] = getenv('TEST_SECRET_KEY')
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        print("--------------------------NEXT-TEST----------------------------------------------")
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="/home/ngww95/chromedriver", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create dummy info that will be added into database
        hashed_pw = bcrypt.generate_password_hash('password2')
        test = Users(first_name="test", last_name="user", username="test", password=hashed_pw)

        hashed_pw_2 = bcrypt.generate_password_hash('password3')
        tester = Users(first_name="tester", last_name="user", username="tester", password=hashed_pw_2)

        question = Questions(ask="what clolour is the sky", user_id=1)
        answer = Answers(ans="Blue", user_id=2, ask_id=1)

        db.session.add(test)
        db.session.add(tester)
        db.session.add(question)
        db.session.add(answer)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()
        print("--------------------------END-OF-TEST----------------------------------------------\n\n\n-------------------------UNIT-AND-SELENIUM-TESTS----------------------------------------------")

    def test_server_is_up_and_running(self):
        response = urlopen("http://localhost:5000")
        self.assertEqual(response.code, 200)

class TestWebApp(TestBase):

    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be
        redirected to the login page
        """

        # Click register menu link
        self.driver.find_element_by_xpath("/html/body/div[2]/a[2]").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert url_for('login') in self.driver.current_url

    def test_login(self):
        self.driver.find_element_by_xpath("/html/body/div[2]/a[2]").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        assert url_for('question') in self.driver.current_url

    def test_response(self):
        self.driver.find_element_by_xpath('/html/body/div[3]/h2/a').click()
        time.sleep(1)

        assert url_for('response') in self.driver.current_url

    def test_ask(self):
        self.driver.find_element_by_xpath("/html/body/div[2]/a[2]").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath("/html/body/div[2]/a[2]").click()
        time.sleep(1)

        # Fill in question form
        self.driver.find_element_by_xpath('//*[@id="ask"]').send_keys(test_question)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        
        assert url_for('home') in self.driver.current_url


    def test_answer_no_login(self):
        self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/span[2]/a").click()
        time.sleep(1)

        assert url_for('login') in self.driver.current_url

    def test_answer_login(self):
        self.driver.find_element_by_xpath("/html/body/div[2]/a[2]").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="ask"]').send_keys(test_question)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/span[2]/a").click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="ans"]').send_keys(test_answer)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        assert url_for('home') in self.driver.current_url

if __name__ == '__main__':
    unittest.main(port=5000)

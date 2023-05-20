from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from apps.controller import controller
from apps.models import *
import unittest
from selenium.webdriver.common.by import By
from apps import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        # Start the web browser
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Quit the web browser
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.driver.quit()


    def test_register(self):

        # Register a Valid User 
        self.driver.get("http://localhost:5000/register")

        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("testuser")

        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("testuser@example.com")

        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")

        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()

        # Wait for the user to be created
        time.sleep(2)

        # Check if the user was registered successfully
        assert self.driver.current_url == "http://localhost:5000/index"

        # Click the logout button
        logout_button = self.driver.find_element(By.NAME, "logout")
        logout_button.click()

        # Username already registered
        self.driver.get("http://localhost:5000/register")
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("testuser")
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("testuser@example.com")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()
        time.sleep(2)
        assert "Username already registered" in self.driver.page_source

        # Email already registered
        self.driver.get("http://localhost:5000/register")
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("testuser1")
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("testuser@example.com")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()
        time.sleep(2)
        assert "Email already registered" in self.driver.page_source

        # Email field can not be empty
        self.driver.get("http://localhost:5000/register")
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("testuser1")
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()
        time.sleep(2)
        assert "Email field can not be empty" in self.driver.page_source

        # Not a Valid Email
        self.driver.get("http://localhost:5000/register")
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("testuser1")
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("testuser")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()
        time.sleep(2)
        assert "Not a Valid Email" in self.driver.page_source

        # Username field can not be empty
        self.driver.get("http://localhost:5000/register")
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("")
        email_field = self.driver.find_element(By.NAME, "email")
        email_field.send_keys("testuser1@example.com")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        submit_button = self.driver.find_element(By.NAME, "register")
        submit_button.click()
        time.sleep(2)
        assert "Username field can not be empty" in self.driver.page_source

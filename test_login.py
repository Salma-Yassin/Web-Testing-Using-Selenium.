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


    def test(self):

        # Register a user First 
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
        # Wait for the user to be logged out
        time.sleep(2)
        # Check if the user was logged out successfully
        assert self.driver.current_url == "http://localhost:5000/login"
        self.driver.get("http://localhost:5000/login")

        # Check Log in successfully 
        username_field = self.driver.find_element(By.NAME, "Username")
        username_field.send_keys("testuser")
        password_field = self.driver.find_element(By.NAME, "Password")
        password_field.send_keys("testpassword")

        submit_button = self.driver.find_element(By.NAME, "login")
        submit_button.click()
        time.sleep(2)

        self.assertEqual(self.driver.current_url, "http://localhost:5000/index")
        logout_button = self.driver.find_element(By.NAME, "logout")
        logout_button.click()
        time.sleep(2)
        # Check if the user was logged out successfully
        assert self.driver.current_url == "http://localhost:5000/login"

        self.driver.get("http://localhost:5000/login")

        # Wrong password Test case 
        username_field = self.driver.find_element(By.NAME, "Username")
        username_field.send_keys("testuser")

        password_field = self.driver.find_element(By.NAME, "Password")
        password_field.send_keys("testpassword1")

        # Submit the login form
        submit_button = self.driver.find_element(By.NAME, "login")
        submit_button.click()

        time.sleep(2)

        assert "Wrong password" in self.driver.page_source

        # ' User not found or wrong user'

        # Wrong password Test case 
        username_field = self.driver.find_element(By.NAME, "Username")
        username_field.send_keys("testuser1")

        password_field = self.driver.find_element(By.NAME, "Password")
        password_field.send_keys("testpassword")

        # Submit the login form
        submit_button = self.driver.find_element(By.NAME, "login")
        submit_button.click()

        time.sleep(2)

        assert " User not found or wrong user" in self.driver.page_source

      
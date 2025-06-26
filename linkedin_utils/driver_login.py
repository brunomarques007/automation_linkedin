import os
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")
language = os.getenv("LINKEDIN_LANGUAGE")


def setup_driver():
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def login(driver, username, password):
    # Verifica se já está logado
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    username_field = driver.find_element("id", "username")
    password_field = driver.find_element("id", "password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys("\ue007")  # Keys.RETURN
    time.sleep(5)
    if "feed" not in driver.current_url:
        print("Login falhou. Verifique suas credenciais.")
        driver.quit()
        sys.exit(1)
    else:
        print("Login bem-sucedido.")

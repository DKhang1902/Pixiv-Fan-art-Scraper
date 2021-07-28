#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs

PATH = r"C:\Program Files (x86)\geckodriver.exe"
PATH_2 = r"C:\Program Files (x86)\chromedriver.exe"
url = "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2Fen%2Ftags%2Fasuna&lang=en&source=pc&view_type=page"

# Get basic information from the user: query, pixiv username and password
query = input("What is your keyword: ")
username = input("What is your user name: ")
password = input("What is your password: ")

# Choose your browser:
browser = input("Would you like to use Google or Firefox(g/f):")
if browser == "g":
    driver = webdriver.Chrome(PATH_2)
else:
    driver = webdriver.Firefox(executable_path= PATH)
driver.get(url)

# Enter the username in the box
search_username = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[1]/input")
for letter in username:
    search_username.send_keys(letter)

# Enter the password in the box
search_passwd = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[2]/input")
for letter in password:
    search_passwd.send_keys(letter)
search_passwd.send_keys(Keys.RETURN)


# Return to home page
try:
    home_page = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[1]/a"))
    )
    home_page.click()
except:
    driver.quit()

# Enter the query in the search box
try:
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[2]/form/div/input"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
except:
    driver.quit()

def find_the_link():
    global driver
    time.sleep(5)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = bs(html, "lxml")
    links = soup.find_all("a",class_="rp5asc-16 kdmVAX sc-AxjAm MksUu")
    links = [link.get("href") for link in links]




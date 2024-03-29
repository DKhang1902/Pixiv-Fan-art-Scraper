#!/usr/bin/env python3
from requests.api import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from bs4 import BeautifulSoup as bs
import io

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
    driver_2 = webdriver.Chrome(PATH_2)
else:
    driver = webdriver.Firefox(executable_path= PATH)
    driver_2 = webdriver.Firefox(executable_path= PATH)
driver.implicitly_wait(30)
driver_2.implicitly_wait(30)

driver.get(url)
driver_2.get(url)
# Enter the username in the box
search_username = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[1]/input")
for letter in username:
    search_username.send_keys(letter)

# Enter the password in the box
search_passwd = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[2]/input")
for letter in password:
    search_passwd.send_keys(letter)
search_passwd.send_keys(Keys.RETURN)

# Enter the username in the box
search_username = driver_2.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[1]/input")
for letter in username:
    search_username.send_keys(letter)

# Enter the password in the box
search_passwd = driver_2.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[2]/input")
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
try:
    home_page = WebDriverWait(driver_2, 300).until(
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

def find_the_links():
    global driver
    time.sleep(5)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = bs(html, "lxml")
    links = soup.find_all("a",class_="rp5asc-16 kdmVAX sc-AxjAm MksUu")
    links = [link.get("href") for link in links]
    links = ["https://pixiv.net"+link for link in links if link.startswith("/en/artworks")]
    print(links)
    return links

def write_to_csv_file(file_name, row):
    with open(file_name,"a",encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
    
def get_detailed_data(links):
    global driver_2
    for link in links:
        driver_2.get(link)
        time.sleep(2)
        html = driver_2.execute_script("return document.documentElement.outerHTML")
        soup = bs(html,"lxml")
        author = soup.find("a",class_ = "sc-10gpz4q-6 hsjhjk").find("div").text
        if author == None:
            time.sleep(3)
            author = soup.find("a",class_ = "sc-10gpz4q-6 hsjhjk").find("div").text
        likes = soup.find("dd", {"title": "Like"}).text
        bookmarks = soup.find("dd", {"title": "Bookmarks"}).text
        views = soup.find("dd", {"title": "Views"}).text
        date = soup.find("div", {"title": "Posting date"}).text
        try:
            title = soup.find("h1", class_ = "sc-1u8nu73-3 feoVvS").text
        except:
            title = ""
        data = [title, author, likes, bookmarks, views, date,link]
        write_to_csv_file(file_name, data)
              

# The main function:
file_name = query.replace(" ","-") + ".csv"
with open(file_name,"a",encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "author", "likes", "bookmarks", "views", "date","link"])

the_links = find_the_links()
print("This is number 1")
get_detailed_data(the_links)
print("This is number 2")
page = 2
def url_generator(query,page):
    url = "https://www.pixiv.net/en/tags/" + query.replace(" ","%20") + "/artworks?p="+str(page)+"&s_mode=s_tag"
    return url
while True:
    hyper = url_generator(query,page)
    try:
        time.sleep(3)
        driver.get(hyper)
    except:
        pass
    the_links = []
    the_links = find_the_links()
    get_detailed_data(the_links)
    page += 1
    if the_links == []:
        break
        

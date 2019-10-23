#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

#READ ACCOUNTS ON FILE
file = open("accounts.txt", "r")
line = file.readline()
account = line.split(" // ")
file.close()

#EXTRACT USER AND PASSWORD OF ONE ACCOUNT
usernameStr = account[0]
passwordStr = account[1]

#SHOW ACCOUNT
print("Account selected: " + usernameStr)

#OPEN NEW WINDOW ON FIREFOX
print("Initializing components")
driver = webdriver.Firefox()

#OPEN URL ON BROWSER
print("Connecting")
driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

#INSERT LOGGING DATA ON LINKEDIN
print("Logging in")
username = driver.find_element_by_id('username')
username.send_keys(usernameStr)
password = driver.find_element_by_id('password')
password.send_keys(passwordStr)
driver.find_element_by_css_selector('.btn__primary--large.from__button--floating').click()

time.sleep(1)

#EXTRACT PROFILE
print("Searching")
driver.get('https://www.linkedin.com/in/leonel-vazquez-41a23a171/')

driver.find_element_by_partial_link_text('contactos').click()

time.sleep(1)

urls = driver.find_elements_by_css_selector('.search-result__result-link.ember-view')

urlslist = []

for url in urls:
    urlslist.append(url.get_attribute("href"))

urlslist = list(dict.fromkeys(urlslist))

for url in urlslist:
    print(url)
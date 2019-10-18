#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from parsel import Selector

from Usuario import Usuario


def searchprofiles(termtofind):
    # READ ACCOUNTS ON FILE
    file = open("accounts.txt", "r")
    line = file.readline()
    account = line.split(" // ")
    file.close()

    # EXTRACT USER AND PASSWORD OF ONE ACCOUNT
    usernameStr = account[0]
    passwordStr = account[1]

    # SHOW ACCOUNT
    print("Account selected: " + usernameStr)

    # OPEN NEW WINDOW ON FIREFOX
    print("Initializing components")
    driver = webdriver.Firefox()

    # OPEN URL ON BROWSER
    print("Connecting")
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

    # INSERT LOGGING DATA ON LINKEDIN
    print("Logging in")
    username = driver.find_element_by_id('username')
    username.send_keys(usernameStr)
    password = driver.find_element_by_id('password')
    password.send_keys(passwordStr)
    driver.find_element_by_css_selector('.btn__primary--large.from__button--floating').click()
    print("Searching")
    driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(termtofind, Keys.ENTER)

    time.sleep(5)

    # GET NAMES
    names = driver.find_elements_by_css_selector('.name.actor-name')

    # GET COMPANIES
    companies = driver.find_elements_by_css_selector('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')

    # GET LINKEDIN PROFILES
    urls = driver.find_elements_by_css_selector('.search-result__result-link.ember-view')

    urlslist = []

    for url in urls:
        urlslist.append(url.get_attribute("href"))

    urlslist = list(dict.fromkeys(urlslist))

    users = []

    i = 0
    while i < len(urlslist):
        user = Usuario(names[i].text, companies[i].text, urlslist[i])
        users.append(user)
        print(names[i].text)
        print(companies[i].text)
        print(urlslist[i])

    return users


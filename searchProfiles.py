#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import urllib.request
from urllib.parse import unquote
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
    time.sleep(6)

    driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(termtofind, Keys.ENTER)

    time.sleep(6)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(6)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    #GET PHOTOS
    images = driver.find_elements_by_xpath('//div[@class="presence-entity presence-entity--size-4 ember-view"]/img')
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
    while i < len(names):
        name = names[i].text
        imagen = "default.jpg"

        if i < len(companies):
            company = companies[i].text
        else:
            company = ""

        if i < len(urlslist):
            url = urlslist[i]
            if i < len(images):
                src = images[i].get_attribute('src')
                if src is not None:
                    imagen = unquote(urlslist[i][28:-1]) + ".jpg"
                    urllib.request.urlretrieve(src, "static/img/" + imagen)
        else:
            url = ""

        user = Usuario(name, company, url, imagen)
        users.append(user)

        i += 1

    driver.close()

    return users


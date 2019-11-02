#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import urllib.request
from urllib.parse import unquote
from Usuario import Usuario
from Account import Account


def searchprofiles(termtofind,user):
    # OPEN NEW WINDOW ON FIREFOX
    print("Initializing components")
    driver = webdriver.Firefox()

    # OPEN URL ON BROWSER
    print("Connecting")
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

    # INSERT LOGGING DATA ON LINKEDIN
    print("Logging in")
    username = driver.find_element_by_id('username')
    username.send_keys(user.username)
    password = driver.find_element_by_id('password')
    password.send_keys(user.password)
    driver.find_element_by_css_selector('.btn__primary--large.from__button--floating').click()
    print("Searching")
    time.sleep(6)

    driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(termtofind, Keys.ENTER)

    time.sleep(5)

    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .01

    time.sleep(1)

    #GET PHOTOS
    images = driver.find_elements_by_xpath('//div[@class="presence-entity presence-entity--size-4 ember-view"]/img')

    for im in images:
        print(im.get_attribute("alt"))

    # GET NAMES
    names = driver.find_elements_by_css_selector('.name.actor-name')

    # GET COMPANIES
    companies = driver.find_elements_by_css_selector('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')

    # GET LINKEDIN PROFILES
    urls = driver.find_elements_by_css_selector('.search-result__result-link.ember-view')

    urlslist = []

    for url in urls:
        if url.get_attribute("href")[25:27] == "in":
            urlslist.append(url.get_attribute("href"))

    urlslist = list(dict.fromkeys(urlslist))

    users = []

    i = 0
    j = 0
    while i < len(names):
        name = names[i].text
        imagen = "default.jpg"

        if i < len(companies):
            company = companies[i].text
        else:
            company = ""

        if i < len(urlslist):
            url = urlslist[i]

            if j < len(images):
                if images[j].get_attribute('alt') == name:
                    src = images[j].get_attribute('src')
                    if src is not None:
                        imagen = unquote(urlslist[i][28:-1]) + ".jpg"
                        urllib.request.urlretrieve(src, "static/img/" + imagen)
                        j += 1
        else:
            url = ""

        user = Usuario(name, company, url, imagen)
        users.append(user)

        i += 1

    driver.close()

    return users


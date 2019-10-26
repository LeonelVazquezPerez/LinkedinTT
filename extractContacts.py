#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

def extractContacts(driver):
    driver.find_element_by_partial_link_text('contactos').click()

    time.sleep(1)

    urls = driver.find_elements_by_css_selector('.search-result__result-link.ember-view')

    urlslist = []
    for url in urls:
        urlslist.append(url.get_attribute("href"))

    urlslist = list(dict.fromkeys(urlslist))

    for url in urlslist:
        print(url)

    return urlslist
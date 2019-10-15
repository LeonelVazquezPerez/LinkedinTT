#IMPORT LIBRARIES FROM SELENIUM
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from parsel import Selector


def searchprofiles(termtofind, driver):

    print("Searching")
    driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(termtofind, Keys.ENTER)

    time.sleep(5)

    urls = driver.find_elements_by_css_selector('.search-result__result-link.ember-view')

    urlslist = []

    for url in urls:
        urlslist.append(url.get_attribute("href"))

    urlslist = list(dict.fromkeys(urlslist))

    #ademas de obtener la url tambien necesitamos nombre, foto y extracto
    pagina = driver.page_source
    page = open("source.txt", "w")
    selec = Selector(text=pagina)
    page.write(pagina)
    names = selec.xpath('//*[starts-with(@class, "name actor-name")]/text()').extract()
    #print("dato:"+str(names))
    titles = selec.xpath('//*[starts-with(@class, "subline-level-1 t-14 t-black t-normal search-result__truncate")]/text()').extract()
    #print("dato: "+str(titles))

    resultados = []
    print(" total: " + str(len(urlslist)) + " " + str(len(names)) + " " + str(len(titles)))
    print(str(urlslist))
    print(str(names))
    print(str(titles))


    return urlslist

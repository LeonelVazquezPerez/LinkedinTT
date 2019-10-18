#IMPORT LIBRARIES FROM SELENIUM
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from parsel import Selector
from GestorSelenium import StartSelenium
import Usuario
def scrappyprofile(url):

    driver = StartSelenium()
    driver.get(url)

    pagina = driver.page_source
    page = open("source.txt", "w")
    selec = Selector(text=pagina)
    page.write(pagina)
    perfil = Usuario.Usuario()
    url_imagen = selec.xpath('//*[starts-with(@class,  "pv-top-card-section__photo presence-entity__image EntityPhoto-circle-9 lazy-image loaded ember-view")]/@src').extract()
    print("resultado: "+ str(url_imagen))

    if len(url_imagen) > 0 :
        nombre_local_imagen = "foto.jpg" # El nombre con el que queremos guardarla
        perfil.img = nombre_local_imagen
        imagen = requests.get(url_imagen[0]).content
        with open(nombre_local_imagen, 'wb') as handler:
            handler.write(imagen)
    else:
        print("El perfil no tiene fotografia")

    name = selec.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract()
    title = selec.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal")]/text()').extract()
    address = selec.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract()
    contacts = selec.xpath('//*[starts-with(@class, "ember-view")]/text()').extract()
    print("name: "+ str(name))
    print("title: "+ str(title))
    print("address: "+ str(address))
    print("contacts: "+ str(contacts))
#IMPORT LIBRARIES FROM SELENIUM
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from parsel import Selector
from GestorSelenium import StartSelenium
from Usuario import Usuario
from Cargo import Cargo
def scrappyprofile(url):

    driver = StartSelenium()
    driver.get(url)

    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    pagina = driver.page_source
    page = open("source.txt", "w")
    selec = Selector(text=pagina)
    page.write(pagina)

    url_imagen = selec.xpath('//*[starts-with(@class,  "pv-top-card-section__photo presence-entity__image EntityPhoto-circle-9 lazy-image loaded ember-view")]/@src').extract()

    if len(url_imagen) > 0 :
        b = 1
    else:
        b = 0

    name = selec.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract()
    title = selec.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal")]/text()').extract()
    address = selec.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract()
    contacts = selec.xpath('//*[starts-with(@class, "ember-view")]/text()').extract()
    # Obtenemos los cargos
    cargos = []
    css1cargo = selec.xpath(
        '//*[starts-with(@class, "pv-entity__summary-info pv-entity__summary-info--background-section ")]/h3/text()').extract()
    cargos += css1cargo
    cargo = selec.xpath('//*[starts-with(@class, "t-16 t-black t-bold")]/span/text()').extract()
    cargomas = selec.xpath('//*[starts-with(@class, "t-14 t-black t-bold")]/span/text()').extract()
    cargomas += cargo
    i = 1
    while i < len(cargomas):
        cargos.append(cargomas[i])
        i += 2

    # Obtenemos las empresas
    empresas = selec.xpath('//*[starts-with(@class, "pv-entity__secondary-title t-14 t-black t-normal")]/text()').extract()
    print("name: " + name[0])
    print("title: " + title[0])
    print("address: " + address[0])
    print("contacts: " + str(contacts))
    print("total: " + str(cargos))
    print("empresas: " + str(empresas))

    # Obtenemos las aptitudes

    if b == 1:
        imagen = url[28:-1] + ".jpg"
    else:
        imagen = "default.jpg"

    perfil = Usuario(name[0], title[0], url, imagen)
    trabajos = []
    if len(cargos) != len(empresas):
        for i in range( len(cargos) - len(empresas) ):
            empresas.append("")

    for i in range(len(cargos)):
        trabajo = Cargo(cargos[i],empresas[i],"","")
        trabajos.append(trabajo)
        print("trabajo: "+ trabajo.name)
        print("empresa: "+ trabajo.empresa)
    perfil.cargos = trabajos

    #Obtenemos la educacion
    escuelas = selec.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract()

    print("Escuelas: " + str(escuelas))
    #driver.close()

    return perfil




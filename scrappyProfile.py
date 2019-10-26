#IMPORT LIBRARIES FROM SELENIUM
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from parsel import Selector
from GestorSelenium import StartSelenium
from Usuario import Usuario
from Cargo import Cargo
from Escuela import Escuela
from extractContacts import extractContacts
import connector
def scrappyprofile(url):

    driver = StartSelenium()
    driver.get(url)

    time.sleep(2)

    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .01

    time.sleep(1)

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
    extracto = selec.xpath('//*[starts-with(@class, "pv-about__summary-text mt4 t-14 ember-view")]/span/text()').extract()
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
    # Obtenemos las fechas por empresa
    fechas = selec.xpath('//*[starts-with(@class, "pv-entity__date-range t-14 t-black--light t-normal")]/span/text()').extract()

    print("name: " + name[0])
    print("title: " + title[0])
    print("address: " + address[0])
    print("contacts: " + str(contacts))
    print("extracto: " + str(extracto))
    if b == 1:
        imagen = url[28:-1] + ".jpg"
    else:
        imagen = "default.jpg"

    perfil = Usuario(name[0], title[0], url, imagen)
    perfil.extracto = extracto[0]
    trabajos = []
    if len(cargos) != len(empresas):
        for i in range( len(cargos) - len(empresas) ):
            empresas.append("")
    if len(cargos) != int(len(fechas)/2):
        for i in range(len(cargos) - int(len(fechas)/2)):
            fechas.append("")
            fechas.append("")

    for i in range(len(cargos)):
        fechas.pop(0)
        trabajo = Cargo(cargos[i], empresas[i], "", fechas[i])
        trabajos.append(trabajo)
        print("insertado: "+trabajo.fecha)
    perfil.cargos = trabajos
    perfil.NoCargos = len(trabajos)

    print("Cargos: "+ str(len(perfil.cargos)))
    #Obtenemos la educacion
    escuelas = selec.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract()
    print("escuelas: "+ str(escuelas))
    if len(escuelas) > 0:

        titulos = selec.xpath('//*[starts-with(@class, "pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal")]/span/text()').extract()
        disciplinas = selec.xpath('//*[starts-with(@class, "pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal")]/span/text()').extract()
        fechas = selec.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]/span/time/text()').extract()
        educacion = []

        for long in range(len(escuelas) - len(disciplinas)):
            disciplinas.append("")
            disciplinas.append("")
        print("longitudes: " + str(len(escuelas)) + " : " + str(len(titulos)) + ":" + str(len(disciplinas)))
        for i in range(len(escuelas)):
            escuela = Escuela(escuelas[i])

            if len(titulos) > 0:
                titulos.pop(0)
                escuela.titulacion = titulos[i]
            if len(disciplinas) > 0:
                disciplinas.pop(0)
                escuela.disciplina = disciplinas[i]
            escuela.fecha = fechas[i] + " - "+fechas[i+1]
            print("Escuelas: " + escuela.name)
            print("Titulos: " + escuela.titulacion)
            print("Disciplinas: " + escuela.disciplina)
            #print("fechas: " + str(fechas))
            educacion.append(escuela)
        perfil.escuelas = educacion
    #obteniendo las aptitudes
    aptitudes= selec.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text t-16 t-black t-bold")]/text()').extract()
    print("aptitudes: " + str(aptitudes))
    perfil.aptitudes = aptitudes
    #Obteniendo los intereses
    intereses = selec.xpath('//*[starts-with(@class, "pv-entity__summary-info ember-view")]/h3/span/text()').extract()
    print("Intereses: " + str(intereses))
    perfil.intereses = intereses
    contactos = extractContacts(driver)

    perfil.contactos = contactos
    i = 0
    for user in contactos:
        i += 1;
        print("**CONTACTO " + str(i))
        print(str(user.name))
        print(str(user.imagen))


    connector.insertarUsuario(perfil)
    #driver.close()

    return perfil




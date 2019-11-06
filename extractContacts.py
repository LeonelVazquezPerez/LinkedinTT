#IMPORT LIBRARIES FROM SELENIUM
import random
import json
import time
import urllib.request
from urllib.parse import unquote
from Usuario import Usuario
from Usuario import UsuarioContact
import math

def extractContacts(driver,urlP):
    users = []
    contacts = []

    try:
        link = driver.find_element_by_partial_link_text('contactos')

        if link.get_attribute('href')[24:31] == '/search':
            link.click()

            #driver.find_element_by_css_selector('.t-16.t-bold').click()

            time.sleep(1)

            scheight = .1
            while scheight < 9.9:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
                scheight += .01

            time.sleep(1)

            # GET PHOTOS
            images = driver.find_elements_by_xpath('//div[@class="presence-entity presence-entity--size-4 ember-view"]/img')

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
                user = UsuarioContact(name, company, url, imagen)
                user.father = urlP
                contacts.append(user)

                i += 1

        else:
            print("No se puede acceder a contactos")

    except Exception as e:
        print("No se puede acceder a contactos")

    #print("CONTACTOS PRINCIPALES")
    #i = 0
    #for cont in contacts:
        #i += 1
        #print("**CONTACTO " + str(i))
        #print(str(cont.name))
        #print(str(cont.url))
        #print(str(cont.imagen))

    datosModelo = searchContacts(driver,contacts,urlP)

    return users,datosModelo

def searchContacts(driver,contacts,urlP):
    for contact in contacts:
        try:
            driver.get(contact.url)
            link = driver.find_element_by_partial_link_text('contactos')

            if link.get_attribute('href')[24:31] == '/search':
                link.click()

                time.sleep(1)

                scheight = .1
                while scheight < 9.9:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
                    scheight += .01

                time.sleep(1)

                # GET PHOTOS
                images = driver.find_elements_by_xpath('//div[@class="presence-entity presence-entity--size-4 ember-view"]/img')

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

                    user = UsuarioContact(name, company, url, imagen)
                    user.father = contact.url
                    contact.contacts.append(user)

                    i += 1

            else:
                print("No se puede acceder a contactos")

        except Exception as e:
            print("No se puede acceder a contactos")

    allcontacts = []
    for contact in contacts:
        for cont in contact.contacts:
            allcontacts.append(cont)

    all = list(dict.fromkeys(allcontacts))

    ids = []
    contactids = []

    for contact in all:
        flag = 0
        for id in ids:
            if contact.url[28:-1] == id:
                flag = 1
                break

        if flag == 0:
            ids.append(contact.url[28:-1])
            contactids.append(contact)

    occurrencies = []

    for contact in contactids:
        cont = 0
        for contactAux in all:
            if contact.url == contactAux.url:
                cont += 1
        occurrencies.append(cont)

    orderedContact = []
    manyContact = []

    i = 0

    for contact in contactids:
        if occurrencies[i] == 1:
            orderedContact.append(contact)
        else:
            manyContact.append(contact)

        i += 1

    orderedContact += manyContact

    datos = {}
    datos["nodes"] = []
    datos["edges"] = []

    i = 0

    for contact in orderedContact:

        if urlP == contact.url:
            x = 0
            y = 0
            color = 'MediumSeaGreen'
        else:
            x = math.cos((i * len(contactids) *.05) + i)
            y = math.sin((i * len(contactids) *.05) + i)
            color = 'white'

        node = {
            "id": str(contact.url[28:-1]),
            "label": str(contact.name),
            "type": 'circle',
            "image": {
                'url': "../../static/img/" + str(contact.imagen),
                'scale': 1.5
            },
            "x": x,
            "y": y,
            "size": 20,
            "color": color
        }

        datos["nodes"].append(node)

        i += 1

    i = 0

    colors = ['red','blue','purple','black','orange','brown','gray','silver','maroon','olive','lime','aqua','navy','fuchsia']

    for contact in all:
        datos["edges"].append(
            {
                "id": str(i),
                "source": str(contact.father[28:-1]),
                "target": str(contact.url[28:-1]),
                "size": 13,
                "color": random.choice(colors)
            }
        )
        i += 1

    jsonstr = json.dumps(datos)

    contacts.clear()
    all.clear()
    contactids.clear()
    orderedContact.clear()
    manyContact.clear()

    print("JSON : "+jsonstr)
    return jsonstr








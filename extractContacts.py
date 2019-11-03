#IMPORT LIBRARIES FROM SELENIUM
import random
import json
import time
import urllib.request
from urllib.parse import unquote
from Usuario import Usuario
from Usuario import UsuarioContact

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

    print("CONTACTOS PRINCIPALES")
    i = 0
    for cont in contacts:
        i += 1
        print("**CONTACTO " + str(i))
        print(str(cont.name))
        print(str(cont.url))

    datosModelo = searchContacts(driver,contacts)

    return users,datosModelo

def searchContacts(driver,contacts):
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


    datos = {}
    datos["nodes"] = []
    datos["edges"] = []

    for contact in contactids:
        datos["nodes"].append(
            {
                "id": str(contact.url[28:-1]),
                "label": str(contact.name),
                "x": random.randrange(11),
                "y": random.randrange(11),
                "size": 15
            }
        )

    i = 0
    for contact in all:
        datos["edges"].append(
            {
                "id": str(i),
                "source": str(contact.father[28:-1]),
                "target": str(contact.url[28:-1]),
                "size": 10
            }
        )
        i += 1

    jsonstr = json.dumps(datos)

    print("JSON : "+jsonstr)
    return jsonstr








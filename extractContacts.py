#IMPORT LIBRARIES FROM SELENIUM
import time
import urllib.request
from urllib.parse import unquote
from Usuario import Usuario

def extractContacts(driver):
    users = []

    try:
        link = driver.find_element_by_partial_link_text('contactos')
        print(link.get_attribute('href')[24:31])
        if link.get_attribute('href')[24:31] == '/search':
            link.click()

            #driver.find_element_by_css_selector('.t-16.t-bold').click()

            time.sleep(2)

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

                i += 1

        else:
            print("No se puede acceder a contactos")

    except Exception as e:
        print("No se puede acceder a contactos")
    print(users)
    return users
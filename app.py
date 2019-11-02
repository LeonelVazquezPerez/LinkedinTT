from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from searchProfiles import searchprofiles
from scrappyProfile import scrappyprofile
from connector import borrarperfilbyurl
from accountController import accountController

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/resultados/', methods = ["GET","POST"])
def resultados():
    if request.method== "POST":
        cadena = request.form["cadena"]
        print("valor obtenido:"+cadena)
        userR = controller.selectAccount()
        resultado = searchprofiles(cadena, userR)
        for res in resultado:
            print(res.url[28:-1] + ".jpg")
        paquete = []
        paquete.append(cadena)
        paquete.append(len(resultado))
        paquete.append(resultado)
        controller.closeAccount(userR)

        return render_template("resultados.html", paquete=paquete)
    return render_template('resultados.html')


@app.route('/resultados/verperfil/', methods = ["GET","POST"])
def verperfil():
    if request.method == "GET":
        url = request.args.get("url", "")
        print("URL solicitada: "+url)
        userV = controller.selectAccount()
        perfil = scrappyprofile(url, userV)
        controller.closeAccount(userV)
        return render_template("verPerfil.html", perfil=perfil)
    return render_template('index.html')

@app.route('/verperfil/', methods = ["GET","POST"])
def actualizarperfil():
    if request.method == "GET":
        url = request.args.get("url","")
        print("URL solicitada para actualizar: "+url)
        borrarperfilbyurl(url)
        userA = controller.selectAccount()
        perfil = scrappyprofile(url,userA)
        controller.closeAccount(userA)
        return render_template("verPerfil.html", perfil=perfil)
    return render_template('index.html')


@app.route('/vercontactos/', methods = ["GET","POST"])
def vercontactos():
    if request.method == "GET":
        url = request.args.get("url", "")
        print("URL solicitada: " + url)

        return render_template("verRedContactos.html")
    return render_template('verRedContactos.html')

global driver
if __name__ == "__main__":
    controller = accountController()
    app.run(host='127.0.0.1', debug=True)


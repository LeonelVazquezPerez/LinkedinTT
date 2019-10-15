from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from searchProfiles import searchprofiles
from GestorSelenium import StartSelenium
@app.route('/')
def index():

    return render_template('index.html')


@app.route('/resultados/', methods = ["GET","POST"])
def resultados():
    if request.method== "POST":
        cadena = request.form["cadena"]
        print("valor obtenido:"+cadena)
        resultado = searchprofiles(cadena,driver)
        paquete = []
        paquete.append(cadena)
        paquete.append(len(resultado))
        paquete.append(resultado)
        return render_template("resultados.html", paquete=paquete)
    return render_template('resultados.html')


@app.route('/resultados/verperfil/', methods = ["GET","POST"])
def verperfil():
    if request.method == "GET":
        url = request.args.get("url","")
        print("URL solicitada: "+url)
        return render_template("verPerfil.html", paquete=url)
    return render_template('index.html')


global driver


if __name__ == "__main__":
    driver = StartSelenium()
    print("Driver recibido")
    app.run(debug=True)


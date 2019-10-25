class Usuario:
    aptitudes = []
    cargos = []
    certificacion = []
    contactos = []
    cursos = []
    escuelas = []
    patente = []
    publicacion = []
    residencia = []
    empresas = []
    NoCargos = 0
    intereses = []
    extracto = ""
    def __init__(self, name, company, url, imagen):
        self.name = name
        self.company = company
        self.url = url
        self.imagen = imagen
class Usuario:
    aptitudes = []
    cargos = []
    certificacion = []
    contactos = []
    cursos = []
    escuela = []
    patente = []
    publicacion = []
    residencia = []

    def __init__(self, name, company, url, imagen):
        self.name = name
        self.company = company
        self.url = url
        self.imagen = imagen
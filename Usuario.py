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

    def __init__(self, name, company, url):
        self.name = name
        self.company = company
        self.url = url
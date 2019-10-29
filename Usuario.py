class Usuario:
    aptitudes = []
    cargos = []
    certificaciones = []
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
    logros = []
    logrosTitles = []
    def __init__(self, name, company, url, imagen):
        self.name = name
        self.company = company
        self.url = url
        self.imagen = imagen
import pymysql
def consultarUsuarios():
    try:
        conexion = pymysql.connect(host='localhost', user='root', password='', db='tt')
        try:
            with conexion.cursor() as cursor:
                #consulta = "INSERT INTO peliculas(titulo, anio) VALUES (%s, %s);"
                #Podemos llamar muchas veces a .execute con datos distintos
                #cursor.execute(consulta, ("Volver al futuro 1", 1985))
                consulta = "SELECT * FROM usuario;"
                cursor.execute(consulta)
                for perfil in cursor.fetchall():
                    print(perfil)
                conexion.commit()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)

def insertarUsuario(usuario):
    try:
        conexion = pymysql.connect(host='localhost', user='root', password='', db='tt')
        try:
            with conexion.cursor() as cursor:
                #consulta = "INSERT INTO peliculas(titulo, anio) VALUES (%s, %s);"
                #Podemos llamar muchas veces a .execute con datos distintos
                #cursor.execute(consulta, ("Volver al futuro 1", 1985))
                consulta = "INSERT INTO usuario(nombre,titular,extracto,url) VALUES (%s,%s,%s,%s);"
                cursor.execute(consulta, (usuario.name, usuario.company, usuario.extracto, usuario.url))
                conexion.commit()
                consultarUsuarios()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)

# ALTER TABLE `members` CHANGE COLUMN` full_names` `fullname` char (250) NOT NULL;
#alter table personal drop pasatiempo;
def insertarCargos(usuario):
    try:
        conexion = pymysql.connect(host='localhost', user='root', password='', db='tt')
        try:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO cargos(nombre,empresa,ubicacion,fecha) VALUES (%s,%s,%s,%s)"
                cursor.execute(consulta, (usuario.name, usuario.company, usuario.extracto, usuario.url))
                conexion.commit()
                consultarUsuarios()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
consultarUsuarios()
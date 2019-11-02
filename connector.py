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
                flag = True
                print("Revisando si ya existe el usuario")
                consulta = "SELECT * FROM usuario WHERE url = '" + usuario.url + "';"
                cursor.execute(consulta)
                for coincidencia in cursor.fetchall():
                    flag = False
                    break

                if flag:
                    print("EL usuario no existe, lo insertamos")
                    #Se inserta en la tabla usuario
                    consulta = "INSERT INTO usuario(nombre,titular,extracto,url) VALUES (%s,%s,%s,%s);"
                    cursor.execute(consulta, (usuario.name, usuario.company, usuario.extracto, usuario.url))
                    conexion.commit()
                    print("consultamos el ultimo usuario insertado")
                    consulta = "select * from usuario order by idUsuario desc limit 1;"
                    cursor.execute(consulta)
                    indiceUsuario = cursor.fetchone()
                    print("Ultimo indice:" + str(indiceUsuario[0]))

                    #se insertan las aptitudes
                    insertarAptitudes(conexion,usuario.aptitudes,indiceUsuario)
                    #Se insertan los cargos
                    insertarCargos(conexion, usuario.cargos, indiceUsuario)
                    #Se insertan las certificaciones
                    insertarCertificaciones(conexion, usuario.certificaciones,indiceUsuario)
                    #Se insertan las escuelas
                    insertarEscuelas(conexion,usuario.escuelas,indiceUsuario)

                else:
                    print("EL usuario ya existe")



                consultarUsuarios()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)


def insertarCargos(conexion, cargos, indiceUsuario):

        try:
            for cargo in cargos:
                with conexion.cursor() as cursor:
                    consulta = "INSERT INTO cargos(nombre,empresa,ubicacion,fecha) VALUES (%s,%s,%s,%s)"
                    cursor.execute(consulta, (cargo.name, cargo.empresa, cargo.ubicacion, cargo.fecha))
                    conexion.commit()
                    print("cargo insertado")
                    consulta = "select * from cargos order by idCargo desc limit 1;"
                    cursor.execute(consulta)
                    indiceCargo = cursor.fetchone()
                    putRelUsuarioCargo(conexion, str(indiceUsuario[0]), str(indiceCargo[0]))

        finally:
            print("cargos insertados")


def putRelUsuarioCargo(conexion,idusu,idcargo):
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuario_has_cargos(usuario_idUsuario,cargos_idCargo) VALUES (%s,%s)"
            cursor.execute(consulta, (idusu,idcargo))
            conexion.commit()
            return "Relacion insertada"
    finally:
        print("Relaciones Insertadas")

def insertarEscuelas(conexion,escuelas,indiceUsuario):
    try:
        for escuela in escuelas:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO escuela(nombre,titulacion,disciplinaAcademica,fecha) VALUES (%s,%s,%s,%s)"
                cursor.execute(consulta, (escuela.name, escuela.titulacion, escuela.disciplina, escuela.fecha ))
                conexion.commit()
                print("escuela insertada")
                consulta = "select * from escuela order by idEscuela desc limit 1;"
                cursor.execute(consulta)
                indiceCargo = cursor.fetchone()
                putRelUsuarioEscuela(conexion, str(indiceUsuario[0]), str(indiceCargo[0]))

    finally:
        print("cargos insertados")


def putRelUsuarioEscuela(conexion, idusu,idescuela):
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuario_has_escuela(usuario_idUsuario,escuela_idEscuela) VALUES (%s,%s)"
            cursor.execute(consulta, (idusu, idescuela))
            conexion.commit()
            return "Relacion insertada"
    finally:
        print("Relaciones Insertadas")

def insertarAptitudes(conexion, aptitudes, indiceUsuario):
    try:
        for aptitud in aptitudes:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO aptitudes(descripcion) VALUES (%s)"
                cursor.execute(consulta, (aptitud))
                conexion.commit()
                print("aptitud insertada")
                consulta = "select * from aptitudes order by idAptitud desc limit 1;"
                cursor.execute(consulta)
                indiceAptitud = cursor.fetchone()
                putRelUsuarioAptitud(conexion, str(indiceUsuario[0]), str(indiceAptitud[0]))

    finally:
        print("cargos insertados")


def putRelUsuarioAptitud(conexion, idusu,idAptitud):
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuario_has_aptitudes(usuario_idUsuario,aptitudes_idAptitud) VALUES (%s,%s)"
            cursor.execute(consulta, (idusu, idAptitud))
            conexion.commit()
            return "Relacion insertada"
    finally:
        print("Relaciones Insertadas")

def insertarCertificaciones(conexion, certificaciones, indiceUsuario):

    try:
        for certificacion in certificaciones:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO certificacion(nombre) VALUES (%s)"
                cursor.execute(consulta, (certificacion))
                conexion.commit()
                print("certificacion insertada")
                consulta = "select * from certificacion order by idCertificacion desc limit 1;"
                cursor.execute(consulta)
                indiceCargo = cursor.fetchone()
                putRelUsuarioCertificacion(conexion, str(indiceUsuario[0]), str(indiceCargo[0]))

    finally:
        print("cargos insertados")


def putRelUsuarioCertificacion(conexion, idusu,idCertificacion):
    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuario_has_certificacion(usuario_idUsuario,certificacion_idCertificacion) VALUES (%s,%s)"
            cursor.execute(consulta, (idusu, idCertificacion))
            conexion.commit()
            return "Relacion insertada"
    finally:
        print("Relaciones Insertadas")


def borrarperfilbyurl(url):
    try:
        conexion = pymysql.connect(host='localhost', user='root', password='', db='tt')
        try:
            with conexion.cursor() as cursor:
                consulta = "SELECT idUsuario FROM usuario WHERE url = '"+url+"';"
                cursor.execute(consulta)
                idUsuario = cursor.fetchone()[0] #es entero el id
                print("idUsuario obtenido: " + str(idUsuario))

                #Eliminamos las aptitudes
                consulta = "SELECT aptitudes_idAptitud FROM usuario_has_aptitudes WHERE usuario_idUsuario = " + str(idUsuario) + ";"
                cursor.execute(consulta)
                for idaptitud in cursor.fetchall():
                    print("idAptitud: " + str(idaptitud[0]))
                    consulta = "DELETE FROM usuario_has_aptitudes WHERE aptitudes_idAptitud =" + str(idaptitud[0]) + ";"
                    cursor.execute(consulta)
                    consulta = "DELETE FROM aptitudes WHERE idAptitud =" + str(idaptitud[0]) + ";"
                    cursor.execute(consulta)

                #Eliminamos los cargos
                consulta = "SELECT cargos_idCargo FROM usuario_has_cargos WHERE usuario_idUsuario = " + str(idUsuario) +";"
                cursor.execute(consulta)
                for idcargo in cursor.fetchall():
                    print("idCargo: " + str(idcargo[0]))
                    consulta = "DELETE FROM usuario_has_cargos WHERE cargos_idCargo =" + str(idcargo[0]) + ";"
                    cursor.execute(consulta)
                    consulta = "DELETE FROM cargos WHERE idCargo =" + str(idcargo[0]) + ";"
                    cursor.execute(consulta)
                #Eliminamos las certificaciones
                consulta = "SELECT certificacion_idCertificacion FROM usuario_has_certificacion WHERE usuario_idUsuario = " + str(idUsuario) + ";"
                cursor.execute(consulta)
                for idcertificacion in cursor.fetchall():
                    print("idCertificacion: " + str(idcertificacion[0]))
                    consulta = "DELETE FROM usuario_has_certificacion WHERE certificacion_idCertificacion =" + str(idcertificacion[0]) + ";"
                    cursor.execute(consulta)
                    consulta = "DELETE FROM certificacion WHERE idCertificacion =" + str(idcertificacion[0]) + ";"
                    cursor.execute(consulta)
                #Eliminamos las escuelas
                consulta = "SELECT escuela_idEscuela FROM usuario_has_escuela WHERE usuario_idUsuario = " + str(idUsuario) + ";"
                cursor.execute(consulta)
                for idescuela in cursor.fetchall():
                    print("idEscuela: "+ str(idescuela[0]))
                    consulta = "DELETE FROM usuario_has_escuela WHERE escuela_idEscuela =" + str(idescuela[0]) + ";"
                    cursor.execute(consulta)
                    consulta = "DELETE FROM escuela WHERE idEscuela =" + str(idescuela[0]) + ";"
                    cursor.execute(consulta)

                #Eliminamos el usuario
                consulta = "DELETE FROM usuario WHERE url = '" + url + "';"
                cursor.execute(consulta)
                conexion.commit()
                print("EL USUARIO SE HA ELIMINADO")
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)


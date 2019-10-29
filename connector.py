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
                    consulta = "INSERT INTO usuario(nombre,titular,extracto,url) VALUES (%s,%s,%s,%s);"
                    cursor.execute(consulta, (usuario.name, usuario.company, usuario.extracto, usuario.url))
                    conexion.commit()
                    print("consultamos el ultimo usuario insertado")
                    consulta = "select * from usuario order by idUsuario desc limit 1;"
                    cursor.execute(consulta)
                    indiceUsuario = cursor.fetchone()
                    print("Ultimo indice:" + str(indiceUsuario[0]))
                    print("Cargos: " + str(len(usuario.cargos)))
                    insertarCargos(conexion, usuario.cargos, indiceUsuario)

                else:
                    print("EL usuario ya existe")



                consultarUsuarios()
        finally:
            conexion.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)

# ALTER TABLE `members` CHANGE COLUMN` full_names` `fullname` char (250) NOT NULL;
#alter table personal drop pasatiempo;


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




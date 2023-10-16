

class Devoluciones:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def crear_devolucion(self, devolucion):
        sql = f"INSERT INTO `devoluciones` (`num_factura`, `documento_operador`, `nombre_operador`, `apellido_operador`, `cliente_devolucion`, `fecha_devolucion`) VALUES  ('{devolucion[0]}','{devolucion[1]}','{devolucion[2]}','{devolucion[3]}','{devolucion[4]}','{devolucion[5]}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def devolucion_Existe_Db(self, devolucion):
        sql = f"SELECT COUNT(*) FROM devoluciones WHERE id_devolucion = '{devolucion}'"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False
        
    def buscar_devolucion(self, id_devoluciones):
        sql = f"SELECT id_devolucion FROM devoluciones WHERE id_devoluciones = '{id_devoluciones}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        if(len(resultado)==0):
            return False
        else:
            return True
        
    #modificar clientes
    def modificar_devolcion(self, devolucion):
        sql=f"UPDATE devoluciones SET id_devolucion='{devolucion[0]}',num_factura='{devolucion[1]}',documento_operador='{devolucion[2]}',nombre_operador='{devolucion[3]}', WHERE 1"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    #Borrar clientes
    def borrar_devolucion(self, id_devolucion):
        if not self.devolucion_Existe_Db(id_devolucion):
            return False  

        sql = f"UPDATE devoluciones SET estado_devolucion='INACTIVO' WHERE id_devolucion = '{id_devolucion}'"

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True  # Borrado exitoso
        except Exception as e:
            print(f"Error al borrar devolucion: {str(e)}")
            self.conexion.rollback()
            return False
            
    
    
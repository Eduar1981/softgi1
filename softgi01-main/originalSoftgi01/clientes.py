
class Clientes:
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()

    def crear_cliente(self, cliente):           
        sql = f"INSERT INTO clientes(doc_cliente, nom_cliente, ape_cliente, fecha_nacimiento_cliente, contacto_cliente, email_cliente, direccion_cliente, ciudad_cliente, tipo_persona, doc_empleado, nom_empleado, ape_empleado, fechahora_registro, estado_cliente) VALUES ('{cliente[0]}','{cliente[1]}','{cliente[2]}','{cliente[3]}','{cliente[4]}','{cliente[5]}','{cliente[6]}', '{cliente[7]}','{cliente[8]}','{cliente[9]}', '{cliente[10]}', '{cliente[11]}', '{cliente[12]}', '{cliente[13]}', '{cliente[14]}''ACTIVO')"
        self.cursor.execute(sql)
        self.conexion.commit()


    def cliente_existe_en_db(self, cliente):
        sql = f"SELECT COUNT(*) FROM clientes WHERE doc_cliente = '{cliente}'"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False

        
    def buscar_cliente(self, doc_cliente):
        sql = f"SELECT doc_cliente FROM clientes WHERE doc_cliente = '{doc_cliente}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        if(len(resultado)==0):
            return False
        else:
            return True
        
    #modificar clientes
    def modificar_cliente(self,clientes):
        sql=f"UPDATE clientes SET doc_cliente='{clientes[0]}', nom_cliente='{clientes[1]}', ape_cliente='{clientes[2]}', fecha_nacimiento_cliente='{clientes[3]}', contacto_cliente='{clientes[4]}', email_cliente='{clientes[5]}', direccion_cliente='{clientes[6]}', ciudad_cliente='{clientes[7]}', tipo_persona='{clientes[8]}' WHERE doc_cliente='{clientes[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    #Borrar clientes
    def borrar_cliente(self, documento):
        if not self.cliente_existe_en_db(documento):
            return False  

        sql = f"UPDATE clientes SET estado_cliente='INACTIVO' WHERE doc_cliente = '{documento}'"

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True  # Borrado exitoso
        except Exception as e:
            print(f"Error al borrar cliente: {str(e)}")
            self.conexion.rollback()
            return False
            
    
    
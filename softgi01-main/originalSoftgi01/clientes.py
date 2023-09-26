
class Clientes:
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()

    def crear_cliente(self, cliente):           
        sql = f"INSERT INTO clientes(doc_cliente, nom_cliente, ape_cliente, contacto_cliente, email_cliente, direccion_cliente, tipo_persona, estado_cliente) VALUES ('{cliente[0]}','{cliente[1]}','{cliente[2]}','{cliente[3]}','{cliente[4]}','{cliente[5]}','{cliente[6]}', 'ACTIVO')"
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
        sql=f"UPDATE clientes SET doc_cliente='{clientes[0]}', nom_cliente='{clientes[1]}', ape_cliente='{clientes[2]}', contacto_cliente='{clientes[3]}', email_cliente='{clientes[4]}', direccion_cliente='{clientes[5]}', tipo_persona='{clientes[6]}' WHERE doc_cliente='{clientes[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    #Borrar clientes
    def borrar_cliente(self, documento):
        if not self.cliente_existe_en_db(documento):
            return False  

        sql = f"UPDATE clientes SET estado='INACTIVO' WHERE doc_cliente = '{documento}'"

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True  # Borrado exitoso
        except Exception as e:
            print(f"Error al borrar cliente: {str(e)}")
            self.conexion.rollback()
            return False
            
    
    
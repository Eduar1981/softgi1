class Categorias:
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()

    def crear_categoria(self, categoria):    
        sql = f"INSERT iINTO `categorias`(`nom_categoria`, `fechahora_creacion`, `documento_operador`, `nombre_operador`, `apellido_operador`, `estado_categorias`) VALUES ('{categoria[0]}', '{categoria[1]}', '{categoria[2]}', '{categoria[3]}', '{categoria[4]}','ACTIVO')"
        self.cursor.execute(sql)
        self.conexion.commit()
 

    def categoria_existe_en_db(self, categoria):
        sql = f"SELECT COUNT(*) FROM categorias WHERE nom_categoria = '{categoria}'"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False
        
        
    def modificar_categoria(self, categorias):
        sql=f"UPDATE categorias SET id_categoria='{categorias[0]}', nom_categoria='{categorias[1]}' WHERE id_categoria='{categorias[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()


    def borrar_categoria(self,id_categoria):
        sql=f"UPDATE categorias SET estado_categorias='INACTIVO' WHERE id_categoria='{id_categoria}'"
        self.cursor.execute(sql)
        self.conexion.commit()

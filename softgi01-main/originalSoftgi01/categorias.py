class Categorias:
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()

    def crear_categoria(self, categoria):    
        sql = f"INSERT INTO categorias('id_categoria', 'nom_categoria' 'operador_categoria', 'fechahora_creacion','estado_categorias') VALUES ('{categoria[0]}', '{categoria[1]}', '1112388921', '{categoria[3]}', 'ACTIVO')"
        self.cursor.execute(sql)
        self.conexion.commit()
 

    def categoria_existe_en_db(self, categoria):
        sql = f"SELECT COUNT(*) FROM categoria WHERE nom_categoria = '{categoria}'"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False
        
        
    def modificar_categoria(self, categorias):
        sql=f"UPDATE categorias SET id_categoria='{categorias[0]}', nom_categoria='{categorias[1]}'"
        self.cursor.execute(sql)
        self.conexion.commit()

    
    def borrar_categoria(self, idcategoria):
        if not self.categoria_existe_en_db(idcategoria):
            return False  

        sql = f"UPDATE categorias SET estado='INACTIVO' WHERE idcat = '{idcategoria}'"

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True  # Borrado exitoso
        except Exception as e:
            print(f"Error al borrar la categoria: {str(e)}")
            self.conexion.rollback()
            return False
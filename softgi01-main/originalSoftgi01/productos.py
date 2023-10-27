class Productos:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    def crearProductos(self, producto):
        sql = F"INSERT INTO `productos`( `id_producto`, `referencia_producto`, `categoria`, `proveedor`, `nombre_producto`, `precio_compra`, `precio_venta`, `cantidad_producto`, `descripcion`, `stockminimo`, `ubicacion`, `estante`, `fechahora_registro`, `documento_operador`, `nombre_operador`, `apellido_operador`,`nombre_proveedor`, `estado_producto`) VALUES ('{producto[0]}','{producto[1]}','{producto[2]}','{producto[3]}','{producto[4]}','{producto[5]}','{producto[6]}','{producto[7]}','{producto[8]}','{producto[9]}','{producto[10]}', '{producto[11]}', '{producto[12]}', '{producto[13]}' , '{producto[14]}', '{producto[15]}','{producto[16]}', 'ACTIVO')"
        self.cursor.execute(sql)
        self.conexion.commit() 
    

    def producto_existe_en_db(self, producto):
        sql = f"SELECT COUNT(*) FROM productos WHERE id_producto = '{producto}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False


    def modificar(self,productos):
        sql=f"UPDATE productos SET id_producto='{productos[0]}', referencia_producto='{productos[1]}', categoria='{productos[2]}',proveedor='{productos[3]}', nombre_producto='{productos[4]}', precio_compra='{productos[5]}', precio_venta='{productos[6]}', cantidad_producto='{productos[7]}', descripcion='{productos[8]}', stockminimo='{productos[9]}', ubicacion='{productos[10]}', estante='{productos[11]}', nombre_proveedor='{productos[12]}' WHERE id_producto='{productos[0]}'"

        self.cursor.execute(sql)
        self.conexion.commit()

    
    def borrar_producto(self, id_producto):
        if not self.producto_existe_en_db(id_producto):
            return False  

        sql = f"UPDATE productos SET estado_producto='INACTIVO' WHERE id_producto = '{id_producto}'"

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True  # Borrado exitoso
        except Exception as e:
            print(f"Error al borrar el producto: {str(e)}")
            self.conexion.rollback()
            return False
    
    
 

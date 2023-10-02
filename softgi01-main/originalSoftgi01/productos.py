class productos:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    """ def crearProductos(self, agregar):
        sql = F"INSERT INTO `productos`('id_producto`, `referencia_producto, `categoria`, `proveedor`, `nombre_producto`, `precio_compra`, `precio_venta`, `cantidad_producto`, 'descripcion', `stockminimo`, 'estado_producto', `ubicacion`, `estante`, `operador_producto`)VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}','{agregar[5]}','{agregar[6]}','{agregar[7]}','{agregar[8]}','{agregar[9]}','{agregar[10]}', '{agregar[11]}', '{agregar[12]}', '{agregar[13]}' 'ACTIVO')"
        self.cursor.execute(sql)
        self.conexion.commit() """
    def crearProductos(self, agregar):
        sql = """
        INSERT INTO productos
        (id_producto, referencia_producto, categoria, proveedor, nombre_producto, precio_compra, precio_venta, cantidad_producto, descripcion, stockminimo, estado_producto, ubicacion, estante, operador_producto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, agregar)
        self.conexion.commit()

    def producto_existe_en_db(self, producto):
        sql = f"SELECT COUNT(*) FROM clientes WHERE id_producto = '{producto}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False


    #leer producto
    def muestra_Productos(self, id_producto):
        sql = f"SELECT * FROM productos WHERE id_producto = '{id_producto}' AND estado = 'ACTIVO'"
        self.cursor.execute(sql)
        producto = self.cursor.fetchone()

        if producto:
            return {
                'referencia_producto': producto[0],
                'id_producto': producto[1],
                'categoria': producto[2],
                'proveedor': producto[3],
                'nombre_producto': producto[4],
                'precio_compra': producto[5],
                'precio_venta': producto[6],
                'cantidad_producto': producto[7],
                'descripcion' : producto[8],
                'stockminimo': producto[9],
                'ubicacion': producto[10],
                'estante': producto[11]
            }
        else:
            return None
        
def modificar(self, producto):
        sql=f"UPDATE productos SET id_producto ='{producto[0]}',referencia_producto='{producto[1]}', categoria ='{producto[2]}', proveedor ='{producto[3]}', nombre_producto ='{producto[4]}', precio_compra ='{producto[5]}', precio_venta = '{producto[6]}', cantidad_producto = '{producto[7]}', descripcion = '{producto[8]}', stockminimo = '{producto[9]}', estado_producto = '{producto[10]}', ubicacion = '{producto[11]}', operador_producto = '{producto[12]}'WHERE doc_proveedor='{producto[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()

 #Eliminar productos
def borra_produc(self,id_producto):
    sql=f"UPDATE productos SET estado_producto ='INACTIVO' WHERE id_producto ='{id_producto}'"
    self.cursor.execute(sql)
    self.conexion.commit()
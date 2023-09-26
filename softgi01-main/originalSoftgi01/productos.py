class productos:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    def crearProductos(self, agregar):
        bsdsql = F"INSERT INTO `productos`(`id_producto`, `referencia_producto`, `categoria`, `proveedor`, `nombre_producto`, `precio_compra`, `precio_venta`, `cantidad_producto`, `stockminimo`, `ubicacion`, `estante`, `operador_producto` `estado_producto`,)VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}','{agregar[5]}','{agregar[6]}','{agregar[7]}','{agregar[8]}','{agregar[9]}','{agregar[10]}', '{agregar[11]}', 'ACTIVO')"

        self.cursor.execute(bsdsql)
        self.conexion.commit()

    #Eliminar productos
    def borrar(self,id_producto):
        sql=f"UPDATE productos SET estado_producto ='INACTIVO' WHERE id_producto ='{id_producto}'"
        self.cursor.execute(sql)
        self.conexion.commit()


    #leer producto
    def leerProducto(self, id_producto):
        sql = f"SELECT * FROM productos WHERE id_producto = '{id_producto}' AND estado = 'ACTIVO'"
        self.cursor.execute(sql)
        producto = self.cursor.fetchone()

        if producto:
            return {
                'id_producto': producto[0],
                'referencia_producto': producto[1],
                'categoria': producto[2],
                'proveedor': producto[3],
                'nombre_producto': producto[4],
                'precio_compra': producto[5],
                'precio_venta': producto[6],
                'cantidad_producto': producto[7],
                'stockminimo': producto[8],
                'ubicacion': producto[9],
                'estante': producto[10],
                'operador_producto': producto[11],
            }
        else:
            return None


class Compras_proved:
    def __init__(self, DB, app):  
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  
        self.cursor = self.conexion.cursor()

    def registrar_compra(self,datos_compra):
        sql = f"INSERT INTO `comprasproveedores`(`proveedor_compra`, `documento_operador`, `nombre_operador`, `apellido_operador`, `date_compra`,`estado`,`codigo_tabla`) VALUES ('{datos_compra[0]}','{datos_compra[1]}','{datos_compra[2]}','{datos_compra[3]}','{datos_compra[4]}','{datos_compra[5]}','{datos_compra[6]}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def registrar_detalles_compra(self,datos_compra):
        sql = f"INSERT INTO detallecomprasproveedores (detallenum_compra, producto_compra, cantidad_producto_compra, valorunidad_prodcompra, valortotal_cantidadcomp) VALUES ('{datos_compra[0]}','{datos_compra[1]}','{datos_compra[2]}','{datos_compra[3]}','{datos_compra[4]}')"
        self.cursor.execute(sql)
        self.conexion.commit()

    def cacela_compra(self,num_compra):
        sql = f"UPDATE comprasproveedores SET estado = 'CANCELADO' WHERE num_compra = '{num_compra}'"
        self.cursor.execute(sql)
        self.conexion.commit()

    def edita_detalles_compra(self,datos_compra):
        sql = f"UPDATE detallecomprasproveedores SET num_compra='{datos_compra[0]}' ,producto_compra='{datos_compra[1]}', cantidad_producto_compra='{datos_compra[2]}', valorunidad_prodcompra='{datos_compra[3]}',valortotal_cantidadcomp='{datos_compra[4]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
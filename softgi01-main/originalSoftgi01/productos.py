class productos:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    def crearProductos(self, agreagr):
        bsdsql = F"INSERT INTO `productos`(`idprod`,`prov`, `cat`, `nomprod`, `ref`, `precomp`, `prevent`, `desprod`, `cantprod`, `stockmin`, `ubicacion`, `estado`) VALUES ('{agreagr[0]}','{agreagr[1]}','{agreagr[2]}','{agreagr[3]}','{agreagr[4]}','{agreagr[5]}','{agreagr[6]}','{agreagr[7]}','{agreagr[8]}','{agreagr[9]}','{agreagr[10]}','ACTIVO')"
        self.cursor.execute(bsdsql)
        self.conexion.commit()

    #Eliminar productos
    def borrar(self,id_producto):
        sql=f"UPDATE productos SET estado='INACTIVO' WHERE idprod='{id_producto}'"
        self.cursor.execute(sql)
        self.conexion.commit()


    #leer producto
    def leerProducto(self, id_producto):
        sql = f"SELECT * FROM productos WHERE idprod = '{id_producto}' AND estado = 'ACTIVO'"
        self.cursor.execute(sql)
        producto = self.cursor.fetchone()

        if producto:
            return {
                'idprod': producto[0],
                'prov': producto[1],
                'cat': producto[2],
                'nomprod': producto[3],
                'ref': producto[4],
                'precomp': producto[5],
                'prevent': producto[6],
                'desprod': producto[7],
                'cantprod': producto[8],
                'stockmin': producto[9],
                'ubicacion': producto[10],
                'estado': producto[11]
            }
        else:
            return None
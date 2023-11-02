class Ventas:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def crear_venta(self, venta):
        sql = f"INSERT INTO `ventas` (`num_factura`, `cliente_factura`, `numero_cotizacion`, `nombre_operador`, `apellido_operador`, `fechahora_venta`,`forma_pago`,`medio_pago`) VALUES  ('{venta[0]}','{venta[1]}','{venta[2]}','{venta[3]}','{venta[4]}','{venta[5]}','{venta[6]}','{venta[7]}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def venta_Existe_Db(self, venta):
        sql = f"SELECT COUNT(*) FROM ventas WHERE num_factura = '{venta}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False
        
    def buscar_venta(self, num_factura):
        sql = f"SELECT num_factura FROM ventas WHERE num_factura = '{num_factura}'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        if(len(resultado)==0):
            return False
        else:
            return True
        
    #modificar venta
    def modificar_venta(self, venta):
        sql=f"UPDATE ventas SET num_factura='{venta[0]}',nombre_operador='{venta[1]}',apellido_operador='{venta[2]}', WHERE 1"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    
            
    def crearDetalleventa(self, registrar):
        bsql = f"INSERT INTO `detalleventas`(`id_detalle_factura`, `num_factura_venta`,`producto_factura`,`cantidad_productos_factura`,`precio_productofactura`,`valortotal_productos_factura`,`servicio_factura`,`cantidad_servicios_factura`,`precio_serviciosfactura`,`valortotal_servicios_factura`,`total_pagar_factura`) VALUES  ('{registrar[0]}','{registrar[1]}','{registrar[2]}','{registrar[3]}','{registrar[4]}','{registrar[5]}','{registrar[6]}','{registrar[7]}','{registrar[8]}','{registrar[9]}','{registrar[10]}')"
        self.cursor.execute(bsql)
        self.conexion.commit()
    
    def editarDetalleventa(self, editar):
        bsql =f"UPDATE `detalleventas` SET `id_detalle_factura`='{editar[1]}',`num_factura_venta`='{editar[2]}',`producto_factura`='{editar[3]}',`cantidad_productos_factura`='{editar[4]}',`precio_productofactura`='{editar[5]}' WHERE id_detalle_factura"
        self.cursor.execute(bsql)
        self.conexion.commit()
        
    def eliminarDetalleventa(self,id_detalle_ventas):
        sql = f"DELETE FROM `detalleventas` WHERE  `id_detalle_factura`='{id_detalle_ventas}'"
        self.cursor.execute(sql)
        self.conexion.commit()




    
    
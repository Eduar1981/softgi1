class Ventas:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    # ----------------------------------------- VENTAS NORMALES -------------------------------------------------

    def crear_venta(self, venta):
        sql = f"INSERT INTO `ventas`(`cliente_factura`,`documento_operador`, `fechahora_venta`, `forma_pago`, `codigo_tabla`, `nombre_operador`, `apellido_operador`) VALUES ('{venta[0]}','{venta[1]}','{venta[2]}','{venta[3]}','{venta[4]}','{venta[5]}','{venta[6]}')"
        self.cursor.execute(sql)
        self.conexion.commit()

    def crearDetalleventa(self, venta):
        bsql = f"INSERT INTO `detalleventas`(`num_factura_venta`, `producto_factura`, `cantidad_productos_factura`, `valortotal_productos_factura`, `total_pagar_factura`) VALUES ('{venta[0]}','{venta[1]}','{venta[2]}','{venta[3]}','{venta[4]}')"
        self.cursor.execute(bsql)
        self.conexion.commit()

# ----------------------------------------- VENTAS A CREDITO ----------------------------------------------------

    def crear_venta_credito(self, venta):
            sql = f"INSERT INTO `ventas_credito`(`cliente`, `productos`, `credito_total`, `credito_restante`, `operador`, `fecha_venta`, `estado`) VALUES ('{venta[0]}','{venta[1]}','{venta[2]}','{venta[3]}','{venta[4]}','{venta[5]}','ACTIVO')"
            self.cursor.execute(sql)
            self.conexion.commit()

    def venta_cancelada_cred(self, contador):
            sql = f"UPDATE `ventas_credito` SET `estado`='PAGADA' WHERE contador = '{contador}'"
            self.cursor.execute(sql)
            self.conexion.commit()

    # abono por si se completa el credito
    def abono_completo(self, contador):
            sql = f"UPDATE `ventas_credito` SET `credito_restante`='{0}', `estado`='PAGADO' WHERE contador = '{contador}'"
            self.cursor.execute(sql)
            self.conexion.commit()

    # actualiza credito restante
    def actualiza_credito_rest(self, info):
            sql = f"UPDATE `ventas_credito` SET `credito_restante`='{info[0]}' WHERE contador = '{info[1]}'"
            self.cursor.execute(sql)
            self.conexion.commit()
        



# -----------------------------------------------------------------------------------------------------------------

 
        
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
    
    
            

    
    def editarDetalleventa(self, editar):
        bsql =f"UPDATE `detalleventas` SET `id_detalle_factura`='{editar[1]}',`num_factura_venta`='{editar[2]}',`producto_factura`='{editar[3]}',`cantidad_productos_factura`='{editar[4]}',`precio_productofactura`='{editar[5]}' WHERE id_detalle_factura"
        self.cursor.execute(bsql)
        self.conexion.commit()
        
    def eliminarDetalleventa(self,id_detalle_ventas):
        sql = f"DELETE FROM `detalleventas` WHERE  `id_detalle_factura`='{id_detalle_ventas}'"
        self.cursor.execute(sql)
        self.conexion.commit()




    
    
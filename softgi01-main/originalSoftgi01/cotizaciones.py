class Cotizaciones:
    def __init__(self, DB, app): 
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  
        self.cursor = self.conexion.cursor()
        
        
    def crearCotizaciones(self, registro):           
        sql = f"INSERT INTO `cotizaciones`(`cliente_cotizacion`, `documento_operador`, `nombre_operador`, `apellido_operador`, `fecha_inicio_cotizacion`, `fecha_fin_cotizacion`, `nombre_cliente_cotizacion`) VALUES ('{registro[0]}','{registro[1]}','{registro[2]}','{registro[3]}','{registro[4]}','{registro[5]}','{registro[6]}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        
        
    def editarCotizacion(self,editar):
        bsql = f"UPDATE `cotizaciones` SET num_cotizacion='{editar[0]}', documento_operador='{editar[1]}', documento_operador='{editar[2]}', nombre_operador='{editar[3]}', apellido_operador='{editar[4]}', fecha_inicio_cotizacion='{editar[5]}', fecha_fin_cotizacion='{editar[6]}', nombre_cliente_cotizacion='{editar[7]}' WHERE num_cotizacion='{editar[0]}'"
        self.cursor.execute(bsql)
        self.conexion.commit()
        

    def eliminarCotizacion(self,id_cotizaciones):
        sql = f"DELETE FROM `cotizaciones` WHERE num_cotizacion='{id_cotizaciones}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        

    def crearDetalleCotizacion(self, registrar):
        bsql = f"INSERT INTO `detallecotizaciones`(`num_cotizacion`, `producto_cotizacion`, `cantidad_productos_cotizacion`, `valorunidad_prodcotizacion`, `valortotal_cantidaproductos_cotizacion`, `servicio_cotizacion`, `cantidad_servicios_cotizacion`, `valorunidad_servicioscotizacion`, `valortotal_cantidadservicios_cotizacion`, `totalpagar_cotizacion`) VALUES ('{registrar[0]}','{registrar[1]}','{registrar[2]}','{registrar[3]}','{registrar[4]}','{registrar[5]}','{registrar[6]}','{registrar[7]}','{registrar[8]}','{registrar[9]}')"
        self.cursor.execute(bsql)
        self.conexion.commit()
    
    def editarDetalleCotizaciones(self, editar):
        bsql =f"UPDATE `detallecotizaciones` SET `id_detalle_cotizacion`='{editar[0]}',`num_cotizacion`='{editar[1]}',`producto_cotizacion`='{editar[2]}',`cantidad_productos_cotizacion`='{editar[3]}',`valorunidad_prodcotizacion`='{editar[4]}',`valortotal_cantidaproductos_cotizacion`='{editar[5]}',`servicio_cotizacion`='{editar[6]}',`cantidad_servicios_cotizacion`='{editar[7]}',`valorunidad_servicioscotizacion`='{editar[8]}',`valortotal_cantidadservicios_cotizacion`='{editar[9]}',`totalpagar_cotizacion`='{editar[10]}' WHERE `id_detalle_cotizacion`='{editar[0]}'"
        self.cursor.execute(bsql)
        self.conexion.commit()
        
    def eliminarDetalleCotizacion(self,id_detallecotizaciones):
        sql = f"DELETE FROM `detallecotizaciones` WHERE  `id_detalle_cotizacion`='{id_detallecotizaciones}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        
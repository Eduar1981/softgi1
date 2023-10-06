class Cotizaciones:
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()
        
        
    def crearCotizaciones(self, registro):           
        sql = f"INSERT INTO `cotizaciones`(`cliente_cotizacion`, `documento_operador`, `nombre_operador`, `apellido_operador`, `fecha_inicio_cotizacion`, `fecha_fin_cotizacion`, `nombre_cliente_cotizacion`) VALUES ('{registro[0]}','{registro[1]}','{registro[2]}','{registro[3]}','{registro[4]}','{registro[5]}','{registro[6]}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def editarCotizacion(self,editar):
        bsql = f"UPDATE `cotizaciones` SET documento_operador='{editar[0]}'OR documento_operador='{editar[1]}' OR nombre_operador='{editar[2]}' OR apellido_operador='{editar[3]}' OR fecha_inicio_cotizacion='{editar[4]}' OR fecha_fin_cotizacion='{editar[5]}' OR nombre_cliente_cotizacion='{editar[6]}'"
        self.cursor.execute(bsql)
        self.conexion.commit()
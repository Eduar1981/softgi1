from conexion import * #traiga todo a de conexion

class Ventas:
    def __init__(self, DB4FREE, app):
        self.mysql = DB4FREE
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def crear_venta(self, num_factura, cliente_factura, numero_cotizacion,documento_operador,fechahora_venta, forma_pago, medio_pago, detalles):
        # Crear una nueva venta en la tabla "VENTAS"
        query_ventas = "INSERT INTO VENTAS (num_factura, cliente_factura, numero_cotizacion, documento_operador, fechahora_venta, forma_pago, medio_pago) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores_ventas = (num_factura, cliente_factura, numero_cotizacion, documento_operador, fechahora_venta, forma_pago, medio_pago)

        try:
            self.cursor.execute(query_ventas, valores_ventas)
            self.conexion.commit()
            venta_id = self.cursor.lastrowid
        except Exception as e:
            return str(e)

        # Insertar detalles de la venta en la tabla "DETALLEVENTAS"
        for detalle in detalles:
            num_factura_venta = detalle.get('num_factura_venta', '')
            producto_factura = detalle.get('producto_factura', '')
            cantidad_productos_factura = detalle.get('cantidad_productos_factura', 0)
            precio_productofactura = detalle.get('precio_productofactura', 0.0)
            valortotal_productos_factura = detalle.get('valortotal_productos_factura', 0.0)
            servicio_factura = detalle.get('servicio_factura', '')
            cantidad_servicios_factura = detalle.get('cantidad_servicios_factura', 0)
            precio_serviciosfactura = detalle.get('precio_serviciosfactura', 0.0)
            valortotal_servicios_factura = detalle.get('valortotal_servicios_factura', 0.0)
            total_pagar_factura = detalle.get('total_pagar_factura', 0.0)

            query_detalles = """
                INSERT INTO DETALLEVENTAS 
                (venta_id, num_factura_venta, producto_factura, cantidad_productos_factura, precio_productofactura, 
                 valortotal_productos_factura, servicio_factura, cantidad_servicios_factura, precio_serviciosfactura, 
                 valortotal_servicios_factura, total_pagar_factura)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores_detalles = (venta_id, num_factura_venta, producto_factura, cantidad_productos_factura, precio_productofactura,
                              valortotal_productos_factura, servicio_factura, cantidad_servicios_factura, precio_serviciosfactura,
                              valortotal_servicios_factura, total_pagar_factura)

            try:
                self.cursor.execute(query_detalles, valores_detalles)
                self.conexion.commit()
            except Exception as e:
                return str(e)

        return "Venta creada exitosamente."

    def obtener_ventas(self):
        # Obtener todas las ventas de la tabla "VENTAS" con sus detalles de "DETALLEVENTAS"
        query = """
            SELECT VENTAS.num_factura, VENTAS.cliente_factura, VENTAS.numero_cotizacion, VENTAS.documento_operador, 
            VENTAS.fechahora_venta, VENTAS.forma_pago, VENTAS.medio_pago, DETALLEVENTAS.num_factura_venta, 
            DETALLEVENTAS.producto_factura, DETALLEVENTAS.cantidad_productos_factura, DETALLEVENTAS.precio_productofactura, 
            DETALLEVENTAS.valortotal_productos_factura, DETALLEVENTAS.servicio_factura, DETALLEVENTAS.cantidad_servicios_factura, 
            DETALLEVENTAS.precio_serviciosfactura, DETALLEVENTAS.valortotal_servicios_factura, DETALLEVENTAS.total_pagar_factura
            FROM VENTAS
            LEFT JOIN DETALLEVENTAS ON VENTAS.id = DETALLEVENTAS.venta_id
        """
        try:
            self.cursor.execute(query)
            ventas = self.cursor.fetchall()
            return ventas
        except Exception as e:
            return str(e)

    def eliminar_venta(self, venta_id):
        # Eliminar una venta y sus detalles por su ID
        query_eliminar_detalles = "DELETE FROM DETALLEVENTAS WHERE venta_id = %s"
        query_eliminar_venta = "DELETE FROM VENTAS WHERE id = %s"
        valores = (venta_id,)

        try:
            self.cursor.execute(query_eliminar_detalles, valores)
            self.cursor.execute(query_eliminar_venta, valores)
            self.conexion.commit()
            return "Venta eliminada exitosamente."
        except Exception as e:
            return str(e)
        
    def actualizar_venta(self, venta_id, num_factura, cliente_factura, numero_cotizacion, documento_operador, fechahora_venta, forma_pago, medio_pago, detalles):
        # Actualizar una venta en la tabla "VENTAS"
        query_ventas = """
            UPDATE VENTAS 
            SET num_factura = %s, cliente_factura = %s, numero_cotizacion = %s, documento_operador = %s, 
            fechahora_venta = %s, forma_pago = %s, medio_pago = %s 
            WHERE id = %s
        """
        valores_ventas = (num_factura, cliente_factura, numero_cotizacion, documento_operador, fechahora_venta, forma_pago, medio_pago, venta_id)

        try:
            self.cursor.execute(query_ventas, valores_ventas)
            self.conexion.commit()
        except Exception as e:
            return str(e)




    
    
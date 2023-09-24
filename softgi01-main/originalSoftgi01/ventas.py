from conexion import * # conexion con todo lo que hay en conexion.py


class Factura:
    def __init__(self, DB4FREE, app): #creo la clase
        self.mysql = DB4FREE
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    
    def crear_venta(self, venta):
        if request.method == 'POST': #creo la funcion para crear un nuevo cliente tomando los datos desde el formulario html
            num_factura = request.form[num_factura]
            factura_cliente = request.form[factura_cliente]
            factura_empleado = request.form[factura_empleado]
            tipo_venta = request.form[tipo_venta]
            fecha_venta = request.form[fecha_venta]
            cantidad_producto = request.form[cantidad_producto]
            total_pagar = request.form[total_pagar]
            medio_pago =request.form[medio_pago]
            forma_pago = request.form[forma_pago]

            if venta  != " " and not self.venta_existe(venta): # Ahora, verifica si venta no está vacío y si aún no está en la base de datos
                                                                # Si venta no está vacío y no existe en la DB, procede a insertar en la base de datos
                                                
                now = datetime.now() #Aquí, se obtiene la fecha y hora actual utilizando el módulo datetime
                tiempo = now.strftime("%Y%m%d%H%M%S") # Con la fecha y hora actual, se crea una cadena de texto formateada como "AñoMesDíaHoraMinutoSegundo". Por 
                                                        #ejemplo, si la fecha actual es 2023-09-14 15:30:45, 
                                                        # tiempo sería "20230914153045".

                sql = f"INSERT INTO ventas (num_factura, factura_cliente, factura_empleado, tipo_venta, fecha_venta, cantidad_producto, total_pagar, medio_pago, forma_pago) VALUES  ('{num_factura}', '{factura_cliente}', '{factura_empleado}', '{tipo_venta}','{fecha_venta}', '{cantidad_producto}', '{total_pagar}', '{medio_pago}', '{forma_pago}')"                                      
                                                          
                self.cursor.execute(sql)
                self.conexion.commit()
            else:
                return "Venta vacía o ya existe en la base de datos"

    def venta_existe_en_db(self, venta):
    
        sql = f"SELECT COUNT(*) FROM ventas WHERE num_factura = '{venta}'" # Realiza una consulta SQL para verificar si existe una venta con el mismo número de factura en la base de datos
                                                                            
        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if resultado[0] > 0:  # Si el resultado es mayor que cero, significa que ya existe una venta con el mismo número de factura
                              
            return True
        else:
            return False       


'''posibles campos en la DB, numero_factura, factura_cliente, factura_empleado, tipo_venta, fecha_venta, 
cantidad_producto, total_pagar, medio_pago, forma_pago'''
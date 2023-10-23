from conexion import * # conexion con todo lo que hay en conexion.py


class Factura:
    def __init__(self, DB4FREE, app): #creo la clase
        self.mysql = DB4FREE
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    
    

class Proveedores:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    #Crear provedores
    def crear(self, agregar):
        bsdsql = F" INSERT INTO `proveedores`(`doc_proveedor`, `nom_proveedor`, `contacto_proveedor`, `email_proveedor`, `direccion_proveedor`, `ciudad_proveedor`, `registro_proveedor`, `operador_proveedor`, `estado_proveedor` ) VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}', '{agregar[5]}', '{agregar[6]}', '{agregar[7]}','ACTIVO')"
        self.cursor.execute(bsdsql)
        self.conexion.commit()


    #modificar Proveedores
    def modificar(self,proveedor):
        sql=f"UPDATE proveedores SET doc_proveedor='{proveedor[0]}',nom_proveedor='{proveedor[1]}',contacto_proveedor='{proveedor[2]}',email_proveedor='{proveedor[3]}', direccion_proveedor='{proveedor[4]}' ciudad_proveedor='{proveedor[5]}' WHERE doc_proveedor='{proveedor[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()

    #Eliminar proveedores
    def borrar(self,documentoProveedores):
        sql=f"UPDATE proveedores SET estado_proveedor='INACTIVO' WHERE doc_proveedor='{documentoProveedores}'"
        self.cursor.execute(sql)
        self.conexion.commit()

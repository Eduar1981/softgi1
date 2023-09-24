
class Proveedores:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    #Crear provedores
    def crear(self, agregar):
        bsdsql = F" INSERT INTO `proveedores`(`docprov`, `nomprov`, `contprov`, `emaprov`, `direprov`, `estado`) VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}','ACTIVO')"
        self.cursor.execute(bsdsql)
        self.conexion.commit()


    #modificar Proveedores
    def modificar(self,proveedor):
        sql=f"UPDATE proveedores SET docprov='{proveedor[0]}',nomprov='{proveedor[1]}',contprov='{proveedor[2]}',emaprov='{proveedor[3]}', direprov='{proveedor[4]}' WHERE docprov='{proveedor[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()

    #Eliminar proveedores
    def borrar(self,documentoProveedores):
        sql=f"UPDATE proveedores SET estado='INACTIVO' WHERE docprov='{documentoProveedores}'"
        self.cursor.execute(sql)
        self.conexion.commit()

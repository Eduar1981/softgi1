class manejoUsuarios():
    def __init__(self, DB, app):  # Recibe mysql y app como parámetros
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()
        
    def registroUsuarios(self, registro):
        bsq = f"INSERT INTO `empleados`(`doc_empleado`, `nom_empleado`, `ape_empleado`, `fecha_nacimiento_empleado`, `contacto_empleado`, `email_empleado`, `direccion_empleado`, `ciudad_empleado`, `contrasena`, `rol`, `fechahora_registroempleado`) VALUES ('{registro[0]}','{registro[1]}','{registro[2]}','{registro[3]}','{registro[4]}','{registro[5]}','{registro[6]}','{registro[7]}','{registro[8]}','{registro[9]}','{registro[10]}')"
        self.cursor.execute(bsq)
        self.conexion.commit()
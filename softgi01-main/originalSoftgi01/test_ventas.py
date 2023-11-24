
from conexion import *







def test_agrega_venta():

    # generador de codigo 
    lower = string.ascii_lowercase       
    upper = string.ascii_uppercase 
    num = string.digits 
    chars = lower + upper + num
    codigo = random.sample(chars, 20)
    codigo_2 = ""  # variable que guarda el codigo
    for c in codigo:
        codigo_2+=c

    tiempo_venta = datetime.datetime.now()

    info_venta = [1213145566, 1086358507,tiempo_venta,"efectivo",codigo_2,"dennis","Echeverri"]
    ventas.crear_venta([info_venta[0], info_venta[1], info_venta[2], info_venta[3], info_venta[4], info_venta[5], info_venta[6]])

    # consulto el num_factura en tabla ventas
    sql = f"SELECT `num_factura` FROM `ventas` WHERE codigo_tabla = '{codigo_2}'"
    conn = mysql.connect()
    cursor = conn.cursor()     
    cursor.execute(sql)
    num_factura = cursor.fetchall()
    conn.commit()

    assert len(num_factura) == 1

    """ info_detalle_v = [num_factura[0][0],"vidrios",10,200000,10000]
    # Insertacion en la tabla detalleventas 
    ventas.crearDetalleventa([num_factura[0], num_factura[1], num_factura[2], num_factura[3], num_factura[4]]) """
from conexion import * #Importo la conexion de la base de datos y las funciones de flask, que en este caso se encuentra en el archivo conexion.py 
from clientes import Clientes  # Importa la clase Clientes desde clientes.py
from categorias import Categorias




@app.route('/') # Inicio la ruta princimpla del programa en este caso home que me muestra como pagina principal un login
def registro(): # Defino la funcion de la ruta principal en este caso la funcion se llama registro
    return redirect('/home') # Retorno o lo devuelvo la ruta home para que me muestre la pagina segun la definicion

def generate_token(length=32): # Esta funcion genera un token de 32 caracteres el token generado se utiliza para enviar un token unico a cada usuario registrado 
    characters = string.ascii_letters + string.digits  # defino esta variable con pertenecias de caracteres especiales permitiendo letras ascii en mayusculas y minusculas y numeros haciendo que cada token sea generado de manera impredecible 
    token01 = ''.join(secrets.choice(characters) for _ in range(length)) # Genero la cadena o el token aleatorio y lo guardo en la variable token01
    return token01 # Retorno o lo devuelvo la variable token01 para ver su resultado en este caso esta comentado por que nomas era una prueba


@app.route('/registroF') # defino la ruta de registro
def registroF(): # defino la funcion de la ruta de registro llamada registroF
    return render_template('/registro_usuario.html') # lo retorno o lo devuelvo al html de registro de usuario en este caso el archivo registro_usuario.html y para eso se untiliza render_template


# Ruta de registro de usuario
@app.route('/registro', methods=['POST']) # defino la ruta que me envia los datos ingresado en el formulario a la base de datos con el metodo post que se utiliza para envio de datos 
def registro_usuario(): #defino la funcion de la ruta 
    
    conn = mysql.connect() # Uso mysql.connect para conectar o hacer la conexion con la base de datos, mysql.connect es una de las funciones que utliza flask para conectarse a una base de datos
    cursor = conn.cursor() # Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    doc_empleado = request.form['documento'] # Utilizo request.form Para trear los datos dijitados en el formulario y la variable docempl la almacena
    nom_empleado = request.form['nombre']# Utilizo request.form Para traer los datos dijitados en el formulario y la variable nomempl la almacena
    ape_empleado = request.form['apellido']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable apempl la almacena
    email_empleado = request.form['correo']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable emaempl la almacena
    rol = request.form['rol']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable rol la almacena
    
    # Validación del correo electrónico
    if not re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_empleado):# Hago una toma de desicion donde el correo no tenga los carateres suficiente q se les requieren muestre un mensaje de error 
        return render_template('/registro_usuario.html', flash="Correo electrónico inválido. Intente nuevamente.") # muestra el mesaje de la toma de desiciones anterior
    
    clave1 = request.form['contrasena'] # Utilizo request.form Para trear los datos dijitados en el formulario y la variable clave1 la almacena
    clave2 = request.form['confirmada']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable clave2 la almacena
    if clave1 == clave2: # Comparo las contraseñas digitadas para confirmar si coinciden 
        cifrada = hashlib.sha512(clave1.encode("utf-8")).hexdigest() # Cifro la contraseña con el metodo hashlib 
        consul = f"SELECT * FROM empleados WHERE doc_empleado='{doc_empleado}' OR email_empleado='{email_empleado}'"# Consulto en la base de dato que el usuario digitado no  exista ni su correo ni su numero de documento
        cursor.execute(consul)# Ejecuto la consulta de la base de dato
        resultado_1 = cursor.fetchone() # guardo los datos de la consulta que se hizo 
        if resultado_1 is not None: # hago una toma de desicion que donde la consulta resultado tiene dato o no esta vacia me haga el siguiente metodo
            flash('Este usuario ya ha sido registrado') # que envie este mensaje para que el usuario lo vea 
            return redirect(url_for('home'))# me retorne o me devuelva a la pagina home en este caso utilizo redirect(url_for('home')) para que me redirija desde python a esa funcion llamada home
        else: # en caso de que la consulta hecha no exista en la base de datos que me tome la siguiente desicion
            mi_token2 = generate_token()  # agrego a la variable mi_token2 la funcion generar token, cada vez que se quiera resgistrar un suario nuevo se genera un token nuevo ya q se ejecuta la funcion generate_token()

            # Envía el correo de confirmación
            enviar_correo_confirmacion(nom_empleado, email_empleado, mi_token2)# ejecuto la funcion de enviar_correo_confirmacion(nom_empleado, email_empleado, mi_token2) enviado 3 variables que son nom_empleado, email_empleado, mi_token2 para enviar como imformacion al correo segun definido en la variable email_empleado con un token unico y el nombre de la persona q se le envia el correo
            
            
            sql = "INSERT INTO empleados (doc_empleado, nom_empleado, ape_empleado, email_empleado, contrasena, rol ) VALUES ( %s, %s, %s, %s, %s, %s)"# Inserto o registro los datos en la base de datos en la tabla empleados 
            cursor.execute(sql, (doc_empleado, nom_empleado, ape_empleado, email_empleado, cifrada, rol)) # ejecuto el registro hecho 
            conn.commit()#hago un conn.commit confirmando la transacción actual
            
            fecha_registro = datetime.datetime.now()#la variable fecha _registro obtiene el tiempo hora fecha año y segundo que estas actual
            tok = f"INSERT INTO tokens (doc_empleado, nom_empleado, email_empleado, token, confir_user, tiempo_registro) VALUES ('{doc_empleado}', '{nom_empleado}', '{email_empleado}','{mi_token2}', 'no confirmado', '{fecha_registro}' )" # Inserto o registro los datos en la base de datos en la tabla tokens
            cursor.execute(tok)# ejecuto el registro hecho
            conn.commit()#hago un conn.commit confirmando la transacción actual
            conn.close()# Utilizamos esta funcion para cerrar la conexion aunque la conexion se ciera sola cuando sale de alcance
            ###flash('Tu usuario ha sido registrado exitosamente') # mostramos este mensaje donde el registro sea exitoso
            flash("Se envio un correo para confirmar tu registro, revisa la bandeja de entrada o spam")# mostramos un mensaje donde el registro sea exitoso y le idicamos que se envio un correo
            return render_template('login.html')# se envia a login.html ya cumplido todo
            

            """ # Insertar los datos del usuario en la base de datos 
            sql = "INSERT INTO empleados (docempl, nomempl, apeempl, emaempl, contrasena, rol, conemail,  token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (docempl, nomempl, apeempl, emaempl, cifrada, rol, 'sin_confirmar', mi_token2))
            conn.commit()
            conn.close()
            flash('Tu usuario ha sido registrado exitosamente')
            return render_template('login.html') """
            
    else:# en el caso de que las contraseña no considan se aplicara esta desicion
        flash('la contraseña no coincide')# muestra un mensaje indicando lo sucedido
        return redirect(url_for('/registro_usuario'))# redirige  a la la funcion de registro_usuario


# Función para enviar el correo de confirmación
def enviar_correo_confirmacion(nombre, email, token):#Esta funcion recibe lo enviando en las variable nomempl, emaempl, mi_token2 para enviar como imformacion al correo 
    confirm_url = url_for('confirmar_correo', token=token, email=email, _external=True)# genero el link agregandole el token unico y el email digitado 
    render_html = render_template('correoMsj.html', nombre=nombre, correo_url=confirm_url)# Creo una variable que me trae el mesaje de un html en este caso correoMsj.html que va hacer el envio que se va hacer al correo
    msg = Message('Confirmación de correo electrónico', sender='jenasoft05@gmail.com', recipients=[email])#defino el titulo el correo que envia y al correo q va ser enviado el mesaje 
    msg.html =  render_html # agrego el mensaje que va a llegar al correo y su informacion segun dada
    mail.send(msg)# envio el mensaje al correo 
        
        

# Ruta de confirmación de correo electrónico    
@app.route('/confirmar_correo/<token>', methods=['GET', 'POST'])# ruta de confirmacion  de correo recibe el token segun el correo y pongo el metdo recibir y enviar GET y POST
def confirmar_correo(token): #declaro la funcion con el nombre confirma_correo
    cursor = mysql.get_db().cursor()
    # Consulto el usuario que tiene tiene el token que se envio segun el correo 
    cursor.execute("SELECT doc_empleado, nom_empleado, email_empleado, confir_user FROM tokens WHERE token = %s", (token,)) #ejecuto la consulta 
    usuario_data = cursor.fetchone() # agrego el resultado de la consulta a la variable usuario_data
    if not usuario_data: # # esta toma de desicion se aplica si el usuario no tiene token 
            flash('El token de confirmación no es válido.', 'danger') # le indico el mensaje al usuario
            return redirect(url_for('home')) # redirijo a la pagina home

    email = usuario_data[2] # Almaceno  el campo email_empleado de la base de datos a la variable email
    correo_confirmado = usuario_data[3] # Almaceno el campo confir_user de la base de dato a la variable correo_confirmado

    if correo_confirmado == 'confirmado':# toma de desicion que se aplica en el caso de que el correo este confirmado
        flash('El correo ya ha sido validado.', 'danger')# le indico el mensaje
        return redirect(url_for('home'))# redirijo a la pagina home
    
    #en caso tal de que no se apliquen los metodos anteriores 
    if request.method == 'POST': # Verifico si la solicitud HTTP es un método POST
        confi= request.form['confir'] # Utilizo request.form Para traer los datos dijitados en el formulario
        # Actualizar el estado de correo a "confirmado"
        cursor.execute(f"UPDATE tokens SET confir_user = '{confi}' WHERE email_empleado = '{email}'") # ejecuto la atualizacion a la base de datos
        mysql.get_db().commit()# obtengo la conexion a la base de dato y confirmo los cambio
        flash('Tu correo ha sido confirmado correctamente.', 'success')# le indico un mensaje
        return redirect(url_for('home'))# redirijo a la pagina home
    
    return render_template('confirmar.html')# renderizo a la pagina confirmar.html



#--------------------------------------------------Inicio de sesion------------------------------------------------------------------------------------------------

@app.route('/inicio')# Ruta de inicio
def inicio(): # hago la funcion de la ruta en este caso su nombre es inicio
    if "email_empleado" in session:# verifico que se alla iniciado sesion
        return render_template('index.html') # renderizo a la pagina inicioexitoso.html
    else: # de lo contrario que no haya inicado sesion
        flash('Algo está mal en sus datos digitados') # indico un mensaje 
        return redirect(url_for('home')) # redirijo a la pagina home


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')# Ruta de home
def home():# hago la funcion de la ruta en este caso su nombre es home
    return render_template('login.html')# rederizo a la pagina login.html

@app.route('/login', methods=["POST"])# Ruta de login
def login():# hago la funcion de la ruta en este caso su nombre es login
    email = request.form['correo'] # Utilizo request.form Para trear los datos dijitados en el formulario
    password = request.form['contrasena'] # Utilizo request.form Para trear los datos dijitados en el formulario
    connt = mysql.connect()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cursor = connt.cursor()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cifrado = hashlib.sha512(password.encode('utf-8')).hexdigest()# Cifro la contraseña con el metodo hashlib 

    """ bsql_emp = f"SELECT email_empleado='{email}', contrasena='{cifrado}' FROM empleados WHERE conemail='confirmado'" """

    bsql_emp = f"SELECT empleados.email_empleado, empleados.contrasena='{cifrado}', tokens. confir_user  FROM empleados INNER JOIN tokens ON empleados.doc_empleado = tokens.doc_empleado WHERE empleados.email_empleado  = '{email}'"
    cursor.execute(bsql_emp)# ejecuto la consulta 
    resultado = cursor.fetchone()# agrego el resultado de la consulta a la variable resultado
    if resultado is not None:# hago una toma de desicion que donde la consulta resultado tenga dato o no esta vacia me haga el siguiente metodo
        if resultado[2] == 'confirmado':# toma de desicion que se aplica en el caso de que el correo este confirmado 
            session["email_empleado"] = resultado[0]# Utilizo session para guardar la informacion de la persona ingresada
            return redirect(url_for('inicio'))#redirijo 
        else:
            flash("No has confirmado tu cuenta, por favor revisa la bandeja de entrada o spam", category="danger")
            return redirect(url_for('home'))
    else:
        flash('Algo esta mal en tus credenciales o tu correo no ha sido confirmado.', 'success')
        return redirect(url_for('home'))
    
    
    
#--------------------------------------------------recuperacion de contraseña------------------------------------------------------------------------------------------------

# Clase User definida previamente
class User:# creo una clase User que la utlizare para crear objetos en este caso User se esta utilizado como plantilla
    def __init__(self, id, email, nombre):# defino el metodo, con sus parametro y los argumentos 
        self.id = id # hago una copia propia de la variable id
        self.email = email  # hago una copia propia de la variable email
        self.nombre = nombre  # hago una copia propia de la variable nombre
        
class PasswordResetToken:# creo una clase User que la utlizare para crear objetos en este caso PasswordResetToken se esta utilizado como plantilla
    def __init__(self, userio_id):# defino el metodo, con sus parametros y los argumentos 
        self.userio_id = userio_id # hago una copia propia de la variable usuario_id
        
        
        
# Función para enviar correos electrónicos de restablecimiento de contraseña
def envio_correo(user, token_rctsn):
    token_url = url_for('recuperar_contraseña', token_rctsn=token_rctsn, user=user, _external=True)
    print(token_url)
    rendered_html = render_template('correoEnv.html', user=user, token_url=token_url)
    msg = Message('Recuperación de contraseña', sender='jenasoft05@gmail.com', recipients=[user.email])
    msg.html = rendered_html
    mail.send(msg)



# Ruta para solicitar el restablecimiento de contraseña
@app.route('/solicitarCambio_contraseña', methods=['GET', 'POST'])
def solicitarCambio_contraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = mysql.get_db().cursor()
        msql = f"SELECT * FROM empleados  WHERE email_empleado  = '{email}'"
        cursor.execute(msql)
        userio_data = cursor.fetchone()

        if userio_data:
            userio = User(id=userio_data[0], email=userio_data[3], nombre=userio_data[1])
            

            cursor = mysql.get_db().cursor()

            # Verificar si hay registros en la tabla recuperarcontrasena para ese correo electrónico
            cursor.execute("SELECT * FROM recuperarcontrasena WHERE email_usuario = %s", (userio.email,))
            existing_token = cursor.fetchone()
            token_recuperar = token_recuperar_contrasena()  #Token que se genera para cambio de contraseña
            """ if existing_token:
                # Si ya existe un token para ese correo, actualiza su fecha de vencimiento
                expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
                cursor.execute("UPDATE recuperarcontrasena SET fechahora_solicitud= %s, fechahora_termina = %s, codigo = %s WHERE email = %s", (datetime.datetime.now(),expiration_time, token_recuperar, userio.email))
            else:
                # Si no existe un token para ese correo, crea uno nuevo
                expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
                cursor.execute("INSERT INTO recuperarcontrasena (id_solicitud, email_usuario, fechahora_solicitud, fechahora_termina, codigo, usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                                (userio.nombre, userio.email, datetime.datetime.now(), expiration_time, token_recuperar, userio.id)) """
            # Si no existe un token para ese correo, crea uno nuevo
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
            cursor.execute("INSERT INTO recuperarcontrasena (id_solicitud, email_usuario, fechahora_solicitud, fechahora_termina, codigo, usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                            (userio.nombre, userio.email, datetime.datetime.now(), expiration_time, token_recuperar, userio.id)) 
            mysql.get_db().commit()
            
            
            envio_correo(userio, token_recuperar)
            print(userio, token_recuperar)
            flash('Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.', 'success')
            return redirect(url_for('home'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.', 'danger')

    return render_template('recuperar_contrasena.html')


# Función para generar un token aleatorio
def token_recuperar_contrasena(length=32):
    characters = string.ascii_letters + string.digits  # Caracteres permitidos en el token
    token02 = ''.join(secrets.choice(characters) for _ in range(length))
    return token02


# Ruta para restablecer la contraseña
@app.route('/recuperar_contraseña/<token_rctsn>', methods=['GET', 'POST'])
def recuperar_contraseña(token_rctsn):
    print(f"Token recibido: {token_rctsn}")
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT  fechahora_termina, codigo, usuario FROM recuperarcontrasena WHERE codigo  = %s", (token_rctsn,))
    datos_db = cursor.fetchone()

    if not datos_db:
        flash('El token de confirmación no es válido.', 'danger')
        return redirect(url_for('solicitarCambio_contraseña'))
    
    usuario = datos_db[2]
    codigo = datos_db[1]

    expiration_time = datos_db[0]  # Obtener la fecha de vencimiento del token desde la base de datos
    current_time = datetime.datetime.now()
    if current_time > expiration_time:
        # El token ha caducado, mostrar un mensaje de error
        flash('El enlace de restablecimiento de contraseña ha caducado.', 'danger')
        return redirect(url_for('solicitarCambio_contraseña'))

    if request.method == 'POST':
        password = request.form.get('password')
        cifrado = hashlib.sha512(password.encode('utf-8')).hexdigest()

        cursor.execute("UPDATE empleados SET contrasena  = %s WHERE doc_empleado = %s", (cifrado, usuario))
        cursor.execute("UPDATE recuperarcontrasena SET usuario='si' WHERE codigo = %s", (codigo))
        mysql.get_db().commit()

        flash('Tu contraseña ha sido restablecida.', 'success')
        return redirect(url_for('home'))

    return render_template('reset_password.html')

#-----------------conexión de la clase cliente------------------

@app.route("/clientes")
def clientes():
    if "email_empleado" in session: 
        sql = "SELECT * FROM clientes WHERE estado_cliente ='ACTIVO'"
        conn = mysql.connect()                    # muestra los clientes
        cursor = conn.cursor()
        cursor.execute(sql)                                          
        resultado = cursor.fetchall()
        return render_template('/clientes/muestraclientes.html', resulta=resultado)
    else:
                flash('Algo esta mal en sus datos digitados')
                return redirect(url_for('home'))


@app.route("/crearClientes")
def crearClientes():
    if "email_empleado" in session:                                
        return render_template('clientes/registrocliente.html')        #crea clientes
    else:
            flash('Algo esta mal en sus datos digitados')
            return redirect(url_for('home'))
    
@app.route("/crear_cliente", methods=['POST'])
def crear_cliente():
    if "email_empleado" in session:

        doc_cliente = request.form['doc_cliente']
        nom_cliente = request.form['nom_cliente']
        ape_cliente = request.form['ape_cliente']
        contacto_cliente = request.form['contacto_cliente']
        email_cliente = request.form['email_cliente']
        direccion_cliente = request.form['direccion_cliente']
        ciudad_cliente = request.form['ciudad_cliente']
        tipo_persona = request.form['tipopersona']                 #crea clientes
        tiempo = datetime.datetime.now()
        

        if not losClientes.buscar_cliente(doc_cliente):
            losClientes.crear_cliente([doc_cliente, nom_cliente, ape_cliente, contacto_cliente, email_cliente, direccion_cliente, ciudad_cliente, tipo_persona, tiempo])
            return redirect('/clientes')
        else:
            mensaje="Cliente ya existe"
            cliente =[doc_cliente, nom_cliente, ape_cliente, contacto_cliente, email_cliente, direccion_cliente, ciudad_cliente, tipo_persona]
            return render_template('clientes/muestraclientes.html', mensaje=mensaje, cliente=cliente)
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    

@app.route("/editarClientes/<documento>")
def edit_cliente(documento):
    if "email_empleado" in session:
        sql = f"SELECT * FROM clientes WHERE doc_cliente = '{documento}'"
        conn = mysql.connect()
        cursor = conn.cursor()                                    #muestra toda la informacion y pone en los imputs
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        return render_template("/clientes/edita_clientes.html", resul=resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

@app.route("/Actualizar_clie", methods=['POST','GET'])
def Actualizar_clie():
    if "email_empleado" in session:
        doc_cliente = request.form['doc_cliente']
        nom_cliente = request.form['nom_cliente']
        ape_cliente = request.form['ape_cliente']
        fecha_nacimiento_cliente = request.form['fecha_nacimiento_cliente']
        contacto_cliente = request.form['contacto_cliente']
        email_cliente = request.form['email_cliente']
        direccion_cliente = request.form['direccion_cliente']
        ciudad_cliente = request.form['ciudad_cliente']
        tipo_persona = request.form['tipo_persona']  
        losClientes.modificar_cliente([doc_cliente, nom_cliente, ape_cliente, fecha_nacimiento_cliente, contacto_cliente, email_cliente, direccion_cliente, ciudad_cliente, tipo_persona])
        return redirect('/clientes')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

    
@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    if "email_empleado" in session:
        if request.method == 'POST':
            busqueda = request.form['busqueda']
            # Realiza la consulta en la base de datos utilizando MySQL y Flask-MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM clientes WHERE nom_cliente LIKE %s", (f"%{busqueda}%",))   #buscador de clientes
            resultados = cursor.fetchall()
            conn.close()
            return render_template('registroclientes.html', resultados=resultados) # Envía los resultados al mismo formulario de registroclientes.html
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    
@app.route('/borracliente/<documento>')
def borrarcliente(documento):
    if "email_empleado" in session:
        losClientes.borrar_cliente(documento)
        return redirect('/clientes')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))





#---------------------------------------------- Provedores ------------------------------------------------ 

@app.route("/muestra_info_prov/<doc_proveedor>")   # muestra info del proveedor y la envia a los imputs en actualizar
def muestra_info_prov(doc_proveedor):
    if "email_empleado" in session:
        documento = doc_proveedor
        sql = f"SELECT doc_proveedor, nom_proveedor, contacto_proveedor, email_proveedor, direccion_proveedor, ciudad_proveedor FROM proveedores WHERE doc_proveedor='{documento}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()               # no me toque el codigo niche pleace
        return render_template("/provedor/actualizar_proveedores.html", resul = resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))


@app.route("/modificarprovee", methods=['POST', 'GET'])
def modificarprovee():
    if "email_empleado" in session:
        documento = request.form['documentoProveedor']
        nombre = request.form['nombreProveedor']
        numero = request.form['numeroProveedores']
        correo = request.form['correoProveedores']                           
        direccion = request.form['direccionProveedores']
        ciudad = request.form['ciudadProveedor']
        proveedores.modificar([documento,nombre,numero,correo,direccion,ciudad])
        return redirect('/muestra_Proveedores')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
 

@app.route('/borraprovee/<doc_proveedor>')
def borraprovee(doc_proveedor):
    if "email_empleado" in session:
        proveedores.borrar(doc_proveedor)                        #borra proveedor
        return redirect("/muestra_Proveedores")
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))




#-----------------------------------------------------------Crear proveedores---------------------------------------
@app.route('/proveedoress')
def proveedoress():
    if "email_empleado" in session:
        return render_template('/provedor/proveedore.html')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))



@app.route('/crearProveedores', methods=['POST'])
def crearProveedores():
    if "email_empleado" in session:
        documento = request.form['documentoProveedor']
        nombre = request.form['nombreProveedor']
        numero = request.form['numeroProveedores']
        correo = request.form['correoProveedores']
        direcion = request.form['direccionProveedores']
        ciudad = request.form['ciudadProveedor']
        tiempo = datetime.datetime.now()

        proveedores.crear([documento,nombre,numero,correo,direcion,ciudad, tiempo])
        return redirect('/muestra_Proveedores')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    
    
#-----------------------------------------------------------mostrar proveedores---------------------------------------

@app.route('/muestra_Proveedores')
def muestra_Proveedores():
    if "email_empleado" in session:
        sql = "SELECT * FROM `proveedores` WHERE estado_proveedor='ACTIVO'"           # consulta toda la info de proveedores.
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()   # no me toque el codigo niche pleace
        conn.commit()
        if (len(resultado) >= 1):
            return render_template("/provedor/muestra_proveedores.html", resul=resultado)   # si hay resultados se muestran.
        else:
            resultado2 = "No hay proveedores registrados"
            return render_template("/provedor/muestra_proveedores.html", resul2=resultado2)
    # sino se muestra el mensaje de resultado2.
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    


#----------------------------------------------Crud de categorías------------------------------------------------ 

@app.route("/categorias")
def categorias():
    sql = "SELECT * FROM categorias"
    conn = mysql.connect()                    # muestra las categorias
    cursor = conn.cursor()
    cursor.execute(sql)                                          
    resultado = cursor.fetchall()
    return render_template('/categorias/muestracategorias.html', resulta=resultado)


@app.route("/crearCategorias")
def crearCategoria():                                
    return render_template('categorias/registrar_categorias.html')        #crea categorias
    
@app.route("/registrar_categorias", methods=['POST'])
def registrar_categorias():
    if "email_empleado" in session:
        nombre_categoria = request.form['nom_categoria']#crea clientes
        """ now = datetime.now()
        tiempo = now.strftime("%Y%m%d%H%M%S")
        """
        return render_template('/muestracategorias/registrado.html')
    else:
        flash('Algo esta mal en sus datos digitados')
        return redirect(url_for('home'))
    
        
'''
@app.route("/editarClientes/<documento>")
def edit_cliente(documento):
    sql = f"SELECT * FROM clientes WHERE docclie = '{documento}'"
    conn = mysql.connect()
    cursor = conn.cursor()                                    #muestra toda la informacion y pone en los imputs
    cursor.execute(sql)
    resultado = cursor.fetchall()
    conn.commit()
    return render_template("/clientes/edita_clientes.html", resul=resultado[0])

@app.route("/Actualizar_clie", methods=['POST','GET'])
def Actualizar_clie():
    docclie = request.form['docclie']
    nomclie = request.form['nomclie']
    apeclie = request.form['apeclie']                # actualiza la info de clientes
    contclie = request.form['contclie']
    emaclie = request.form['emaclie']
    direclie = request.form['direclie']
    tipopersona = request.form['tipopersona']  
    losClientes.modificar([docclie,nomclie,apeclie,contclie,emaclie,direclie,tipopersona])
    return redirect('/clientes')

    
@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        # Realiza la consulta en la base de datos utilizando MySQL y Flask-MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM clientes WHERE nombre LIKE %s", (f"%{busqueda}%",))   #buscador de clientes
        resultados = cursor.fetchall()
        conn.close()
        return render_template('registroclientes.html', resultados=resultados) # Envía los resultados al mismo formulario de registroclientes.html
    
@app.route('/borracliente/<documento>')
def borrarcliente(documento):
    losClientes.borrar_cliente(documento)
    return redirect('/clientes')

'''


                                        
#----------------------------------------------Crud de productos------------------------------------------------ 

@app.route('/productos')
def crear_producto():
    if "email_empleado" in session:
        sql = "SELECT * FROM productos WHERE estado_producto = 'ACTIVO' "
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template('/productos/muestra_productos.html', resulta=resultado)
    else:
            flash('Algo esta mal en sus datos digitados')
            return redirect(url_for('home'))
    
""" 
@app.route('/crearProductos')
def crearProductos():
        if "email_empleado" in session:
            return render_template('productos/registrar_productos.html')
        else:
            flash('Algo esta mal en los datos digitados')
            return redirect(url_for('home'))
    
@app.route('/crearProductos', methods=['POST'])
def crearProductos():
    if "email_empleado" in session:
        return render_template('productos/registro_productos.html')
    else:
        flash('Algo esta mal en los datos digitados')
        return redirect(url_for('home'))
     """

        
@app.route("/crearProducto", methods=['POST'])
def crearProductos():
    if "email_empleado" in session:
        id_producto = request.form['id_producto']
        referencia_producto = request.form['referencia_producto']
        cantegoria = request.form['cantegoria']
        proveedor = request.form['proveedor']
        nombre_producto = request.form['nombre_producto']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        cantindad_producto = request.form['cantidad_producto']
        descipcion = request.form['descripcion']
        stockminimo = request.form['stockminimo']
        estado_producto = request.form['estado_producto']
        ubicacion = request.form['ubicacion']
        estante = request.form['estante']
        operador_producto = request.form['operador_producto']
        tiempo = datetime.datetime.now()

        productos.crear([id_producto,referencia_producto,cantegoria,proveedor,nombre_producto,precio_compra,precio_venta,cantindad_producto,descipcion,stockminimo,estado_producto,ubicacion,estante,operador_producto])
        return redirect('/muestra_productos')
    else:
        flash('Algo esta mal en los datos digitados')

        """ if not losProductos.buscar_producto(id_producto):
            losProductos.crearProducto([id_producto, referencia_producto, cantegoria, proveedor, nombre_producto, precio_compra, precio_venta, cantindad_producto, descipcion, stockminimo, estado_producto, ubicacion, estante, operador_producto])
            return redirect('/productos') """

""" @app.route('/muestra_productos')
def muestra_Productos():
    if "email_empleado" in session:
        sql = "SELECT * FROM `productos` WHERE estado_producto ='ACTIVO'"           # consulta toda la informacion de productos.
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()  
        conn.commit()
        if (len(resultado) >= 1):
            return render_template("/productos/muestra_productos.html", resul=resultado)   # si hay resultados se muestran.
        else:
            resultado2 = "No hay productos registrados"
            return render_template("/productos/muestra_productos.html", resul2=resultado2)
    # sino se muestra el mensaje de resultado2.
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))      


@app.route('/borra_produc/<idprod>')
def borra_produc(id_producto):
    if "email_empleado" in session:
        Crudproductos.borrar(id_producto)        # Eliminar productos
        return redirect("/muestra_productos")   
    else:
        flash('Algo esta mal en los datos digitados')
        return redirect(url_for('home'))
 """
@app.route('/muestra_productos')
def muestra_Productos():
    if "email_empleado" in session:
        sql = "SELECT * FROM productos WHERE estado_producto ='ACTIVO'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        if len(resultado) >= 1:
            return render_template("/productos/muestra_productos.html", resul=resultado)
        else:
            resultado2 = "No hay productos registrados"
            return render_template("/productos/muestra_productos.html", resul2=resultado2)
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

@app.route('/crear_producto', methods=['GET', 'POST'])
def crearProducto():
    if "email_empleado" in session:
        if request.method == 'POST':
            id_producto = request.form['id_producto']
            referencia_producto = request.form['referencia_producto']
            categoria = request.form['categoria']
            proveedor = request.form['proveedor']
            nombre_producto = request.form['nombre_producto']
            precio_compra = request.form['precio_compra']
            precio_venta = request.form['precio_venta']
            cantidad_producto = request.form['cantidad_producto']
            descripcion = request.form['descripcion']
            stockminimo = request.form['stockminimo']
            estado_producto = 'ACTIVO'  # Se establece como 'ACTIVO' por defecto
            ubicacion = request.form['ubicacion']
            estante = request.form['estante']
            operador_producto = request.form['operador_producto']

            producto_nuevo = [id_producto, referencia_producto, categoria, proveedor, nombre_producto, precio_compra, precio_venta, cantidad_producto, descripcion, stockminimo, estado_producto, ubicacion, estante, operador_producto]

            productos.crearProductos(producto_nuevo)  # Llama a la función para crear el nuevo producto
            flash('Producto creado exitosamente')
            return redirect('/muestra_productos')
        else:
            return render_template('productos/registrar_productos.html')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

if __name__ == '__main__':


    app.run(host='0.0.0.0', debug=True, port="5096")



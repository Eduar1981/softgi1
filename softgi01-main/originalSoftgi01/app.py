from conexion import * #Importo la conexion de la base de datos y las funciones de flask, que en este caso se encuentra en el archivo conexion.py 



@app.route('/') # Inicio la ruta principal del programa en este caso home que me muestra como pagina principal un login
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
    direccion = request.form['direccion']
    contactoEmpleado = request.form['contactoEmpleado']
    ciudad = request.form['ciudad']
    fechaNacimiento = request.form['fechaNacimiento']
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
            tiemporegistro = datetime.datetime.now()
            todoRegistro =[doc_empleado, nom_empleado, ape_empleado, fechaNacimiento, contactoEmpleado, email_empleado, direccion, ciudad, cifrada, rol, tiemporegistro]
            manejoDsuario.registroUsuarios(todoRegistro)
            
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
    if "email_empleado" in session:# verifico que se haya iniciado sesion
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
    cedula = request.form['cedula'] # Utilizo request.form Para trear los datos dijitados en el formulario
    password = request.form['contrasena'] # Utilizo request.form Para trear los datos dijitados en el formulario
    connt = mysql.connect()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cursor = connt.cursor()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cifrado = hashlib.sha512(password.encode('utf-8')).hexdigest()# Cifro la contraseña con el metodo hashlib 

    """ bsql_emp = f"SELECT email_empleado='{email}', contrasena='{cifrado}' FROM empleados WHERE conemail='confirmado'" """

    bsql_emp = f"SELECT empleados.email_empleado, empleados.doc_empleado, empleados.nom_empleado, empleados.ape_empleado, tokens.confir_user FROM empleados INNER JOIN tokens ON empleados.doc_empleado = tokens.doc_empleado WHERE empleados.doc_empleado  = '{cedula}' AND empleados.contrasena='{cifrado}'"
    cursor.execute(bsql_emp)# ejecuto la consulta 
    resultado = cursor.fetchone()# agrego el resultado de la consulta a la variable resultado
    if resultado is not None:# hago una toma de desicion que donde la consulta resultado tenga dato o no esta vacia me haga el siguiente metodo
        if resultado[4] == 'confirmado':# toma de desicion que se aplica en el caso de que el correo este confirmado 
            session["email_empleado"] = resultado[0]# Utilizo session para guardar la informacion de la persona ingresada
            session["doc_empleado"] = resultado[1]
            session["nom_empleado"] = resultado[2]
            session["ape_empleado"] = resultado[3]

            # consulta el rol del empleado
            sql = f"SELECT `rol` FROM `empleados` WHERE doc_empleado = '{resultado[1]}'"
            conn = mysql.connect()
            cursor = conn.cursor() 
            cursor.execute(sql)
            rol = cursor.fetchall()
            conn.commit()

            # se almacena el resultado
            session["rol"] = rol[0][0]


            print(session)
            print(resultado)
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
        usuario_data = cursor.fetchone()

        if usuario_data:
            usuario = User(id=usuario_data[0], email=usuario_data[5], nombre=usuario_data[1])
            

            cursor = mysql.get_db().cursor()

            # Verificar si hay registros en la tabla recuperarcontrasena para ese correo electrónico
            cursor.execute("SELECT * FROM recuperarcontrasena WHERE email_usuario = %s", (usuario.email,))
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
            cursor.execute("INSERT INTO recuperarcontrasena (email_usuario, fechahora_solicitud, fechahora_termina, codigo, usuario,utilizado) VALUES (%s, %s, %s, %s, %s,%s)",
                            (usuario.email, datetime.datetime.now(), expiration_time, token_recuperar, usuario.id,'no')) 
            mysql.get_db().commit()
            
            
            envio_correo(usuario, token_recuperar)
            print(usuario, token_recuperar)
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
        cursor.execute("UPDATE recuperarcontrasena SET utilizado='si' WHERE codigo = %s", (codigo))
        mysql.get_db().commit()

        flash('Tu contraseña ha sido restablecida.', 'success')
        return redirect(url_for('home'))

    return render_template('reset_password.html')

#----------------------------------------conexión de la clase cliente-------------------------------------

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
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        doc_cliente = request.form['doc_cliente']
        nom_cliente = request.form['nom_cliente']
        ape_cliente = request.form['ape_cliente']
        fecha_nacimiento_cliente = request.form['fecha_nacimiento_cliente']
        contacto_cliente = request.form['contacto_cliente']
        email_cliente = request.form['email_cliente']
        direccion_cliente = request.form['direccion_cliente']
        ciudad_cliente = request.form['ciudad_cliente']
        tipo_persona = request.form['tipopersona']                 #crea clientes
        tiempo = datetime.datetime.now()
        

        if not losClientes.buscar_cliente(doc_cliente):
            losClientes.crear_cliente([doc_cliente, nom_cliente, ape_cliente, fecha_nacimiento_cliente, contacto_cliente, email_cliente, direccion_cliente, ciudad_cliente, tipo_persona, tiempo, documento_registro, nombre_operador, apellido_operador])
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
            cursor.execute("SELECT * FROM clientes WHERE estado_cliente='ACTIVO' AND nom_cliente LIKE %s", (f"%{busqueda}%",))
    #buscador de clientes
            resultados = cursor.fetchall()
            conn.close()
            return render_template('clientes/muestraclientes.html', resulta=resultados) # Envía los resultados al mismo formulario de registroclientes.html
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
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        print(bsq)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        print(resultado)
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        documento = request.form['documentoProveedor']
        nombre = request.form['nombreProveedor']
        numero = request.form['numeroProveedores']
        correo = request.form['correoProveedores']
        direcion = request.form['direccionProveedores']
        ciudad = request.form['ciudadProveedor']
        tiempo = datetime.datetime.now()

        proveedores.crear([documento,nombre,numero,correo,direcion,ciudad, tiempo, documento_registro, nombre_operador, apellido_operador])
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

# muestra las categorias-------------------------------------------

@app.route("/categorias")
def categorias():
    sql = "SELECT * FROM categorias WHERE estado_categorias ='ACTIVO'"
    conn = mysql.connect()                    
    cursor = conn.cursor()
    cursor.execute(sql)                                          
    resultado = cursor.fetchall()
    return render_template('/categorias/muestracategorias.html', resulta=resultado)


 #crea categorias--------------------------------------------------

@app.route("/crearCategoria")
def crearCategoria(): 
    if "email_empleado" in session:                                   
        return render_template('categorias/registrar_categorias.html')       
    else:
            flash('Algo esta mal en sus datos digitados')
            return redirect(url_for('home'))
    
   

@app.route("/registrar_categorias", methods=['POST'])
def registrar_categorias():
    if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        print(bsq)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        print(resultado)
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        nombre_categoria = request.form['nom_categoria']
        tiempo = datetime.datetime.now()

        lascategorias.crear_categoria([nombre_categoria, tiempo, documento_registro, nombre_operador, apellido_operador])
        return redirect('categorias')
    

    else:
        flash('Algo esta mal en sus datos digitados')
        return redirect(url_for('home'))
    
        
#editar categorias---------------------------------------------

#muestra los datos para editar---------------------------

@app.route("/editarCategorias/<id_categoria>")  
def editarctegorias(id_categoria):
    if "email_empleado" in session:
        idcategoria = id_categoria
        sql = f"SELECT * FROM categorias WHERE id_categoria = '{idcategoria}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()          
        return render_template("/categorias/editar_categorias.html", resul = resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    
#edita-----------------------------------------------

@app.route("/editar_categoria", methods=['POST', 'GET'])
def editacategoria():
    if "email_empleado" in session:
        idcategoria = request.form['id_categoria']
        nombre_categoria = request.form['nom_categoria']
        lascategorias.modificar_categoria([idcategoria, nombre_categoria])
        return redirect('/categorias')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    
 #elimina------------------------------------------

@app.route('/borracategoria/<id_categoria>')
def borracategoria(id_categoria):
    if "email_empleado" in session:
        lascategorias.borrar_categoria (id_categoria)                      
        return redirect('/categorias')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

                                        
#----------------------------------------------Crud de productos------------------------------------------------ 

@app.route('/productos')
def productos():
        return render_template('/productos/muestra_productos.html')
    
@app.route('/registrar_productos')
def registrar_productos():
    return render_template('/productos/registrar_productos.html')
        
@app.route('/crear_producto', methods=['POST'])
def crearProducto():
    if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        print(bsq)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        nombreProveedor = request.form['nombreProveedor']
        sql = f"SELECT doc_proveedor FROM proveedores WHERE nom_proveedor= '{nombreProveedor}'"
        cursor.execute(sql)
        resultado2 = cursor.fetchone()
        print(resultado2)
        id_producto = request.form['id_producto']
        referencia_producto = request.form['referencia_producto']
        categoria = request.form['categoria']
        proveedor = resultado2[0]
        print(proveedor)
        nombre_producto = request.form['nombre_producto']
        precio_compra = request.form['precio_compra']
        precio_venta = request.form['precio_venta']
        cantidad_producto = request.form['cantidad_producto']
        descripcion = request.form['descripcion']
        stockminimo = request.form['stockminimo']
        ubicacion = request.form['ubicacion']
        estante = request.form['estante']
        tiempoRegistro = datetime.datetime.now()

        Crudproductos.crearProductos([id_producto, referencia_producto, categoria, proveedor, nombre_producto, precio_compra, precio_venta, cantidad_producto, descripcion, stockminimo, ubicacion, estante, tiempoRegistro, documento_registro, nombre_operador, apellido_operador, nombreProveedor])
        return redirect('/muestra_productos') 
    else:
        flash('Algo esta mal en los datos digitados')
        return redirect(url_for('home'))




@app.route('/muestra_productos')
def muestra_Productos():
    if "email_empleado" in session:
        sql = "SELECT  p.referencia_producto, c.nom_categoria, p.proveedor, p.nombre_proveedor, p.nombre_producto, p.precio_compra, p.precio_venta, p.cantidad_producto, p.descripcion, p.stockminimo, p.ubicacion, p.estante FROM productos p JOIN categorias c ON p.categoria = c.id_categoria WHERE p.estado_producto ='ACTIVO';" # se realiza un join para la consulta, con la unión de la tabla categoría para obtener el nombre de la categoría en lugar de su ID.
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        if (len(resultado) >= 1):
            return render_template("/productos/muestra_productos.html", resul=resultado)   # si hay resultados se muestran.
        else:
            resultado2 = "No hay productos registrados"
            return render_template("/productos/muestra_productos.html", resul2=resultado2)  # sino se muestra el mensaje de resultado2.
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

@app.route('/Busca_productos', methods=['POST'])
def Busca_productos():
    dato_busqueda = request.form['dato_busqueda']
    sql = f"SELECT `id_producto`, `referencia_producto`, `categoria`, `proveedor`, `nombre_producto`, `precio_compra`, `precio_venta`, `cantidad_producto`, `descripcion`, `stockminimo`, `ubicacion`, `estante`, `estado_producto`, `nombre_proveedor` FROM `productos` WHERE estado_producto='activo' AND id_producto LIKE '%{dato_busqueda}%' OR estado_producto='activo' AND nombre_producto LIKE '%{dato_busqueda}%' OR estado_producto='activo' AND categoria LIKE '%{dato_busqueda}%' OR estado_producto='activo' AND 'descripcion' LIKE '%{dato_busqueda}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)             # puede buscar por doc_empleado,nom_empleado y ape_empleado
    resultado = cursor.fetchall()  
    conn.commit()
    return render_template("/productos/muestra_productos.html", resul=resultado)



@app.route("/modificar_producto/<id_producto>")
def editar_producto(id_producto):
    if "email_empleado" in session:
        
        sql = f"SELECT * FROM productos WHERE id_producto='{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()  
        conn.commit()
        return render_template("/productos/edita_productos.html", resul= resultado)
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))      


@app.route('/modificar_producto', methods=['POST', 'GET'])
def modificarProducto():
     if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        print(bsq)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        nombreProveedor = request.form['nombreProveedor']
        sql = f"SELECT doc_proveedor FROM proveedores WHERE nom_proveedor= '{nombreProveedor}'"
        cursor.execute(sql)
        resultado2 = cursor.fetchone()
        print(resultado2)
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
        ubicacion = request.form['ubicacion']
        estante = request.form['estante']
        Crudproductos.modificar([id_producto, referencia_producto, categoria, proveedor, nombre_producto, precio_compra, precio_venta, cantidad_producto, descripcion, stockminimo, ubicacion, estante, documento_registro, nombre_operador, apellido_operador, nombreProveedor])
        return redirect('/muestra_productos')
     else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
 

@app.route('/borra_produc/<idprod>')
def borra_produc(idprod):
    if "email_empleado" in session:
        Crudproductos.borrar_producto(idprod)        # Eliminar productos
        return redirect("/muestra_productos")   
    else:
        flash('Algo esta mal en los datos digitados')
        return redirect(url_for('home'))
    

#----------------------------------------------Crud de empleados------------------------------------------------ 

@app.route('/muestra_empleados')         # muestra datos de los empleados
def muestra_empleados():
    sql = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado`, `fecha_nacimiento_empleado`, `contacto_empleado`, `email_empleado`, `direccion_empleado`, `ciudad_empleado`, `rol`, `fechahora_registroempleado` FROM `empleados`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()  
    conn.commit()
    return render_template("/empleados/muestra_empleados.html", resul=resultado) 


@app.route('/edita_empleados/<doc_empleado>')      # muestra los datos del empleado en los inputs de editar
def edita_empleados(doc_empleado):
    sql = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado`, `fecha_nacimiento_empleado`, `contacto_empleado`, `email_empleado`, `direccion_empleado`, `ciudad_empleado`, `rol` FROM `empleados` WHERE doc_empleado='{doc_empleado}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()  
    conn.commit()
    return render_template("/empleados/edita_empleados.html", resul=resultado[0])

@app.route('/Actualiza_empleados', methods=['POST'])
def Actualiza_empleados():
    doc_empleado = request.form['doc_empleado']
    nom_empleado = request.form['nom_empleado']             # actualiza la info del empleado
    ape_empleado = request.form['ape_empleado']
    fecha_nacimiento = request.form['fecha_nacimiento']
    contacto_empleado = request.form['contacto_empleado']
    email_empleado = request.form['email_empleado']
    direccion_empleado = request.form['direccion_empleado']
    ciudad_empleado = request.form['ciudad_empleado']
    rol = request.form['rol']
    empleados.modificar([doc_empleado, nom_empleado, ape_empleado, fecha_nacimiento, contacto_empleado, email_empleado, direccion_empleado, ciudad_empleado, rol])
    return redirect('/muestra_empleados')

#                        -------------------- busca empleados --------------------------
@app.route('/Busca_empleados', methods=['POST'])
def Busca_empleados():
    dato_busqueda = request.form['dato_busqueda']
    sql = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado`, `fecha_nacimiento_empleado`, `contacto_empleado`, `email_empleado`, `direccion_empleado`, `ciudad_empleado`, `rol` FROM `empleados` WHERE estado='activo' AND doc_empleado LIKE '%{dato_busqueda}%' OR nom_empleado LIKE '%{dato_busqueda}%' OR ape_empleado LIKE '%{dato_busqueda}%'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)             # puede buscar por doc_empleado,nom_empleado y ape_empleado
    resultado = cursor.fetchall()  
    conn.commit()
    return render_template("/empleados/muestra_empleados.html", resul=resultado)



@app.route('/elimina_empleados/<doc_empleado>')        # Elimina los empleados
def elimina_empleados(doc_empleado):
    empleados.eliminar(doc_empleado)
    return redirect('/muestra_empleados')

#---------------------------------------------------cotizaciones----------------------------------------------------

@app.route("/Cotizacion")
def Cotizacion():
    if "email_empleado" in session:
        msql= f"SELECT `num_cotizacion`,`nombre_cliente_cotizacion`, `nombre_operador`, `fecha_inicio_cotizacion`, `fecha_fin_cotizacion` FROM `cotizaciones`"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(msql)
        datos = cursor.fetchall()
        return render_template("/cotizaciones/mostrar_cotizaciones.html", datos=datos)
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#registro de cotizaciones
@app.route("/verCotizaciones")
def mostraCotizaciones():
    if "email_empleado" in session:
        return render_template('cotizaciones/registrar_cotizaciones.html')

@app.route('/crearCotizacion', methods=['POST'])
def crearCotizacion():
    if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        nombre_cliente_cotizacion = request.form['clienteCotizacion']
        bsqd = f"SELECT `doc_cliente` FROM clientes WHERE `nom_cliente`='{nombre_cliente_cotizacion}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsqd)
        resultado2 = cursor.fetchone()
        print(resultado2)
        clienteCotizacion = resultado2[0]
        fechaInicioCotizacion = request.form['fechaInicioCotizacion']
        fechaFinCotizacion = request.form['fechaFinCotizacion']
        datos_cotizaciones = [nombre_cliente_cotizacion,documento_registro,nombre_operador,apellido_operador,fechaInicioCotizacion,fechaFinCotizacion, nombre_cliente_cotizacion]
        Crudcotizaciones.crearCotizaciones([clienteCotizacion,documento_registro,nombre_operador,apellido_operador,fechaInicioCotizacion,fechaFinCotizacion, nombre_cliente_cotizacion])
        return redirect('detalleCotizacion')
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))
    
#Borrar cotizacion 
@app.route('/borraCotizacion/<id_cotizacion>')
def borraCotizacion(id_cotizacion):
    if "email_empleado" in session:
        Crudcotizaciones.eliminarCotizacion(id_cotizacion)                       
        return redirect("/Cotizacion")
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))


#mostrar detalle de cotizacion
@app.route('/cotizacionesDetalles')
def cotizacionesDetalles():
    bsq = f"SELECT * FROM `detallecotizaciones`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(bsq)
    resultado = cursor.fetchall()
    return render_template('cotizaciones/mostrar_detalleCotizacion.html', datos = resultado)

#editar detalle de cotizacion
@app.route("/editarDetalleCotizacion/<id_DetalleCotizacion>")
def editarDetalleCotizacion(id_DetalleCotizacion):
    if "email_empleado" in session:
        sql = f"SELECT * FROM `detallecotizaciones` WHERE `id_detalle_cotizacion` = '{id_DetalleCotizacion}'"
        conn = mysql.connect()
        cursor = conn.cursor()                                   
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        return render_template("cotizaciones/editar_detalleCotizacion.html", resul=resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
#Actualizar detalle de cotizacion
@app.route('/editarDetalleCotizacions', methods=['POST', 'GET'])
def editarDetalleCotizacions():
    if "email_empleado" in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        id_detalle = request.form['id']
        cantidadProductosCotizacion = request.form['cantidadProductosCotizacion']
        valorunidadProdcotizacion = request.form['valorunidadProdcotizacion']
        valortotalCantidaproductosCotizacion = request.form['valortotalCantidaproductosCotizacion']
        servicioCotizacion = request.form['servicioCotizacion']
        cantidadServiciosCotizacion = request.form['cantidadServiciosCotizacion']
        valorunidadServicioscotizacion = request.form['valorunidadServicioscotizacion']
        valortotalCantidadserviciosCotizacion = request.form['valortotalCantidadserviciosCotizacion']
        totalpagarCotizacion = request.form['totalpagarCotizacion']
        sql = f"SELECT `num_cotizacion` FROM `cotizaciones` WHERE `num_cotizacion`='1'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        num_cotizacion  = resultado[0]
        referenciaProducto = request.form['referenciaProducto']
        bsql = f"SELECT `id_producto` FROM `productos` WHERE referencia_producto='{referenciaProducto}'"
        cursor.execute(bsql)
        resultado2 = cursor.fetchone() 
        producto_cotizacion = resultado2[0]
        datos = [id_detalle, num_cotizacion, producto_cotizacion, cantidadProductosCotizacion, valorunidadProdcotizacion, valortotalCantidaproductosCotizacion, servicioCotizacion, cantidadServiciosCotizacion, valorunidadServicioscotizacion, valortotalCantidadserviciosCotizacion, totalpagarCotizacion ]
        Crudcotizaciones.editarDetalleCotizaciones(datos)
        return redirect('cotizacionesDetalles')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

#Borrar cotizacion 
@app.route('/borraDetalleCotizacion/<id_detalleCotizacion>')
def borraDetalleCotizacion(id_detalleCotizacion):
    if "email_empleado" in session:
        Crudcotizaciones.eliminarDetalleCotizacion(id_detalleCotizacion)                       
        return redirect("/cotizacionesDetalles")
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

#crear detalle de cotizacion
@app.route('/detalleCotizacion')
def detalleCotizacion():
    return render_template('cotizaciones/detalle_cotizacion.html')

@app.route('/registroDetalleCotizacion', methods=['POST'])
def registroDetalleCotizacion():
     if "email_empleado" in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        cantidadProductosCotizacion = request.form['cantidadProductosCotizacion']
        valorunidadProdcotizacion = request.form['valorunidadProdcotizacion']
        valortotalCantidaproductosCotizacion = request.form['valortotalCantidaproductosCotizacion']
        servicioCotizacion = request.form['servicioCotizacion']
        cantidadServiciosCotizacion = request.form['cantidadServiciosCotizacion']
        valorunidadServicioscotizacion = request.form['valorunidadServicioscotizacion']
        valortotalCantidadserviciosCotizacion = request.form['valortotalCantidadserviciosCotizacion']
        totalpagarCotizacion = request.form['totalpagarCotizacion']
        sql = f"SELECT `num_cotizacion` FROM `cotizaciones` WHERE `num_cotizacion`='1'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        num_cotizacion  = resultado[0]
        referenciaProducto = request.form['referenciaProducto']
        bsql = f"SELECT `id_producto` FROM `productos` WHERE referencia_producto='{referenciaProducto}'"
        cursor.execute(bsql)
        resultado2 = cursor.fetchone() 
        producto_cotizacion = resultado2[0]
        datos = [num_cotizacion, producto_cotizacion, cantidadProductosCotizacion, valorunidadProdcotizacion, valortotalCantidaproductosCotizacion, servicioCotizacion, cantidadServiciosCotizacion, valorunidadServicioscotizacion, valortotalCantidadserviciosCotizacion, totalpagarCotizacion ]
        Crudcotizaciones.crearDetalleCotizacion(datos)
        return redirect('Cotizacion')
     else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    

#editar cotizacion
@app.route("/editarCotizacion/<id_cotizacion>")
def editarCotizacion(id_cotizacion):
    if "email_empleado" in session:
        sql = f"SELECT * FROM cotizaciones WHERE num_cotizacion = '{id_cotizacion}'"
        print(id_cotizacion)
        conn = mysql.connect()
        cursor = conn.cursor()                                    #muestra toda la informacion y pone en los imputs
        cursor.execute(sql)
        resultado = cursor.fetchall()
        print(resultado)
        conn.commit()
        return render_template("cotizaciones/editar_cotizaciones.html", resul=resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

@app.route('/atualizarCotizacion', methods=['POST'])
def atualizarCotizacion():
    if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        nombre_cliente_cotizacion = request.form['clienteCotizacion']
        bsqd = f"SELECT doc_cliente FROM clientes WHERE nom_cliente='{nombre_cliente_cotizacion}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsqd)
        resultado2 = cursor.fetchone()
        clienteCotizacion = resultado2[0]
        id_c = request.form['id']
        fechaInicioCotizacion = request.form['fechaInicioCotizacion']
        fechaFinCotizacion = request.form['fechaFinCotizacion']
        datos_cotizaciones = [id_c, clienteCotizacion,documento_registro,nombre_operador,apellido_operador,fechaInicioCotizacion,fechaFinCotizacion, nombre_cliente_cotizacion ]
        Crudcotizaciones.editarCotizacion(datos_cotizaciones)
        return redirect('Cotizacion')
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#---------------------------------------------------compras PROVEEDORES----------------------------------------------------


# ------------- registra compras  --------------

@app.route("/Regitra_compra_prov")
def Regitra_compra_prov():
    if "email_empleado" in session:

        sql = "SELECT doc_proveedor FROM proveedores WHERE estado_proveedor = 'ACTIVO'"
        conn = mysql.connect()
        cursor = conn.cursor()                  # consulta todos los documentos de los proveedores y los envia al select
        cursor.execute(sql)
        resultado = cursor.fetchall()         # y muestra el html registra_compras_prove
        conn.commit()
        return render_template("/compra_proveedores/registra_compras_prove.html",resul = resultado)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


@app.route("/Registrar_compra_p", methods=['POST'])
def Registrar_compra_p():
    if "email_empleado" in session:


        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)                         # recibe la info y consulta los datos del operador
        resultado = cursor.fetchone()

        documento_operador = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]

        proveedor_compra = request.form['proveedor_compra']
        producto_compra = request.form['producto_compra']
        Cantidad_compra = request.form['cantidad_compra']
        cantidad_compra = int(Cantidad_compra)
        valor_unidad = request.form['valor_unidad']
        valor_total_unidad = (valor_unidad*cantidad_compra)
        estado = "ACTIVO"
        tiempo_compra = datetime.datetime.now()

        lower = string.ascii_lowercase       
        upper = string.ascii_uppercase # generador de codigo 
        num = string.digits 
        chars = lower + upper + num
        codigo = random.sample(chars, 10)
        codigo_2 = ""  # variable que guarda el codigo
        for c in codigo:
            codigo_2+=c
        print(f"\n {codigo_2} \n")

        compras_prove.registrar_compra([proveedor_compra, documento_operador, nombre_operador, apellido_operador, tiempo_compra, estado, codigo_2])   # se incerta los datos en la primera tabla
        
        
        
        sql = f"SELECT num_compra FROM comprasproveedores WHERE codigo_tabla = '{codigo_2}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        num_compra = cursor.fetchall()   # consulta el numero de compra de acuerdo al  codigo de esa tabla
        conn.commit()
        num = num_compra[0][0] # [[N]] ----> N 
        
        compras_prove.registrar_detalles_compra([num, producto_compra, cantidad_compra, valor_unidad, valor_total_unidad])   # se incerta los datos en la segunda tabla
        flash('¡Compra registrada con exito!')
        return redirect("/Regitra_compra_prov")



    else:
        flash('Por favor inicia sesion para poder acceder')
        return redirect(url_for('home'))
    


# ------------- cancela compras -------

@app.route("/cancelar_compra_proveed/<num_compra>")
def cancelar_compra_proveed(num_compra):
    if "email_empleado" in session:

        compras_prove.cacela_compra(num_compra)
        return redirect("/muestra_compra_proved")

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))



# ------- editar detalles de compras a proveedores -----

@app.route("/edita_compras_provee/<num_compra>") 
def edita_compras_provee(num_compra):
    if "email_empleado" in session:

        sql = f"SELECT num_compra, producto_compra, cantidad_producto_compra, valorunidad_prodcompra FROM detallecomprasproveedores WHERE num_compra = '{num_compra}' "
        conn = mysql.connect()
        cursor = conn.cursor()                  
        cursor.execute(sql)
        resultado = cursor.fetchall()  
        conn.commit()
        return render_template("/compra_proveedores/edita_compras_prove.html", resul=resultado[0])
    
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


@app.route("/actualiza_compra_provee", methods=['POST'])
def actualiza_compra_provee():
    if "email_empleado" in session:

        num_compra = request.form['num_compra']
        producto_compra = request.form['producto_compra']
        cantidad_compra = request.form['cantidad_compra']
        valor_unidad = request.form['valor_unidad']
        valor_total_unidad = (cantidad_compra*valor_unidad)
        
        compras_prove.edita_detalles_compra([num_compra, producto_compra, cantidad_compra, valor_unidad, valor_total_unidad])

        return redirect("/muestra_compra_proved")
    
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))



# ------------- buscador --------------

@app.route("/busca_compras_prov", methods=['POST', 'GET'])
def busca_compras_prov():
    if "email_empleado" in session:
        if request.method == 'POST':
            dato_busqueda = request.form['dato_busqueda']
            sql = f"SELECT `num_compra`, `proveedor_compra`, `documento_operador`, `nombre_operador`, `apellido_operador`, `date_compra`, `num_factura_proveedor` FROM `comprasproveedores` WHERE estado='activo' AND (num_compra LIKE '%{dato_busqueda}%' OR proveedor_compra LIKE '%{dato_busqueda}%')"
            conn = mysql.connect()
            cursor = conn.cursor()                  # muestra las compras a proveedores dependiendo de la busqueda
            cursor.execute(sql)
            resultado = cursor.fetchall()  
            conn.commit()
            return render_template("/compra_proveedores/muestra_compras_prove.html", resul=resultado)
        return redirect('muestra_compra_proved')

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


# --------- muestra compras a proveedores -------

@app.route("/muestra_compra_proved")
def muestra_compra_proved():
    if "email_empleado" in session:

        sql ="SELECT `num_compra`, `proveedor_compra`, `documento_operador`, `nombre_operador`, `apellido_operador`, `date_compra`, `num_factura_proveedor` FROM `comprasproveedores` WHERE estado = 'ACTIVO'"
        conn = mysql.connect()
        cursor = conn.cursor()                  # muestra las compras a proveedores
        cursor.execute(sql)
        resultado = cursor.fetchall()  
        conn.commit()
        return render_template("/compra_proveedores/muestra_compras_prove.html", resul=resultado) 
    
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))
    

# ------------- muestra detalles de compras a proveedores ----------

@app.route("/muestra_detalles_com/<num_compra>")
def muestra_detalles_com(num_compra):
    if "email_empleado" in session:
        
        sql = f"SELECT `detallenum_compra`,`detallenum_compra`, `producto_compra`, `cantidad_producto_compra`, `valorunidad_prodcompra`, `valortotal_cantidadcomp`, `totalpagar_compra` FROM `detallecomprasproveedores` WHERE detallenum_compra = '{num_compra}'"
        conn = mysql.connect()
        cursor = conn.cursor()                  # muestra los detalles de compras a proveedores
        cursor.execute(sql)
        resultado = cursor.fetchall()  
        conn.commit()
        return render_template("/compra_proveedores/detalles_compras/muestra_detalles.html", resul=resultado)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#--------------------------------------devoluciones----------------------------------------------------------------

@app.route("/muestraDevoluciones")
def muestraDevoluciones():
    if "email_empleado" in session:
        msql= f"SELECT `id_devolucion`, `num_factura`, `documento_operador`, `nombre_operador`, `apellido_operador`, `cliente_devolucion`, `fecha_devolucion` FROM `devoluciones`"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(msql)
        datos = cursor.fetchall()
        return render_template("/devoluciones/muestra_devoluciones.html", datos=datos)
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#registro de devoluciones
@app.route("/crear_devolucion")
def crear_devolucion():
    if "email_empleado" in session:
        return render_template('devoluciones/registrar_devolucion.html')

@app.route('/crear_devolucion', methods=['POST'])
def crearDevoluciones():
    if "email_empleado" in session:
        email = session["email_empleado"]
        conn = mysql.connect()
        cursor = conn.cursor()

        # Obtener los detalles del empleado
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        cursor.execute(bsq)
        resultado = cursor.fetchone()

        if resultado:
            documento_registro = resultado[0]
            nombre_operador = resultado[1]
            apellido_operador = resultado[2]

            # Obtener detalles del formulario
            num_factura = request.form['num_factura']
            cliente_devolucion = request.form['cliente_devolucion']
            fecha_devolucion = request.form['fecha_devolucion']

            # Verificar existencia de datos
            bsqd_venta = f"SELECT num_factura FROM ventas WHERE num_factura='{num_factura}'"
            cursor.execute(bsqd_venta)
            resultado_venta = cursor.fetchone()

            bsqd_cliente = f"SELECT doc_cliente FROM clientes WHERE doc_cliente='{cliente_devolucion}'"
            cursor.execute(bsqd_cliente)
            resultado_cliente = cursor.fetchone()

            bsqd_empleado = f"SELECT doc_empleado FROM empleados WHERE doc_empleado='{documento_registro}'"
            cursor.execute(bsqd_empleado)
            resultado_empleado = cursor.fetchone()

            if resultado_venta and resultado_cliente and resultado_empleado:
                # Llamar a la función para crear la devolución
                Cruddevoluciones.crear_devolucion([num_factura, cliente_devolucion, documento_registro, nombre_operador, apellido_operador, fecha_devolucion])
                return redirect('muestraDevoluciones')
            else:
                flash('Algunos datos no existen en la base de datos')
                return redirect(url_for('home'))
        else:
            flash('No se encontró el empleado en la base de datos')
            return redirect(url_for('home'))
    else:
        flash('Por favor inicia sesión para poder acceder')
        return redirect(url_for('home'))


#mostrar detalle de devolucion
@app.route('/detalledevoluciones')
def detallesDevoluciones():
    bsq = f"SELECT * FROM `detallesdevoluciones`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(bsq)
    resultado = cursor.fetchall()
    return render_template('devoluciones/muestra_detalle_devoluciones.html', datos = resultado)

#editar detalle de devolucion
@app.route("/editarDetalleDevolucioncion/<id_DetalleDevolucion>")
def editarDetalleDevolucion(id_DetalleDevolucion):
    if "email_empleado" in session:
        sql = f"SELECT * FROM `detalledevoluciones` WHERE `id_detalle_devolucion` = '{id_DetalleDevolucion}'"
        conn = mysql.connect()
        cursor = conn.cursor()                                   
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        return render_template("devoluciones/editar_detalle_devolucion.html", resul=resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
#Actualizar detalle de cotizacion
@app.route('/editarDetalleDevoluciones', methods=['POST', 'GET'])
def editarDetalleDevoluciones():
    if "email_empleado" in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        num_devolucion = request.form['num_devolucion']
        producto_devolucion = request.form['producto_devolucion']
        cantidad_proddevolucion = request.form['cantidad_proddevolucion']
        precio_proddevolucion = request.form['precio_proddevolucion']
        motivo_devolucion = request.form['motivo_devolucion']
        monto_total_devolucion = request.form['monto_total_devolucion']
        sql = f"SELECT `num_devolucion` FROM `devoluciones` WHERE `num_devolucion`='1'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        num_devolucion  = resultado[1]
        bsql = f"SELECT `num_devolucion` FROM `devoluciones` WHERE id_devolucion='{num_devolucion}'"
        cursor.execute(bsql)
        resultado2 = cursor.fetchone() 
        producto_cotizacion = resultado2[0]
        datos = [num_devolucion, producto_cotizacion, producto_devolucion, cantidad_proddevolucion, precio_proddevolucion, motivo_devolucion, monto_total_devolucion   ]
        Crudcotizaciones.editarDetalleCotizaciones(datos)
        return redirect('detallesDevoluciones')
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

#Borrar detalle de devolucion 
@app.route('/borraDetalleCotizacion/<id_detalleDevolucion>')
def borraDetalleDevolucion(id_detalleDevolucion):
    if "email_empleado" in session:
        Cruddevoluciones.eliminarDetalleDevolucion(id_detalleDevolucion)                       
        return redirect("/detallesDevoluciones")
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

#crear detalle de cotizacion
@app.route('/detalleDevoluciones')
def detalleDevolucion():
    return render_template('devoluciones/detalle_devoluciones.html')

@app.route('/registroDetalleDevolucion', methods=['POST'])
def registroDetalleDevolucion():
     if "email_empleado" in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        producto_devolucion = request.form['producto_devolucion']
        cantidad_proddevolucion = request.form['cantidad_proddevolucion']
        precio_proddevolucion = request.form['precio_proddevolucion']
        motivo_devolucion = request.form['motivo_devolucion']
        monto_total_devolucion = request.form['monto_total_devolucion']
        sql = f"SELECT `id_devolucion` FROM `devoluciones` WHERE `id_devolucion`='0'"
        cursor.execute(sql)
        resultado = cursor.fetchone()
        id_detalle_devolucion  = resultado[0]
        num_factura = request.form['num_factura']
        bsql = f"SELECT `num_factura` FROM `ventas` WHERE num_factura='{num_factura}'"
        cursor.execute(bsql)
        resultado2 = cursor.fetchone() 
        producto_devolucion = resultado2[0]
        datos = [id_detalle_devolucion, producto_devolucion, cantidad_proddevolucion, precio_proddevolucion, motivo_devolucion, monto_total_devolucion ]
        Crudcotizaciones.crearDetalleCotizacion(datos)
        return redirect('Devolucion')
     else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))
    

#editar cotizacion
@app.route("/modificar_devolucion/<id_devolucion>")
def editarDevolucion(id_devolucion):
    if "email_empleado" in session:
        sql = f"SELECT * FROM devoluciones WHERE id_devolucion = '{id_devolucion}'"
        print(id_devolucion)
        conn = mysql.connect()
        cursor = conn.cursor()     #muestra toda la informacion y pone en los imputs
        cursor.execute(sql)
        resultado = cursor.fetchall()
        print(resultado)
        conn.commit()
        return render_template("devoluciones/editar_devolucion.html", resul=resultado[0])
    else:
        flash('Algo está mal en los datos digitados')
        return redirect(url_for('home'))

@app.route('/actualizarDevolucion', methods=['POST'])
def atualizarDevolucion():
    if "email_empleado" in session:
        email = session["email_empleado"]
        bsq = f"SELECT `doc_empleado`, `nom_empleado`, `ape_empleado` FROM empleados WHERE email_empleado='{email}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsq)
        resultado = cursor.fetchone()
        documento_registro = resultado[0]
        nombre_operador = resultado[1]
        apellido_operador = resultado[2]
        cliente_devolucion = request.form['clienteDevolucion']
        bsqd = f"SELECT doc_cliente FROM clientes WHERE nom_cliente='{cliente_devolucion}'"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(bsqd)
        resultado2 = cursor.fetchone()
        cliente_devolucion = resultado2[0]
        id_c = request.form['id']
        fecha_devolucion = request.form['fecha_devolucion']
        datos_cotizaciones = [id_c, cliente_devolucion, documento_registro, nombre_operador, apellido_operador,fecha_devolucion, cliente_devolucion ]
        Crudcotizaciones.editarCotizacion(datos_cotizaciones)
        return redirect('Devolucion')
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


#-------------------------------------------------------- Historial de ventas ----------------------------------------------------------------

@app.route("/muestra_ventas")
def muestra_ventas():
    if "email_empleado" in session:
        
        sql = "SELECT  `num_factura`, `cliente_factura`, `documento_operador`, `nombre_operador`, `apellido_operador`, `fechahora_venta`, `forma_pago` FROM `ventas` ORDER BY num_factura DESC"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("/ventas/muestra_ventas.html",resul = resultado)
    
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))
    
    
@app.route("/muestra_detalles_ventas/<num_factura>")
def muestra_detalles_ventas(num_factura):
    if "email_empleado" in session:
        
        sql = f"SELECT `num_factura_venta`, `producto_factura`, `cantidad_productos_factura`, `total_pagar_factura` FROM `detalleventas` WHERE num_factura_venta = '{num_factura}'"
        conn = mysql.connect()
        cursor = conn.cursor()     #muestra toda la informacion de detalles
        cursor.execute(sql)
        resultado = cursor.fetchall()

        return render_template("/ventas/detalle_ventas.html", resul = resultado)
        
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))








#-------------------------------------------------------- Muestra Historial de abonos ----------------------------------------------------------------

@app.route("/historial_abonos/<contador>")
def historial_abonos(contador):
    if "email_empleado" in session:
        
        sql = f"SELECT `abono`, `operador`, `fecha_abono` FROM `historial_credito` WHERE contador_ventacredito = '{contador}' ORDER BY contador DESC"
        conn = mysql.connect()
        cursor = conn.cursor()     #muestra toda la informacion
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conn.commit()
        return render_template("/ventas_credito/historial_abonos.html",resul = resultado)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


#-------------------------------------------------------- abonos ventas a credito ----------------------------------------------------------------

@app.route("/abono_credito/<contador>")
def abono_credito(contador):
    if "email_empleado" in session:

        # muestra el html
        return render_template("/ventas_credito/abono_venta.html",cont = contador)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))



# ------- recibe la info del FRONT-END -----

@app.route("/confirma_abono", methods = ['POST'])
def confirma_abono():
    if "email_empleado" in session:

        contador = request.form['contador']
        abono = request.form['abono']
        documento_operador = session["doc_empleado"]    

        # combierto el texto a numero
        abono = int(abono)
        
        # conuslto el credito restante
        sql = f"SELECT `credito_restante` FROM `ventas_credito` WHERE contador = '{contador}'"
        conn = mysql.connect()
        cursor = conn.cursor()    
        cursor.execute(sql)
        credito_restante = cursor.fetchall()
        conn.commit()

        # 1 - valido si la cantidad digitada es menor a la debida
        if (credito_restante[0][0] >= abono):

            credito_actual = (credito_restante[0][0] - abono)
            tiempo_venta = datetime.datetime.now()

            # 2 - valido si la resta = 0
            if (credito_actual == 0):

                # se cambia el estado de ACTIVO a CANCELADO
                ventas.abono_completo(contador)
                return redirect("/muestra_ventas_credito")
            
            
            # 2 
            else:
                # se actualiza el credito restante
                ventas.actualiza_credito_rest([credito_actual, contador])

                # se incerta en el historial el abono realizado
                ventas.insert_historial_abn([contador, abono, documento_operador, tiempo_venta])
                return redirect("/muestra_ventas_credito")

        # 1
        else:
            mensaj = "¡Cantidd digitada mayor a la debida!"
            return render_template("/ventas_credito/abono_venta.html",cont = contador, mensaje = mensaj)
            
    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


#-------------------------------------------------------- Cancelador ventas a credito ----------------------------------------------------------------

@app.route("/cancela_venta_c/<contador>")
def cancela_venta_c(contador):
    if "email_empleado" in session:

        # funciona al validar q se pago completo el credito 
        ventas.venta_cancelada_cred(contador)
        return redirect("/muestra_ventas_credito")

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


# -------------------------------- Buscador ventas a credito ---------------------

@app.route("/buscador_venta_c", methods = ['POST'])
def buscador_venta_c():
    if "email_empleado" in session:

        # recibe la info
        busqueda = request.form['dato_busqueda']

        sql = f"SELECT `contador`, `cliente`, `productos`, `credito_total`, `credito_restante`, `operador`, `fecha_venta` FROM `ventas_credito`  WHERE estado ='ACTIVO' AND cliente LIKE '%{busqueda}%' OR estado='ACTIVO' AND operador LIKE '%{busqueda}%'"
        conn = mysql.connect()
        cursor = conn.cursor()     #muestra toda la informacion de la busqueda
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("/ventas_credito/muestra_ventas.html",resul = resultado)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#-------------------------------------------------------- muestra Historial de ventas a credito ----------------------------------------------------------------

@app.route("/muestra_ventas_credito")
def muestra_ventas_credito():
    if "email_empleado" in session:
        
        sql = "SELECT `contador`, `cliente`, `productos`, `credito_total`, `credito_restante`, `operador`, `fecha_venta` FROM `ventas_credito` WHERE estado = 'ACTIVO'"
        conn = mysql.connect()
        cursor = conn.cursor()     #muestra toda la informacion
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("/ventas_credito/muestra_ventas.html",resul = resultado)

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))









#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- <<<< REALIZA LA VENTA >>> --------------------------------------------------

@app.route("/confirma_venta", methods = ['POST'])
def confirma_venta():
    if "email_empleado" in session:

#-------------------------------------------- informacion por si hay un error -----------

        # Muestra el documento del operador
        documento_operador = session["doc_empleado"]

        # consulta los productos del inventario
        sql = "SELECT `id_producto`, `referencia_producto`, `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE `estado_producto`= 'ACTIVO'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        productos_inven = cursor.fetchall()
        conn.commit()

        # consulta los productos seleccionados para venta
        sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        productos_carr = cursor.fetchall()
        conn.commit()

        # Realiza la suma de el total de todos los productos seleccionados
        sql = "SELECT SUM(total) FROM carritoventas"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql) 
        Suma_total = cursor.fetchall()
        conn.commit()

#--------------------------------------------------------------------

        # valido si hay productos o no
        sql = f"SELECT `id_producto` FROM carritoventas"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        busqueda = cursor.fetchall()
        conn.commit()

        # 1 - valido que la venta no este vacia - 
        if ((len(busqueda)) > 0):

            # recibo la info del FRONT-END
            doc_operador = request.form['doc_operador']
            doc_cliente = request.form['doc_cliente']
            forma_de_pago = request.form['forma_de_pago']
            tipo_de_venta = request.form['tipo_de_venta']

            # consulto info del operador
            sql = f"SELECT * FROM `empleados` WHERE doc_empleado = '{doc_operador}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            info_operador = cursor.fetchall()
            conn.commit()

            # 2 - valido que el operador exista
            if ((len(info_operador)) > 0):

                # consulto info cliente
                sql = f"SELECT * FROM `clientes` WHERE estado_cliente = 'ACTIVO' AND doc_cliente = '{doc_cliente}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                info_cliente = cursor.fetchall()
                conn.commit()

                # 3 - valido que el cliente exista
                if ((len(info_cliente)) > 0):

                    # captura el timpo
                    tiempo_venta = datetime.datetime.now()

                    # Agrupo el nombre de todos los productos
                    sql = "SELECT GROUP_CONCAT(nombre_producto SEPARATOR ', ') FROM carritoventas"
                    conn = mysql.connect()
                    cursor = conn.cursor()     
                    cursor.execute(sql)
                    productos_fac = cursor.fetchall()
                    conn.commit()

                    # 4 ----------- Validacion tipo de venta --------------
                    if (tipo_de_venta == "venta_normal"):

                        # consulto el nombre y apellido del operador
                        sql = f"SELECT `nom_empleado`, `ape_empleado` FROM `empleados` WHERE doc_empleado = '{doc_operador}'"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        nombre_apell_operador = cursor.fetchall()
                        conn.commit()

                        # paso de [[]] a []
                        nom_ape_operador = nombre_apell_operador[0]

                        # generador de codigo 
                        lower = string.ascii_lowercase       
                        upper = string.ascii_uppercase 
                        num = string.digits 
                        chars = lower + upper + num
                        codigo = random.sample(chars, 20)
                        codigo_2 = ""  # variable que guarda el codigo
                        for c in codigo:
                            codigo_2+=c
                        
                        # Insertacion de datos en tabla ventas
                        ventas.crear_venta([doc_cliente, doc_operador, tiempo_venta, forma_de_pago, codigo_2, nom_ape_operador[0], nom_ape_operador[1]])

                        # consulto el num_factura en tabla ventas
                        sql = f"SELECT `num_factura` FROM `ventas` WHERE codigo_tabla = '{codigo_2}'"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        num_factura = cursor.fetchall()
                        conn.commit()

                        #consulto el numero de productos seleccionados
                        sql = "SELECT SUM(cantidad_adquirida) FROM `carritoventas`"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        cantidad_productos = cursor.fetchall()
                        conn.commit()

                        # Insertacion en la tabla detalleventas 
                        ventas.crearDetalleventa([num_factura[0][0], productos_fac[0][0], cantidad_productos[0][0], Suma_total[0][0], Suma_total[0][0]])

                        #  Elimino toda la info del carritoventas
                        sql = "DELETE FROM `carritoventas`"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        conn.commit()

                        # consulta los productos seleccionados para venta
                        sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        productos_carr_actualizado = cursor.fetchall()
                        conn.commit()

                        mensaje_exitoso = "¡Venta realizada!"
                        return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr_actualizado, Total = 0, operador = documento_operador, mensaje_2 = mensaje_exitoso) 



                    # 4
                    else:

                        ventas.crear_venta_credito([doc_cliente, productos_fac[0][0], Suma_total[0][0], Suma_total[0][0], doc_operador, tiempo_venta, ])

                        #  Elimino toda la info del carritoventas
                        sql = "DELETE FROM `carritoventas`"
                        conn = mysql.connect()
                        cursor = conn.cursor()     
                        cursor.execute(sql)
                        conn.commit()

                        # consulta los productos seleccionados actualizados para venta
                        sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
                        conn = mysql.connect()
                        cursor = conn.cursor()  
                        cursor.execute(sql)
                        productos_carr_disponible = cursor.fetchall()
                        conn.commit()

                        mensaje_exitoso = "¡Venta a credito realizada!"
                        return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr_disponible, Total = 0, operador = documento_operador, mensaje_2 = mensaje_exitoso)





                # 3
                else:
                    mensaje_error = "¡El cliente no existe en la base de datos!"
                    return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador, mensaje = mensaje_error) 

            # 2
            else:
                mensaje_error = "¡Identificacion del operador invalida!"
                return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador, mensaje = mensaje_error) 
        #  1 
        else:
            # envio mensaje del error
            mensaje_error = "¡No hay productos seleccionados!"
            # muestra el HTML registrar_venta
            return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador, mensaje = mensaje_error) 
        


        

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#---------------------------------------- Elimina Todos los productos seleccionados -------------------------------------------
@app.route("/elimina_todo_seleccionado_p")
def elimina_todo_seleccionado_p():
    if "email_empleado" in session:

        # consulto todos los contadores de carrito_ventas
        sql = "SELECT `contador` FROM `carritoventas`"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        contadores = cursor.fetchall()
        conn.commit()

        # 1 - Valido que aigan productos para eliminar
        if ((len(contadores)) > 0):

            # saco la consulta de [[]] 2 listas a una sola []
            contador_2 = contadores[0]

            # realizo el FOR que elimine uno por uno
            for i in range(len(contador_2)):



                # consulto el id_producto 
                sql = f"SELECT `id_producto` FROM `carritoventas` WHERE contador = '{contador_2[i]}'" # <---- i es el CONTADOR
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                id_pro = cursor.fetchall()
                conn.commit()
                id_producto = id_pro[0][0]

                # consulto el stock disponible que tiene el producto 
                sql = f"SELECT `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                stock_disponible = cursor.fetchall()
                conn.commit()

                # consulto la cantidad seleccionada del producto en el carrito ventas
                sql = f"SELECT `cantidad_adquirida` FROM `carritoventas` WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                cantidad_adquirida = cursor.fetchall()
                conn.commit()

                # sumo al stock disponible la cantidad que adquirida
                stock_disponible = (stock_disponible[0][0] + cantidad_adquirida[0][0])

                # inserto el nuevo stock en la base de datos
                sql = f"UPDATE `productos` SET `cantidad_producto` = '{stock_disponible}' WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                # borro el producto seleccionado de la tabla carrito_ventas
                sql = f"DELETE FROM `carritoventas` WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

            return redirect("/verCrear_ventas")


        # 1
        else:

            # Muestra el documento del operador
            documento_operador = session["doc_empleado"]

            # consulta los productos del inventario
            sql = "SELECT `id_producto`, `referencia_producto`, `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE `estado_producto`= 'ACTIVO'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_inven = cursor.fetchall()
            conn.commit()

            # consulta los productos seleccionados para venta
            sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_carr = cursor.fetchall()
            conn.commit()

            mensaje_error = "¡No hay productos seleccionados para eliminar!"
            return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = 0, operador = documento_operador, mensaje = mensaje_error) 



    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

    

#---------------------------------------- Elimina productos 1 por 1 seleccionados -------------------------------------------
@app.route("/elimina_p_select/<contador>")
def elimina_p_select(contador):
    if "email_empleado" in session:

        # consulto el id_producto 
        sql = f"SELECT `id_producto` FROM `carritoventas` WHERE contador = '{contador}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        id_pro = cursor.fetchall()
        conn.commit()
        id_producto = id_pro[0][0]

        # consulto el stock disponible que tiene el producto 
        sql = f"SELECT `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        stock_disponible = cursor.fetchall()
        conn.commit()

        # consulto la cantidad seleccionada del producto en el carrito ventas
        sql = f"SELECT `cantidad_adquirida` FROM `carritoventas` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        cantidad_adquirida = cursor.fetchall()
        conn.commit()

        # sumo al stock disponible la cantidad que adquirida
        stock_disponible = (stock_disponible[0][0] + cantidad_adquirida[0][0])

        # inserto el nuevo stock en la base de datos
        sql = f"UPDATE `productos` SET `cantidad_producto`='{stock_disponible}' WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        conn.commit()

        # borro el producto seleccionado de la tabla carrito_ventas
        sql = f"DELETE FROM `carritoventas` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        conn.commit()

        return redirect("/verCrear_ventas")

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

    


#---------------------------------------- Selector de 1 cantidad solo producto para Ventas -------------------------------------------
@app.route("/selector_una_cantidad/<id_producto>")
def selector_una_cantidad(id_producto):
    if "email_empleado" in session:

        cantidad_adquirida = 1

        # consulto la cantidad disponible del prodcuto
        sql = f"SELECT `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        stock = cursor.fetchall()
        conn.commit()

         # 1 - valido si la cantidad digitada es menor a la disponible 
        if (stock[0][0] > cantidad_adquirida) or (stock[0][0] == 1 and cantidad_adquirida == 1):

            # consulto la informacion del producto
            sql = f"SELECT `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            info_producto = cursor.fetchall()
            conn.commit()

            # saco la consulta de [[]] 2 listas a una sola []
            info_producto_2 = info_producto[0] 

            # actualizo el stock disponible del producto
            stock_disponible = (info_producto_2[2] - cantidad_adquirida)
            sql = f"UPDATE `productos` SET `cantidad_producto` = '{stock_disponible}' WHERE id_producto = '{id_producto}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            conn.commit()

            # 2 consulto si la cantidad  adquirida en el carrito ventas
            sql = f"SELECT `cantidad_adquirida` FROM `carritoventas` WHERE id_producto = '{id_producto}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            cantidad_carrito = cursor.fetchall()
            conn.commit()
            
            # 2 - valido si ya esta seleccionado el producto
            if ((len(cantidad_carrito)) > 0):
                

                # sumamos la cantidad ya seleccionado con lo digitado
                cantidad_total_adqui = (cantidad_carrito[0][0] + cantidad_adquirida)

                # saco el nuevo total a pagar
                total = (cantidad_total_adqui * info_producto_2[1])

                # actualizo la info del registro de carrito venta
                sql = f"UPDATE `carritoventas` SET `cantidad_adquirida`='{cantidad_total_adqui}',`total`='{total}' WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                return redirect("/verCrear_ventas")



            # 2
            else:

                # inserto los datos en la tabla Carrito ventas
                sql = f"INSERT INTO `carritoventas`(`id_producto`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total`) VALUES ('{id_producto}','{info_producto_2[0]}','{info_producto_2[1]}','{cantidad_adquirida}','{info_producto_2[1]}')"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                return redirect("/verCrear_ventas")

        # 1
        else:

            # Muestra el documento del operador
            documento_operador = session["doc_empleado"]

            # consulta los productos del inventario
            sql = "SELECT `id_producto`, `referencia_producto`, `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE `estado_producto`= 'ACTIVO'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_inven = cursor.fetchall()
            conn.commit()

            # consulta los productos seleccionados para venta
            sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_carr = cursor.fetchall()
            conn.commit()

            # Realiza la suma de el total de todos los productos seleccionados
            sql = "SELECT SUM(total) FROM carritoventas"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql) 
            Suma_total = cursor.fetchall()
            conn.commit()

            mensaje_error = "¡La cantidad solicitada es menor a la disponible!"

            if Suma_total[0][0] is not None:            
                return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador, mensaje = mensaje_error) 
            else:
                return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = 0, operador = documento_operador, mensaje = mensaje_error) 


    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))


#---------------------------------------- Selector de productos para Ventas -------------------------------------------
@app.route("/m_selector_cantidad_p/<id_producto>")
def m_selector_cantidad_p(id_producto):
    if "email_empleado" in session:

        sql = f"SELECT `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        info_producto = cursor.fetchall()
        conn.commit()

        # muestra el html producto_seleccionado donde se digitara la cantidad a comprar del producto
        return render_template('ventas/producto_seleccionado.html',id_p = id_producto, nom_p = info_producto[0])

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))
    


# ------------ Recibe la informacion del FRON-END ---------------------

@app.route("/confirma_p_seleccionado", methods = ['POST'])
def confirma_p_seleccionado():
    if "email_empleado" in session:
        
        # informacion del FRONT-END
        id_producto = request.form['id_producto']
        nombre_producto = request.form['nombre_producto']
        precio_unidad = request.form['precio_unidad']           
        stock_disponible = request.form['Stock_disponible']
        cantidad_digitada = request.form['cantidad_digitada']

        # covierto los valores de texto a numeros 
        precio_unidad = float(precio_unidad)
        stock_disponible = int(stock_disponible)
        cantidad_digitada = int(cantidad_digitada)

        # consulto la cantidad disponible del prodcuto
        sql = f"SELECT `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        stock = cursor.fetchall()
        conn.commit()


        # 1 - valido si la cantidad digitada es menor a la disponible 
        if (stock[0][0] > cantidad_digitada) or (stock[0][0] == 1 and cantidad_digitada == 1):
            
            sql = f"SELECT `cantidad_adquirida` FROM `carritoventas` WHERE id_producto = '{id_producto}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            cantidad_carrito = cursor.fetchall()
            conn.commit()
            
            # 2 - valido si ya esta seleccionado el producto
            if ((len(cantidad_carrito)) > 0):

                # Actualizo el stock disponible del producto 
                stock_disponible = (stock_disponible - cantidad_digitada)

                # Actualizo el stock en la base de datos
                sql = f"UPDATE `productos` SET `cantidad_producto` = '{stock_disponible}' WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                # sumamos la cantidad ya seleccionado con lo digitado
                cantidad_total_adqui = (cantidad_carrito[0][0] + cantidad_digitada)

                # saco el nuevo total a pagar
                total = (cantidad_total_adqui * precio_unidad)

                # actualizo la info del registro de carrito venta
                sql = f"UPDATE `carritoventas` SET `cantidad_adquirida`='{cantidad_total_adqui}',`total`='{total}' WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                return redirect("/verCrear_ventas")


            # 2 inserta normal
            else:
                # Saco el total a pagar por la catidad digitada
                total = (precio_unidad * cantidad_digitada)

                # Actualizo el stock disponible del producto 
                stock_disponible = (stock_disponible - cantidad_digitada)

                # Actualizo el stock en la base de datos
                sql = f"UPDATE `productos` SET `cantidad_producto` = '{stock_disponible}' WHERE id_producto = '{id_producto}'"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                # inserto los datos en la tabla Carrito ventas
                sql = f"INSERT INTO `carritoventas`(`id_producto`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total`) VALUES ('{id_producto}','{nombre_producto}','{precio_unidad}','{cantidad_digitada}','{total}')"
                conn = mysql.connect()
                cursor = conn.cursor()     
                cursor.execute(sql)
                conn.commit()

                return redirect("/verCrear_ventas")
        
        # 1
        else:
            sql = f"SELECT `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE id_producto = '{id_producto}'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            info_producto = cursor.fetchall()
            conn.commit()

            mensaje_error = "¡Cantidad dijitada mayor a la disponible en el stock!"
        
            return render_template('ventas/producto_seleccionado.html',id_p = id_producto, nom_p = info_producto[0], mensaje_Error = mensaje_error)


    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))

#---------------------------------------- Buscador de productos en Ventas -------------------------------------------
@app.route("/Busca_produc_ven", methods = ['POST'])
def Busca_produc_ven():
    if "email_empleado" in session:

        busqueda = request.form['id_nombre']

        # Muestra el documento del operador
        documento_operador = session["doc_empleado"]

        # consulta los productos del inventario segun la busqueda realizada
        sql = f"SELECT `id_producto`, `referencia_producto` , `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos`  WHERE estado_producto ='ACTIVO' AND referencia_producto LIKE '%{busqueda}%' OR estado_producto='ACTIVO' AND nombre_producto LIKE '%{busqueda}%'"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        productos_inven = cursor.fetchall()
        conn.commit()

        # consulta los productos seleccionados para venta
        sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        productos_carr = cursor.fetchall()
        conn.commit()

        # Realiza la suma de el total de todos los productos seleccionados
        sql = "SELECT SUM(total) FROM carritoventas"
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute(sql)
        Suma_total = cursor.fetchall()
        conn.commit()

        # le asigno el 0 si la suma es none
        if Suma_total[0][0] is not None:
            return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador) 
        else:
             return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = 0, operador = documento_operador) 
 

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))



#--------------------------------------------- Muestra registro de venta----------------------------------------------
@app.route("/verCrear_ventas")
def verCrear_ventas():
    if "email_empleado" in session:

        rol = session["rol"]
        if rol == "administrado" or rol == "vendedor":

            # Muestra el documento del operador
            documento_operador = session["doc_empleado"]

            # consulta los productos del inventario
            sql = "SELECT `id_producto`, `referencia_producto`, `nombre_producto`, `precio_venta`, `cantidad_producto` FROM `productos` WHERE `estado_producto`= 'ACTIVO'"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_inven = cursor.fetchall()
            conn.commit()

            # consulta los productos seleccionados para venta
            sql = "SELECT `contador`, `nombre_producto`, `precio_venta`, `cantidad_adquirida`, `total` FROM `carritoventas`"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql)
            productos_carr = cursor.fetchall()
            conn.commit()

            # Realiza la suma de el total de todos los productos seleccionados
            sql = "SELECT SUM(total) FROM carritoventas"
            conn = mysql.connect()
            cursor = conn.cursor()     
            cursor.execute(sql) 
            Suma_total = cursor.fetchall()
            conn.commit()

            # le asigno el 0 si la suma es none
            if Suma_total[0][0] is not None:
                return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = Suma_total[0][0], operador = documento_operador) 
            else:
                return render_template('ventas/registrar_venta.html', prod = productos_inven, prod_carr = productos_carr, Total = 0, operador = documento_operador) 
        
        else:
            return redirect("/inicio")

    else:
        flash('Porfavor inicia sesion para poder acceder')
        return redirect(url_for('home'))



#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------




@app.route('/buscarProvedores', methods=['POST', 'GET'])
def buscarProvedores():
    if request.method == 'POST':
        # Get the search term from the form
        buscar = request.form['buscarProvedor']

        # Query the database
        conn = mysql.connect()
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM proveedores WHERE estado_proveedor = %s AND nom_proveedor LIKE %s", ('ACTIVO', '%' + buscar + '%',))
        results = cursor.fetchall()
        cursor.close()

        return render_template('provedor/buscarProvedor.html', results=results)

    return render_template('provedor/buscarProvedor.html')







if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5090")



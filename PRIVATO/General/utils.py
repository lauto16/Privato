from General.models import Usuario
from Avatares.models import Avatar
from Perfil.models import Post, Busqueda, Notificacion, Amistad, Seguimiento
import bcrypt


# NOTIFICACIONES ------------------------------------------------

def eliminarNotificacionesRelacion(user_actual, user_relacion):

    """ 
    Elimina todas las notificaciones entre dos usuarios
    """

    notificaciones = getNotificaciones(user_actual) + getNotificaciones(user_relacion)

    for noti in notificaciones:

        if ((noti.id_emisor == user_actual.id and noti.id_receptor == user_relacion.id) or
            (noti.id_emisor == user_relacion.id and noti.id_receptor == user_actual.id)):
                
            noti.delete()


def eliminarNotificacion(notificacion):
    try:
        notificacion.delete()
    except:
        pass 


def validacionesNotificacion(id_noti, user_actual):
    """
        Asegurarse que la notificacion:
            1- existe
            2- pertenece a el usuario actual
    """

    try:
        notificacion = Notificacion.objects.get(id=id_noti)
        user_receptor_id = notificacion.id_receptor

        if user_receptor_id == user_actual.id:
            return True, notificacion
        else:
            return False, None
        
    except:
        return False, None

# SEGUIMIENTO ---------------------------------------------------


def generarNotificacion(emisor, receptor, tipo):
    try:
        if tipo == 'follow':
            mensaje = " te ha enviado una solicitud de amistad"
            Notificacion.objects.create(username_emisor=emisor.username,
                                        id_emisor=emisor.id,
                                        id_receptor=receptor.id,
                                        mensaje=mensaje)
            
    except:
        return False


def estadoUser(user_actual, user_page):
    if sonAmigos(user_a=user_actual, user_b=user_page):
        return "Eliminar amistad", "#850234"
    
    elif verificarSeguimiento(user_a=user_actual, user_b=user_page):
        return "Solicitud enviada", "#4ab580"

    else:
        return "Seguir", "#038554"


def eliminarAmistad(user_a, user_b):
    
    amistad = None

    try:
        amistad = Amistad.objects.get(id_usuario_a=user_a.id, id_usuario_b=user_b.id)
    
    except:
        try:
            amistad = Amistad.objects.get(id_usuario_a=user_b.id, id_usuario_b=user_a.id)
        
        except:
            return False
    
    amistad.delete()


def generarSeguimiento(seguidor, seguido):
    try:
        Seguimiento.objects.create(id_seguidor=seguidor.id, id_receptor=seguido.id)
        return True
    except:
        return False


def eliminarSeguimientos(id_user_a, id_user_b):
    try:
        # Intenta eliminar el seguimiento a-b
        seguimiento_ab = Seguimiento.objects.get(id_seguidor=id_user_a, id_receptor=id_user_b)
        seguimiento_ab.delete()

    except:
        pass

    try:
        # Intenta eliminar el seguimiento b-a
        seguimiento_ba = Seguimiento.objects.get(id_seguidor=id_user_b, id_receptor=id_user_a)
        seguimiento_ba.delete()

    except:
        pass


def generarAmistad(id_user_a, id_user_b):

    try:
        amistad = Amistad.objects.create(id_usuario_a=id_user_a, id_usuario_b=id_user_b)
        return amistad
    except:
        return False


def validacionesSeguimiento(user_a, user_b):
    
    """
    Realiza todas las validaciones a la hora de que el usuario sigue a otro usuario
    en caso de haberlo seguido anteriormente o de ya ser amigos, retorna False, de 
    lo contrario retorna True.
    """
    
    son_amigos = sonAmigos(user_a=user_a, user_b=user_b)
    seguido = verificarSeguimiento(user_a=user_a, user_b=user_b)

    if son_amigos or seguido:
        return False

    return True
    

def verificarSeguimiento(user_a, user_b):

    try:
        Seguimiento.objects.get(id_seguidor=user_a.id, id_receptor=user_b.id)
        return True
    
    except:
        return False


def sonAmigos(user_a, user_b):
    
    try:
        Amistad.objects.get(id_usuario_a=user_a.id, id_usuario_b=user_b.id)
        return True
    
    except:

        try:
            Amistad.objects.get(id_usuario_a=user_b.id, id_usuario_b=user_a.id)
            return True
        
        except:
            return False


# BUSQUEDA ------------------------------------------------------


def getLastSearch(user_actual):
    try:

        busquedas = Busqueda.objects.filter(id_usuario=user_actual.id).order_by('-fecha')
        ultima_busqueda = busquedas.first() 
        return ultima_busqueda.busqueda
    
    except:
        return False


def userSearcher(username):
    
    try:
        response = Usuario.objects.get(username=username)
        return True, response
    
    except:
        return False, None


def addBusqueda(busqueda, user_actual):

    try:
        Busqueda.objects.create(id_usuario=user_actual.id, busqueda=busqueda)
        try:
            busquedas = Busqueda.objects.filter(id_usuario=user_actual.id).order_by('-fecha')
            primer_busqueda = busquedas.last()
            if len(busquedas) > 5:
                busqueda_eliminar = Busqueda.objects.get(id=primer_busqueda.id)
                busqueda_eliminar.delete()
        except:
            return False
    except:
        return False

        
# SIGN IN Y LOGIN -----------------------------------------------


def validatePassword(password):

    password = password.lower()
    symbols = False
    numbers = False
    tilde_espacio = False

    for i in password:
        
        if i in ("áéíóú") or i == " ":
            tilde_espacio = True
        if not i.isalnum():
            symbols = True
        if i.isdigit():
            numbers = True
        
    error_messages = []

    if len(password) < 10:
        error_messages.append("La contraseña debe contener al menos 10 caracteres")
    
    if not symbols:
        error_messages.append("La contraseña debe contener al menos un símbolo")
    
    if not numbers:
        error_messages.append("La contraseña debe contener al menos un número")
    
    if tilde_espacio:
        error_messages.append("La contraseña no debe contener tildes o espacios")
    
    if not error_messages:
        return True, None
    
    return False, error_messages


def verifyPassword(password, username):
    try:
        usuario = Usuario.objects.get(username=username)

    except:
        return 'USER_DOES_NOT_EXISTS', None
    
    try:

        hashed_password = usuario.password.encode('utf-8')      
        if (bcrypt.checkpw(password.encode('utf-8'), hashed_password)):      
            return True, usuario
    except:
        return False, None
    
    return False, None


def passwordHashing(password):
    hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    return hashed_password_str


def comprobarUser(usuario, email):

    for char in usuario:
        if not(char.isalnum()):
            return False, "No se permiten simbolos en el nombre de usuario"

    try:
        user = Usuario.objects.get(username=usuario)
        if user:
            return False, "El nombre de usuario ya existe"
    
        
    
    except:

        try:
            Usuario.objects.get(email=email)
        
        except:
            return True, None
        
    return False, "Este email ya esta registrado en una cuenta"


# GETTERS DE USUARIO --------------------------------------------


def getUser(request):
    id_user = None
    if request.user.is_authenticated:
        id_user = request.user.id
        try:
            user_actual = Usuario.objects.get(id=id_user)
            return user_actual
        except:
            return None


def getPosts(user_actual):

    try:
        query_posts = Post.objects.filter(id_usuario=user_actual.id).order_by('-fecha')
        return list(query_posts)
    except:      
        return None


def getNumPosts(request):
    posts = None
    if request.user.is_authenticated:
        posts = request.user.posts
    return posts


def getIdPosts(posts):
    lista_ids = []
    for post in posts:
        lista_ids.append(post.id)
    return lista_ids


def getNotificaciones(user_actual):

    lista_notificaciones = []

    try:
        lista_notificaciones = list(Notificacion.objects.filter(id_receptor=user_actual.id))
    except:
        pass
    
    return lista_notificaciones


# AVATARES -----------------------------------------------------


def getAvatar(user_actual):
    try:
        avatar = Avatar.objects.get(nombre_usuario=user_actual.username)
        return avatar.array_colores
    
    except:
        return None


def tieneAvatar(user_actual):
    try:
        actual_avatar = Avatar.objects.get(nombre_usuario=user_actual.username)
        return True, actual_avatar
    
    except:
        return False, None


def borrarFondo(lista):

    for i in range(len(lista)):
        if lista[i] == "#e9e7e7":
            lista[i] = "x"
    return lista


def comprobarValores(texto):
    if len(texto) > 967:
        return False
    
    for i in texto:
        if not(i.isalnum()) and i != "-":
            return False
    
    return True
        

def completarColores(string_colores):

    lista_colores = []
    
    color = "#"

    for i in range(len(string_colores)):

        if string_colores[i] == "-":
            continue

        elif string_colores[i] == "x":
            lista_colores.append("#e9e7e7")
        
        else:

            caracter = string_colores[i]
            color += caracter
            if len(color) == 7:
                lista_colores.append(color)
                color = "#"

    return lista_colores


def comprimirColores(lista):
    total = ""

    for i in range(len(lista)):
            
        if lista[i] == "x":

            color = "x"
        
        else:
            color = (lista[i])[1:len(lista)-1]
            
        if i == (len(lista) - 1):
            total +=  color

        else:
            total += color + "-"
    
    return total


# UPDATERS -----------------------------------------------------

def updateSeguimiento(user_actual):
    try:
        solicitudes_enviadas = list(Seguimiento.objects.filter(id_seguidor=user_actual.id))
        solicitudes_recibidas = list(Seguimiento.objects.filter(id_receptor=user_actual.id))

    except:
        return None
    
    
    for solicitud_env in solicitudes_enviadas:
        for solicitud_rec in solicitudes_recibidas:

            if (solicitud_env.id_seguidor == solicitud_rec.id_receptor and
                 solicitud_env.id_receptor == solicitud_rec.id_seguidor):
                
                amistad = generarAmistad(id_user_a=user_actual.id, id_user_b=solicitud_rec.id_seguidor)
                eliminarSeguimientos(id_user_a=amistad.id_usuario_a, id_user_b=amistad.id_usuario_b)
                
                try:
                    user_relacion = Usuario.objects.get(id=solicitud_rec.id_seguidor)
                
                except:
                    pass

                eliminarNotificacionesRelacion(user_actual=user_actual, user_relacion=user_relacion)
                

def updatePosts(user_actual):
    
    try:
        id_usuario = user_actual.id
        query_posts = Post.objects.filter(id_usuario=id_usuario)
        lista_posts = list(query_posts)
        user_actual.posts = len(lista_posts)
        user_actual.save()
        return user_actual.posts
    except:
        return 0


def updateAmigos(user_actual):

    try:

        amistadesA = list(Amistad.objects.filter(id_usuario_a=user_actual.id))
        amistadesB = list(Amistad.objects.filter(id_usuario_b=user_actual.id)) 

        user_actual.amigos = (len(amistadesA) + len(amistadesB))
        user_actual.save()
        
        return user_actual.amigos

    except:
        return 0


def addLike(id_post):
    try:
        post = Post.objects.get(id=id_post)
        post.likes += 1
        post.save()
    except:
        return False































































































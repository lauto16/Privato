from .utils import (addBusqueda,
                    completarColores,
                    validatePassword,
                    passwordHashing,
                    comprobarUser, userSearcher,
                    verifyPassword,
                    getUser,
                    getAvatar,
                    getNotificaciones,
                    validacionesNotificacion,
                    generarAmistad,
                    eliminarSeguimientos,
                    eliminarNotificacion,
                    updatePage  
                    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import Register, Login
from .models import Usuario
import json



@login_required
def vista_feed(request):

    user_actual = getUser(request)

    updatePage(user_actual)  
    
    avatar_colores_string = getAvatar(user_actual)
    rango = range(1,122)
    notificaciones = getNotificaciones(user_actual)

    if avatar_colores_string is not None:
    
        colores_completos = completarColores(avatar_colores_string)
        colores_completos_json = json.dumps(colores_completos)

    else:
        return redirect('vista_avatar')

    
    if request.method == "POST":

        peticion = request.POST.get('peticion')

        if peticion == "logout":
            logout(request)
            return redirect('vista_login')

        elif peticion == "config":
            return redirect('vista_config')
        
        elif peticion == "buscar":

            busqueda = request.POST.get('input-busqueda')

            respuesta, usuario = userSearcher(username=busqueda)

            if respuesta:
                
                if usuario.username == user_actual.username:
                    return redirect('vista_perfil') 

                addBusqueda(busqueda, user_actual)
                return redirect('vista_persona')

            return redirect('vista_feed')
            
        elif peticion == "perfil":
            return redirect('vista_perfil')

        elif peticion == "aceptar_notificacion":

            id_noti = request.POST.get('id_noti')
            respuesta_validacion_noti, notificacion = validacionesNotificacion(id_noti=id_noti, user_actual=user_actual)

            if respuesta_validacion_noti:

                amistad = generarAmistad(id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)

                eliminarSeguimientos(id_user_a=amistad.id_usuario_a, id_user_b=amistad.id_usuario_b)
                eliminarNotificacion(notificacion)

            return redirect('vista_feed')

        elif peticion == "denegar_notificacion":
            
            id_noti = request.POST.get('id_noti')
            respuesta_validacion_noti, notificacion = validacionesNotificacion(id_noti=id_noti, user_actual=user_actual)

            if respuesta_validacion_noti:
                eliminarSeguimientos(id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)
                eliminarNotificacion(notificacion)

            return redirect('vista_feed')
            

    return render(request, "feed.html", {
        'colores':colores_completos_json, 
        'form_cerrar_sesion':'logout', 
        'form_config':'config', 
        'form_buscar':'buscar',
        'form_perfil':'perfil',
        'aceptar_notificacion':'aceptar_notificacion',
        'denegar_notificacion':'denegar_notificacion',
        'rango':rango,
        'notificaciones':notificaciones
        })


@login_required
def vista_config(request):
    
    user_actual = getUser(request)

    updatePage(user_actual)  
    
    return render(request, 'config.html')


def vista_login(request):

    if request.method == "POST":

        form = Login(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            resultado, user = verifyPassword(username=username,password=password)
            
            if resultado == 'USER_DOES_NOT_EXISTS' or resultado == False:
                pass   
            

            elif resultado == True:
            
                login(request, user)
                return redirect('vista_feed')



    else:
        form = Login()    

    return render(request, "login.html", {"form": form})


def vista_index(request):

    error = []
    respuesta = False
    reason = ""

    if request.method == "POST":

        form = Register(request.POST)

        if form.is_valid():

            usuario = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']

            if password == password_repeat:
                valida, error = validatePassword(password)

                if valida and not error:

                    respuesta, reason = comprobarUser(usuario, email)

                    if respuesta:

                        try:
                            password = passwordHashing(password)
                            Usuario.objects.create(username=usuario, email=email, password=password, posts=0, amigos=0)
                            return redirect('vista_login')
                        
                        except:
                            pass
                        
                else:

                    return render(request, "index.html", {"form": form, "error": error, 'error_bd':respuesta, "datos_error": reason})

            else:
                error.append("Las contraseñas no son iguales")

        else:
            error.append("El email no es valido")

    else:
        form = Register()

    return render(request, "index.html", {"form": form, "error": error, 'error_bd':respuesta, "datos_error": reason})


# TO DO -------------------------------------------------------------------------------------------
"""
- DARLE CSS A LOS BOTONES DE ACEPTAR Y DENEGAR NOTIFICACIONES
- PERFIL 
- BUSCAR PERFILES
    -DENTRO DEL PERFIL POSIBILIDAD DE SEGUIR Y DEJAR DE SEGUIR
- ELIMINAR AMISTAD
- FEED QUE MUESTRE LAS ULTIMAS PUBLICACIONES DE TUS AMIGOS
- CONFIGURACION
    -BORRAR CUENTA
-CREAR SISTEMA DE COMENTARIOS EN POSTS CON SU MODELO
-PERMITIR DAR ME GUSTA Y COMENTAR
-MODULARIZAR LOGIN Y REGISTER A OTRA APP
-MANEJO DE ERRORES MEDIANTE MODALES QUE DESAPAREZCAN GRADUALMENTE
"""
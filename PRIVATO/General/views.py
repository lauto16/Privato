from .utils import (addBusqueda,
                    completarColores,
                    userSearcher,
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
from django.contrib.auth import logout
import json


@login_required
def vista_feed(request):

    user_actual = getUser(request)

    error = ""

    updatePage(user_actual)
    notificaciones = getNotificaciones(user_actual)

    avatar_colores_string = getAvatar(user_actual)
    rango_avatar = range(1, 122)

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

            respuesta_busqueda, usuario = userSearcher(username=busqueda)

            if respuesta_busqueda:

                if usuario.username == user_actual.username:
                    return redirect('vista_perfil')

                addBusqueda(busqueda, user_actual)
                return redirect('vista_persona')
            else:
                error = "No hay usuarios con ese nombre"

        elif peticion == "perfil":
            return redirect('vista_perfil')

        elif peticion == "aceptar_notificacion":

            id_noti = request.POST.get('id_noti')
            respuesta_validacion_noti, notificacion = validacionesNotificacion(
                id_noti=id_noti, user_actual=user_actual)

            if respuesta_validacion_noti:

                amistad = generarAmistad(
                    id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)

                eliminarSeguimientos(
                    id_user_a=amistad.id_usuario_a, id_user_b=amistad.id_usuario_b)
                eliminarNotificacion(notificacion)
                return redirect('vista_feed')

            error = "No se pudo aceptar la notificacion"

        elif peticion == "denegar_notificacion":

            id_noti = request.POST.get('id_noti')
            respuesta_validacion_noti, notificacion = validacionesNotificacion(
                id_noti=id_noti, user_actual=user_actual)

            if respuesta_validacion_noti:
                eliminarSeguimientos(
                    id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)
                eliminarNotificacion(notificacion)
                return redirect('vista_feed')

            error = "No se pudo denegar la notificacion"

    return render(request, "feed.html", {
        'colores': colores_completos_json,
        'rango': rango_avatar,
        'notificaciones': notificaciones,
        'error': error,
        'form_cerrar_sesion': 'logout',
        'form_config': 'config',
        'form_buscar': 'buscar',
        'form_perfil': 'perfil',
        'aceptar_notificacion': 'aceptar_notificacion',
        'denegar_notificacion': 'denegar_notificacion'
    })


@login_required
def vista_config(request):

    user_actual = getUser(request)

    updatePage(user_actual)

    return render(request, 'config.html')


# TO DO -------------------------------------------------------------------------------------------
"""
- DARLE CSS A LOS BOTONES DE ACEPTAR Y DENEGAR NOTIFICACIONES
- FEED QUE MUESTRE LAS ULTIMAS PUBLICACIONES DE TUS AMIGOS
- CONFIGURACION
    -BORRAR CUENTA
-CREAR SISTEMA DE COMENTARIOS EN POSTS CON SU MODELO
-PERMITIR DAR ME GUSTA Y COMENTAR
"""

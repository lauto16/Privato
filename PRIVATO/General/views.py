from .utils import (addBusqueda,
                    userSearcher,
                    getUser,
                    getNotificaciones,
                    validacionesNotificacion,
                    generarAmistad,
                    eliminarSeguimientos,
                    eliminarNotificacion,
                    updatePage,
                    getListaAmigos,
                    getFriendsPosts,
                    getAvatarImg,
                    tieneAvatar,
                    validacionesComentar,
                    crearComentario,
                    validacionComentarios,
                    getComentarios,
                    formatFecha,
                    validarInput,
                    getUserByPostId
                    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from .forms import Busqueda, Comentar
from .models import Activity
from html import escape
import json


@login_required
def vista_feed(request):

    user_actual = getUser(request)

    error = ""

    updatePage(user_actual)
    lista_amigos = getListaAmigos(user_actual)
    posts_amigos = json.dumps(getFriendsPosts(
        lista_amigos, user_actual, num_posts=3))
    notificaciones = getNotificaciones(user_actual)

    tiene_avatar = tieneAvatar(user_actual)

    if not (tiene_avatar):

        return redirect('vista_avatar')

    avatar_img = getAvatarImg(user_actual=user_actual)

    if request.method == "POST":

        peticion = request.POST.get('peticion')

        if peticion == "logout":
            logout(request)
            return redirect('vista_login')

        elif peticion == "buscar":

            form_add_busqueda = Busqueda(request.POST)

            if form_add_busqueda.is_valid():

                busqueda = escape(
                    form_add_busqueda.cleaned_data['input_busqueda'])

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

        elif peticion == "comentarios":

            id_post = request.POST.get('id_post', None)

            esDiccionario = False
            comentarios_post = "No se encontraron comentarios en el post"

            user_post = getUserByPostId(post_id=id_post)

            if validacionComentarios(id_post=id_post, user_actual=user_actual, user_buscado=user_post, action='persona'):

                comentarios_post, esDiccionario = getComentarios(
                    id_post=id_post)

            response_data = {'comentarios': comentarios_post,
                             'esDiccionario': esDiccionario}

            return JsonResponse(response_data)

        elif peticion == "comentar":

            form_comentar = Comentar(request.POST)

            if form_comentar.is_valid():

                id_post = escape(request.POST.get("id_post_comentar"))
                contenido_comentario = escape(
                    form_comentar.cleaned_data['content_comentario'])

                user_post = getUserByPostId(post_id=id_post)

                if validacionesComentar(user_actual=user_actual, user_buscado=user_post, id_post=id_post, action="persona") and validarInput(input=contenido_comentario):

                    respuesta_crear_comentario, comentario = crearComentario(id_post=id_post, user=user_actual,
                                                                             contenido=contenido_comentario)
                    if respuesta_crear_comentario:

                        response_data = {
                            'success': True,
                            'username': user_actual.username,
                            'fecha': formatFecha(comentario.fecha),
                            'content': contenido_comentario,
                            'src_avatar': getAvatarImg(user_actual).src_imagen.url
                        }

                    else:
                        response_data = {
                            'success': False,
                            'reason': "No se pudo crear el comentario",
                        }

                else:
                    response_data = {
                        'success': False,
                        'reason': "No se pudo validar el post",
                    }

                return JsonResponse(response_data)

        elif peticion == "notificacion":

            id_noti = request.POST.get('id_noti', None)
            action_noti = request.POST.get('action_noti', None)

            if action_noti == 'aceptar_noti':

                respuesta_validacion_noti, notificacion = validacionesNotificacion(
                    id_noti=id_noti, user_actual=user_actual)

                if respuesta_validacion_noti:

                    amistad = generarAmistad(
                        id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)

                    eliminarSeguimientos(
                        id_user_a=amistad.id_usuario_a, id_user_b=amistad.id_usuario_b)

                    eliminarNotificacion(notificacion)

                    response_data = {'success': True, 'id_noti': id_noti}

                else:
                    response_data = {'success': False}

                return JsonResponse(response_data)

            elif action_noti == 'denegar_noti':

                id_noti = request.POST.get('id_noti')

                respuesta_validacion_noti, notificacion = validacionesNotificacion(
                    id_noti=id_noti, user_actual=user_actual)

                if respuesta_validacion_noti:

                    eliminarSeguimientos(
                        id_user_a=notificacion.id_emisor, id_user_b=notificacion.id_receptor)

                    eliminarNotificacion(notificacion)

                    response_data = {'success': True, 'id_noti': id_noti}

                else:
                    response_data = {'success': False}

                return JsonResponse(response_data)

    form_add_busqueda = Busqueda()
    form_add_comentario = Comentar()

    print(posts_amigos)

    return render(request, "feed.html", {
        'avatar': avatar_img.src_imagen.url if avatar_img else '',
        'notificaciones': notificaciones,
        'error': error,
        'form_add_busqueda': form_add_busqueda,
        'form_add_comentario': form_add_comentario,
        'posts_amigos': posts_amigos,
        'form_cerrar_sesion': 'logout',
        'form_buscar': 'buscar',
        'form_perfil': 'perfil',
        'notificacion': 'notificacion',
        'form_comentarios': 'comentarios',
        'form_comentar': 'comentar',

    })

from General.utils import (userSearcher,
                           getLastSearch,
                           getIdPosts,
                           getUser, getPosts,
                           getAvatar, completarColores,
                           validacionesSeguimiento,
                           generarSeguimiento,
                           estadoUser,
                           eliminarAmistad,
                           sonAmigos,
                           generarNotificacion,
                           updatePage,
                           validarInput,
                           formatFecha,
                           getComentarios,
                           validacionComentarios,
                           cambiarFechaPost,
                           validacionesComentar,
                           crearComentario,
                           crearPost,
                           validacionesEliminarPost,
                           eliminarPost
                           )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from General.forms import Posting, Comentar
from html import escape
import json


@login_required
def vista_perfil(request):

    error = ""

    user_actual = getUser(request)

    updatePage(user_actual)

    posts = cambiarFechaPost(getPosts(user_actual))
    ids_posts = json.dumps(getIdPosts(posts))

    avatar_colores_string = getAvatar(user_actual)

    rango_avatar = range(1, 122)

    if avatar_colores_string is not None:

        colores_completos = completarColores(avatar_colores_string)
        colores_completos_json = json.dumps(colores_completos)

    else:
        return redirect('vista_avatar')

    if request.method == "POST":

        peticion = request.POST.get("peticion")

        if peticion == "posteo":

            form_post = Posting(request.POST)

            if form_post.is_valid():

                title = form_post.cleaned_data['title']
                content = form_post.cleaned_data['content']

                if validarInput(input=title):

                    title_filtered = escape(title)
                    content_filtered = escape(content)

                    respuesta_crear_post, new_post = crearPost(
                        id_usuario=user_actual.id, title=title_filtered, contenido=content_filtered, comentarios=0)

                    if respuesta_crear_post:

                        fecha_formateada = formatFecha(fecha=new_post.fecha)

                        response_data = {'success': True,
                                         'post_title': new_post.title,
                                         'post_contenido': new_post.contenido,
                                         'post_comentarios': new_post.comentarios,
                                         'post_fecha': fecha_formateada,
                                         'post_id': new_post.id
                                         }
                    else:
                        response_data = {'success': False,
                                         'reason': "Error al crear el post"}

                return JsonResponse(response_data)

        elif peticion == "comentarios":

            id_post = request.POST.get('id_post', None)

            esDiccionario = False
            comentarios_post = "No se encontraron comentarios en el post"

            if validacionComentarios(id_post=id_post, user_actual=user_actual, user_buscado=None, action='perfil'):

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

                if validacionesComentar(user_actual=user_actual, user_buscado=None, id_post=id_post, action="perfil") and validarInput(input=contenido_comentario):

                    respuesta_crear_comentario, comentario = crearComentario(id_post=id_post, user=user_actual,
                                                                             contenido=contenido_comentario)
                    if respuesta_crear_comentario:

                        response_data = {
                            'success': True,
                            'username': user_actual.username,
                            'fecha': formatFecha(comentario.fecha),
                            'content': contenido_comentario
                        }

                    else:
                        response_data = {
                            'success': False,
                            'reason': "No se pudo crear el comentario",
                        }

                else:
                    response_data = {
                        'success': False,
                        'reason': "No se pudo agregar el comentario",
                    }

                return JsonResponse(response_data)

        elif peticion == "eliminar_post":

            id_post = request.POST.get('id_post')

            if validacionesEliminarPost(id_post=id_post, user_actual=user_actual):

                if eliminarPost(id_post=id_post):

                    response_data = {
                        'success': True,
                        'id_post': id_post
                    }

                else:
                    response_data = {
                        'success': False,
                        'reason': "No se pudo eliminar el post"
                    }

            else:
                response_data = {
                    'success': False,
                    'reason': "No se pudo eliminar el post"
                }

            return JsonResponse(response_data)

        elif peticion == "avatar":
            return redirect('vista_avatar')

    form_post = Posting()
    form_comentar = Comentar()

    return render(request, "perfil.html", {
        'username': user_actual.username,
        'num_posts': user_actual.posts,
        'amigos': user_actual.amigos,
        'colores': colores_completos_json,
        'rango': rango_avatar,
        'posts': posts,
        'ids_posts': ids_posts,
        'error': error,
        'form_add_post': form_post,
        'form_add_comentario': form_comentar,
        'form_post': 'posteo',
        'form_avatar': 'avatar',
        'form_comentarios': 'comentarios',
        'form_comentar': 'comentar',
        'form_eliminar_post': 'eliminar_post'
    })


@login_required
def vista_persona(request):

    error = ""

    rango_avatar = range(1, 122)
    user_actual = getUser(request)

    posts = []
    ids_posts = []

    username_busqueda = getLastSearch(user_actual)
    respuesta, user_buscado = userSearcher(username_busqueda)

    updatePage(user_actual)
    updatePage(user_buscado)

    estado_seguimiento, color_boton_seguir = estadoUser(
        user_actual=user_actual, user_page=user_buscado)
    son_amigos = sonAmigos(user_a=user_actual, user_b=user_buscado)

    if son_amigos:
        posts = cambiarFechaPost(getPosts(user_buscado))
        ids_posts = json.dumps(getIdPosts(posts))

    avatar_colores_string = getAvatar(user_buscado)
    colores_completos_json = ""

    if avatar_colores_string is not None:

        colores_completos = completarColores(avatar_colores_string)
        colores_completos_json = json.dumps(colores_completos)

    if not (respuesta):
        return redirect('vista_feed')

    if request.method == "POST":

        peticion = request.POST.get('peticion')

        if peticion == "agregar":

            respuesta_seguir = validacionesSeguimiento(
                user_a=user_actual, user_b=user_buscado)

            # No son amigos
            if respuesta_seguir:
                generarSeguimiento(seguidor=user_actual, seguido=user_buscado)
                generarNotificacion(emisor=user_actual,
                                    receptor=user_buscado,
                                    tipo='follow')
            # Si son amigos
            else:
                eliminarAmistad(user_a=user_actual, user_b=user_buscado)

            return redirect('vista_persona')

        elif peticion == "comentarios":

            id_post = request.POST.get('id_post', None)

            esDiccionario = False
            comentarios_post = "No se encontraron comentarios en el post"

            if validacionComentarios(id_post=id_post, user_actual=user_actual, user_buscado=user_buscado, action='persona'):

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

            if validacionesComentar(user_actual=user_actual, user_buscado=user_buscado, id_post=id_post, action="persona") and validarInput(input=contenido_comentario):

                respuesta_crear_comentario, comentario = crearComentario(id_post=id_post, user=user_actual,
                                                                         contenido=contenido_comentario)
                if respuesta_crear_comentario:

                    response_data = {
                        'success': True,
                        'reason': None,
                        'username': user_actual.username,
                        'fecha': formatFecha(comentario.fecha),
                        'content': escape(contenido_comentario)
                    }

                else:
                    response_data = {
                        'success': False,
                        'username': None,
                        'fecha': None,
                        'reason': "No se pudo crear el comentario",
                        'content': ""
                    }

            else:
                response_data = {
                    'success': False,
                    'username': None,
                    'fecha': None,
                    'reason': "No se pudo agregar el comentario",
                    'content': ""
                }

            return JsonResponse(response_data)

    form_comentar = Comentar()

    return render(request, 'persona.html', {
        'username': user_buscado.username,
        'num_posts': user_buscado.posts,
        'amigos': user_buscado.amigos,
        'colores': colores_completos_json,
        'rango': rango_avatar,
        'ids_posts': ids_posts,
        'posts': posts,
        'estado_seguimiento': estado_seguimiento,
        'color_boton_seguir': color_boton_seguir,
        'error': error,
        'form_add_comentario': form_comentar,
        'son_amigos': son_amigos,
        'form_agregar': 'agregar',
        'form_comentarios': 'comentarios',
        'form_comentar': 'comentar'
    })

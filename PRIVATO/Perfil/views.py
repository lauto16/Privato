from General.utils import (userSearcher,
                           addLike,
                           getLastSearch,
                           getIdPosts, updatePosts,
                           getUser, getPosts,
                           getAvatar, completarColores,
                           validacionesSeguimiento,
                           generarSeguimiento,
                           estadoUser,
                           eliminarAmistad,
                           sonAmigos,
                           generarNotificacion,
                           updatePage
                           )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from General.forms import Posting
from .models import Post
import json


@login_required
def vista_perfil(request):

    error = ""

    user_actual = getUser(request)

    updatePage(user_actual)

    posts = getPosts(user_actual)
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

            form = Posting(request.POST)

            if form.is_valid():

                title = form.cleaned_data['title']
                content = form.cleaned_data['content']

                if title != "":

                    try:
                        new_post = Post.objects.create(
                            id_usuario=user_actual.id, title=title, contenido=content, comentarios=0)

                        new_post_title = new_post.title
                        new_post_contenido = new_post.contenido
                        new_post_comentarios = new_post.comentarios

                        response_data = {'post_title': new_post_title,
                                         'post_contenido': new_post_contenido,
                                         'post_comentarios': new_post_comentarios
                                         }

                        return JsonResponse(response_data)

                    except Exception as e:
                        print(e)

        elif peticion == "avatar":
            return redirect('vista_avatar')

    form = Posting()

    return render(request, "perfil.html", {
        'username': user_actual.username,
        'num_posts': user_actual.posts,
        'amigos': user_actual.amigos,
        'colores': colores_completos_json,
        'rango': rango_avatar,
        'posts': posts,
        'form_post': 'posteo',
        'form_avatar': 'avatar',
        'ids_posts': ids_posts,
        'error': error,
        'form': form
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

        posts = getPosts(user_buscado)
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
        'son_amigos': son_amigos,
        'form_agregar': 'agregar',
    })

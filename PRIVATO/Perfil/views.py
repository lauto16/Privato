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
from General.models import Usuario
from General.forms import Posting
from .models import Post
import json



@login_required
def vista_perfil(request):

    user_actual = getUser(request)

    updatePage(user_actual)  

    posts = getPosts(user_actual)
    ids_posts = json.dumps(getIdPosts(posts))
    
    avatar_colores_string = getAvatar(user_actual)
    
    rango = range(1,122)



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
                        Post.objects.create(id_usuario=user_actual.id, title=title, contenido=content, likes=0, comentarios=0)
                    except:
                        # No se pudo crear el post, manejar el error
                        pass

                updatePosts(user_actual)
                return redirect('vista_perfil')

        elif peticion == "avatar":
            return redirect('vista_avatar')

    return render(request, "perfil.html", {
        'username':user_actual.username, 
        'num_posts':user_actual.posts, 
        'amigos':user_actual.amigos, 
        'colores':colores_completos_json, 
        'rango':rango,
        'posts':posts,
        'form_post':'posteo',
        'form_avatar':'avatar',
        'ids_posts':ids_posts,
    })



@login_required
def vista_persona(request):

    rango = range(1,122)
    user_actual = getUser(request)

    posts = []
    ids_posts = []

    username_busqueda = getLastSearch(user_actual)
    respuesta, user_buscado = userSearcher(username_busqueda)

    updatePage(user_actual)    
    updatePage(user_buscado)
    
    estado_seguimiento, color_boton_seguir = estadoUser(user_actual=user_actual, user_page=user_buscado)

    if sonAmigos(user_a=user_actual, user_b=user_buscado):

        posts = getPosts(user_buscado)
        ids_posts = json.dumps(getIdPosts(posts))

    avatar_colores_string = getAvatar(user_buscado)

    colores_completos_json = ""

    if avatar_colores_string is not None:

        colores_completos = completarColores(avatar_colores_string)
        colores_completos_json = json.dumps(colores_completos)
    
    if not(respuesta):
        return redirect('vista_feed')
    
    if request.method == "POST":

        peticion = request.POST.get('peticion')

        if peticion == "agregar":
            
            respuesta_seguir = validacionesSeguimiento(user_a=user_actual,user_b=user_buscado)

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

    return render(request, 'persona.html',{
        'username':user_buscado.username,
        'num_posts':user_buscado.posts,
        'amigos':user_buscado.amigos,
        'colores':colores_completos_json, 
        'rango':rango,    
        'ids_posts':ids_posts,
        'posts':posts,
        'estado_seguimiento':estado_seguimiento,
        'color_boton_seguir':color_boton_seguir,
        'form_agregar':'agregar'
    })







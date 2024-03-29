from .img_generator import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from General.utils import (borrarFondo,
                           comprimirColores,
                           comprobarValores,
                           getUser,
                           updatePage,
                           crearAvatarImg
                           )
from PRIVATO.settings import BASE_DIR
import os


@login_required
def vista_avatar(request):

    rango = range(121)
    rango_grid = range(1, 122)
    valores_colores = []
    error = ""

    user_actual = getUser(request)
    updatePage(user_actual)

    path_imgs = "avatares/" + user_actual.username + ".jpg"
    path_imgs_completo = "/home/lauty_/Desktop/PROYECTOS/PRIVATO/PRIVATO/General/media/avatares/" + \
        user_actual.username + ".jpg"

    if request.method == 'POST':

        for i in range(121):
            nombre_input = 'color_' + str(i)
            valor_input = request.POST.get(nombre_input)
            valores_colores.append(valor_input)

        valores_colores = borrarFondo(valores_colores)
        valores_comprimidos = comprimirColores(valores_colores)
        respuesta = comprobarValores(valores_comprimidos)

        if respuesta:

            if user_actual.username != None:

                try:

                    respuesta_crear_img = crearImg(array_colores=formatColores(valores_comprimidos), color_base=(
                        hex_to_rgb('e9e7e7')), path=path_imgs_completo)

                    if respuesta_crear_img:

                        crearAvatarImg(
                            path=path_imgs, user_actual=user_actual)

                        return redirect('vista_perfil')

                except:
                    error = "No se pudo crear el avatar, intentelo de nuevo"

            else:
                error = "Usuario no logueado"

        else:
            error = "No se pudo crear el avatar, intentelo de nuevo"

    return render(request, 'avatar.html', {'rango_grid': rango_grid, 'rango': rango, 'error': error})

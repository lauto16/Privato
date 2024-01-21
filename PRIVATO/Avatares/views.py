from Avatares.models import Avatar
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from General.utils import (borrarFondo,
                           comprimirColores,
                           comprobarValores,
                           getUser,
                           tieneAvatar,
                           updatePage
                           )


@login_required
def vista_avatar(request):

    rango = range(121)
    rango_grid = range(1, 122)
    valores_colores = []
    error = ""

    user_actual = getUser(request)

    updatePage(user_actual)

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

                    respuesta_avatar, avatar_actual = tieneAvatar(user_actual)

                    if respuesta_avatar:
                        avatar_actual.delete()

                    Avatar.objects.create(
                        nombre_usuario=user_actual.username, array_colores=valores_comprimidos)
                    return redirect('vista_perfil')

                except:
                    error = "No se pudo crear el avatar, intentelo de nuevo"

            else:
                error = "Usuario no logueado"

        else:
            error = "No se pudo crear el avatar, intentelo de nuevo"

    return render(request, 'avatar.html', {'rango_grid': rango_grid, 'rango': rango, 'error': error})

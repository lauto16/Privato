from Auth.auth_utils import (
    validatePassword,
    passwordHashing,
    comprobarUser,
    verifyPassword,
)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from General.forms import Register, Login
from General.models import Usuario


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
                            Usuario.objects.create(
                                username=usuario, email=email, password=password, posts=0, amigos=0)
                            return redirect('vista_login')

                        except:
                            error.append("No se pudo crear la cuenta")

                else:

                    return render(request, "index.html", {"form": form, "error": error, 'error_bd': respuesta, "datos_error": reason})

            else:
                error.append("Las contraseñas no son iguales")

        else:
            error.append("El email no es valido")

    else:
        form = Register()

    return render(request, "index.html", {"form": form, "error": error, 'error_bd': respuesta, "datos_error": reason})


def vista_login(request):

    error = ""

    if request.method == "POST":

        form = Login(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            resultado, user = verifyPassword(
                username=username, password=password)

            if resultado == 'USER_DOES_NOT_EXISTS' or resultado == False:
                error = "El usuario o la contraseña no son correctos"

            elif resultado == True:

                login(request, user)
                return redirect('vista_feed')

    else:
        form = Login()

    return render(request, "login.html", {"form": form, "error": error})

from django import forms


class Register(forms.Form):
    username = forms.CharField(label="", max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Nombre de usuario'}))
    email = forms.EmailField(label="", max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Correo electrónico'}))
    password = forms.CharField(label="", max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Contraseña'}))
    password_repeat = forms.CharField(label="", max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Repetir contraseña'}))


class Login(forms.Form):
    username = forms.CharField(label="", max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label="", max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Contraseña'}))


class Posting(forms.Form):
    title = forms.CharField(required=True, label="", max_length=80, widget=forms.TextInput(
        attrs={'placeholder': 'Titulo de la publicacion'}))
    content = forms.CharField(required=False, label="", max_length=952, widget=forms.Textarea(
        attrs={'placeholder': '¿Que quieres compartir hoy?'}))

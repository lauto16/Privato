from django.contrib import admin
from django.urls import path
from General.views import *
from Avatares.views import *
from Perfil.views import * 
from Auth.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', vista_feed, name="vista_feed"),
    path('index/', vista_index, name="vista_index"),
    path('login/', vista_login, name="vista_login"),
    path('avatar/', vista_avatar, name="vista_avatar"),
    path('config/', vista_config, name="vista_config"),
    path('perfil/', vista_perfil, name="vista_perfil"),
    path('persona/', vista_persona, name="vista_persona"),
]

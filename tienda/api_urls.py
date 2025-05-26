from django.urls import path

from .api_views import *


urlpatterns = [
    path('listar_piezas/', listar_piezas),

]
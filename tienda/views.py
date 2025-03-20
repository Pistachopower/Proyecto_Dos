from django.shortcuts import render
from .models import *

# Create your views here.
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    return render(request, 'clientes/lista_cliente.html',{'clientes_mostrar':clientes})


def index(request):
    return render(request, 'index.html',{})
    

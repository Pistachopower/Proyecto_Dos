from django.shortcuts import render
from .models import *

# Create your views here.
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    
    return render(request, 'clientes/clientes.html',{'clientes_mostrar':clientes})

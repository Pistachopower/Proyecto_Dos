from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from .forms import *

# Create your views here.
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    return render(request, 'clientes/lista_cliente.html',{'clientes_mostrar':clientes})


def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
        
    return render(request, 'index.html',{})
    
def registrar_usuario(request):
    if request.method == 'POST':
        #recogemos los datos del formulario
        formulario= RegistroForm(request.POST)
        
        if formulario.is_valid():
            user= formulario.save()
            return redirect('index')

    else:    
        formulario= RegistroForm()
    return render(request, 'registration/signup.html',{'formulario':formulario})
    




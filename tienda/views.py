from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

#skjnceod@56

@permission_required('tienda.view_cliente')
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    return render(request, 'clientes/lista_cliente.html',{'clientes_mostrar':clientes})

@permission_required('tienda.view_vendedor')
def lista_vendedores(request):
    vendedores= Vendedor.objects.all() 
    return render(request, 'vendedores/lista_vendedores.html',{'vendedores_mostrar':vendedores})


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
            rol= int(formulario.cleaned_data.get('rol'))
            
            if (rol == Usuario.CLIENTE):
                grupo= Group.objects.get(name='Clientes')
                grupo.user_set.add(user)
                
                #se asocia el cliente con usuario
                cliente= Cliente.objects.create(usuario=user)
                cliente.save()
                
            elif (rol == Usuario.VENDEDOR):
                grupo= Group.objects.get(name='Vendedores')
                grupo.user_set.add(user)
                
                #se asocia el vendedor con usuario
                vendedor= Vendedor.objects.create(usuario=user)
                vendedor.save()
                
            login(request, user)
            return redirect('index')

    else:    
        formulario= RegistroForm()
    return render(request, 'registration/signup.html',{'formulario':formulario})





    




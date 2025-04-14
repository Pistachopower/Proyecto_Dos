from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib import messages


def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
        
    return render(request, 'index.html',{})


@permission_required('tienda.view_cliente')
def lista_clientes(request):
    clientes= Cliente.objects.all() 
    return render(request, 'clientes/lista_cliente.html',{'clientes_mostrar':clientes})

@permission_required('tienda.view_vendedor')
def lista_vendedores(request):
    vendedores= Vendedor.objects.all() 
    return render(request, 'vendedores/lista_vendedores.html',{'vendedores_mostrar':vendedores})


def registrar_usuario(request):
    if request.method == 'POST':
        #recogemos los datos del formulario
        formulario= RegistroForm(request.POST)
        
        if formulario.is_valid():
            user= formulario.save()
            rol= int(formulario.cleaned_data.get('rol'))
            
            if (rol == Usuario.CLIENTE):
                grupo= Group.objects.get(name='clientes')
                grupo.user_set.add(user)
                
                #se asocia el cliente con usuario
                cliente= Cliente.objects.create(usuario=user)
                cliente.save()
                
            elif (rol == Usuario.VENDEDOR):
                grupo= Group.objects.get(name='vendedores')
                grupo.user_set.add(user)
                
                #se asocia el vendedor con usuario
                vendedor= Vendedor.objects.create(usuario=user)
                vendedor.save()
                
            login(request, user)
            return redirect('index')

    else:    
        formulario= RegistroForm()
    return render(request, 'registration/signup.html',{'formulario':formulario})


@permission_required('tienda.view_pieza')
def lista_pieza(request):
    pieza= Pieza.objects.all() 
    return render(request, 'piezas/lista_pieza.html',{'piezas_mostrar':pieza})


@permission_required('tienda.add_pieza')
def pieza_create(request):
    if request.method == "POST":
        formulario= PiezaModelForm(request.POST)
        
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la pieza")
              
            return redirect("lista_pieza")
    else:
        formulario= PiezaModelForm()
    return render(request, 'piezas/pieza_form.html',{'formulario':formulario})




def dame_producto(request, id_pieza):
    pieza= Pieza.objects.get(id=id_pieza)
    
    return render(request, 'piezas/pieza_id.html',{'pieza':pieza})

@permission_required('tienda.change_pieza')
def pieza_editar(request, id_pieza):
    pieza= Pieza.objects.get(id=id_pieza)
    
    if request.method == "POST":
        #request.POST: recogemos los datos del formulario escritos del usuario
        #instance: recogemos el objeto que queremos editar
        formulario= PiezaModelForm(request.POST, instance=pieza)
        
        #si no hay errores de las validaciones del formulario
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la pieza")
            
            return redirect("dame_producto", id= pieza.id )
            #return redirect("lista_pieza")
        

    else:
        formulario= PiezaModelForm(instance=pieza)
        
    return render(request, 'piezas/pieza_editar.html',{'formulario':formulario, 'pieza': pieza })


@permission_required('tienda.delete_pieza')
def pieza_eliminar(request, id_pieza):
    pieza= Pieza.objects.get(id= id_pieza)
    
    try:
        pieza.delete()
        messages.success(request, "Se ha elimnado la pieza "+ pieza.nombre+" correctamente")

    except Exception as error:
        print(error)
    return redirect('lista_pieza')

#Modelo tienda
#TODO: hacer try catch en consultas de la bd
@permission_required('tienda.view_tienda')
def lista_tienda(request):
    tienda= Tienda.objects.all() 
    return render(request, 'tienda/lista_tienda.html',{'tienda_mostrar':tienda})



@permission_required('tienda.add_tienda')
def tienda_create(request):
    if request.method == "POST":
        formulario= TiendaModelForm(request.POST)
        
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            return redirect("lista_tienda")
    else:
        formulario= TiendaModelForm()
    return render(request, 'tienda/tienda_form.html',{'formulario':formulario})



def dame_tienda(request, id_tienda):
    tienda= Tienda.objects.get(id=id_tienda)
    
    return render(request, 'tienda/tienda_detalle.html',{'tienda':tienda})

@permission_required('tienda.change_tienda')
def tienda_editar(request, id_tienda):
    tienda= Tienda.objects.get(id=id_tienda)
    
    if request.method == "POST":
        
        formulario= TiendaModelForm(request.POST, instance=tienda)
        
        if formulario.is_valid():
            print("Es valido")
            formulario.save()
            
            messages.success(request, "Se ha editado la tienda")
            

            return redirect("lista_tienda" )

        

    else:
        formulario= TiendaModelForm(instance=tienda)
        
    return render(request, 'tienda/tienda_editar.html',{'formulario':formulario, 'tienda': tienda }) #'tienda': tienda: es cuando el formulario vacio
    
    
    
#modelo cuenta bancaria
def perfil_cliente(request, id_cliente):
    cliente= Cliente.objects.get(id=id_cliente)
    
    if not cliente:
        return redirect('index')
    
    # Verificar si el cliente tiene una cuenta bancaria
    cuentaCliente = CuentaBancaria.objects.filter(cliente=cliente).first()
    
    
        
    return render(request, 'perfil/perfil_cliente.html',{'cuentaCliente':cuentaCliente, 'cliente':cliente})


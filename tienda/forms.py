from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import ModelForm


class RegistroForm(UserCreationForm): 
    roles = (
                (Usuario.CLIENTE, 'cliente'),
                (Usuario.VENDEDOR, 'vendedor'),
            )   
    
    
    rol = forms.ChoiceField(choices=roles)
    
    
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2','rol')
        
        
        
class PiezaModelForm(ModelForm):
    class Meta:     #aqui sobreescribimos al padre ModelForm que tiene sus campos
        model = Pieza
        fields = ['nombre', 'version', 'referencia', 'estado', 'descripcion', 'marca', 'precio', 'anio']
        labels = { #esto es lo que va dentro del campo
            "nombre": ("Nombre de la pieza"),
            "descripcion": ("Descripcion de la pieza"),
            "anio": ("Año de la pieza"),
        }
        

        
        help_texts = {
            "nombre": ("10 caracteres como mínimo"),
            "descripcion":("Agrega una descripción de la pieza"),
        }
        
        #Definimos un campo Select para seleccionar el estado de la pieza
        estado = forms.ChoiceField(choices=Pieza.ESTADO,
                               initial="R")
        
        
    def clean(self): #este es para validar 
        
        super().clean() # comprueba las validaciones que tiene por defecto
        
        nombre = self.cleaned_data.get('nombre')
        version = self.cleaned_data.get('version')
        referencia = self.cleaned_data.get('referencia')
        descripcion = self.cleaned_data.get('descripcion')
        marca = self.cleaned_data.get('marca')
        precio = self.cleaned_data.get('precio')
        anio= self.cleaned_data.get('anio')
        
        if len(nombre) < 3:
            self.add_error('nombre','Al menos debes indicar 3 caracteres')
            
        if len(version) < 3:
            self.add_error('version','Al menos debes indicar 3 caracteres')
            
        if len(referencia) < 3:
            self.add_error('referencia','Al menos debes indicar 3 caracteres')
 
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 10 caracteres')
            
        if len(marca) < 2: 
            self.add_error('marca','Al menos debes indicar 2 caracteres')
                      
        if precio < 0:
            self.add_error('precio','El precio no puede ser negativo o cero')
            
        if anio < 1900:
            self.add_error('anio','El año no puede ser menor a 1900')
                   
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data            
        
        
class TiendaModelForm(ModelForm):
    class Meta:   
        model = Tienda
        fields = ['direccion', 'telefono', 'email']
        
    def clean(self): #este es para validar 
        super().clean() # comprueba las validaciones que tiene por defecto
        
        direccion = self.cleaned_data.get('direccion')
        telefono = self.cleaned_data.get('telefono')
        email = self.cleaned_data.get('email')
        
        if len(direccion) < 5: 
            self.add_error('direccion','Al menos debes indicar 5 caracteres')
            
        if len(telefono) < 7:
            self.add_error('telefono','Al menos debes indicar 7 digitos')
        
        # Verifica si el correo tiene mayúsculas
        if email != email.lower():
            self.add_error('email','No puede conteneder mayúsculas')
        
        return self.cleaned_data  

        
class CuentaBancariaModelForm(ModelForm):
    class Meta:   
        model = CuentaBancaria
        fields = ['iban', 'banco', 'moneda']   
        
        moneda = forms.ChoiceField(choices=CuentaBancaria.MONEDA,
                               initial="EUR")
        
        help_texts = {
            "iban": ("Ejemplo de IBAN: ES1234567890123456789012"),
        }
        
    def clean(self):
        super().clean() 
        
        ibam = self.cleaned_data.get('iban')
        banco = self.cleaned_data.get('banco')
                
        if len(ibam) < 22 or len(ibam) > 34:
            self.add_error('iban', 'El IBAN debe tener entre 15 y 34 caracteres')
            
        if len(banco) < 3:
            self.add_error('banco','Al menos debes indicar 3 caracteres')
            
        return self.cleaned_data    
    
    
class DatosVendedorModelForm(ModelForm):
    class Meta:   
        model = DatosVendedor
        fields = ['direccion', 'facturacion']   
        
        
    def clean(self):
        super().clean() 
        
        direccion = self.cleaned_data.get('direccion')
        facturacion = self.cleaned_data.get('facturacion')
                
        if len(direccion) < 2:
            self.add_error('direccion', 'La dirección debe tener al menor 2 caracteres')
            
        if len(facturacion) < 3:
            self.add_error('facturacion','Al menos debes indicar 3 caracteres')
            
        return self.cleaned_data         
    
    
    
class DatosVendedorModelForms(ModelForm):
    class Meta:
        model = DatosVendedor 
        fields = ['direccion', 'facturacion']  
        help_texts = {
            'direccion' : ("Direccion del vendedor"),
            'facturacion': ("Facturacion del vendedor"),
        }      

        
        
class DatosVendedorModelForms(ModelForm):
    class Meta:
        model = Inventario 
        fields = ['tienda', 'pieza','cantidad']  
        help_texts = {
            'tienda' : ("Selecciona la tienda"),
            'pieza' : ("Selecciona la pieza"),
            'cantidad': ("Indica la cantidad"),
        }  
        
    #se usa esto para obtener solo las tiendas que puede ver el usuario loggeado
    def __init__(self, *args, **kwargs):
        self.request= kwargs.pop("request")
        super(DatosVendedorModelForms, self).__init__(*args, **kwargs)
        tiendasDisponibles= Tienda.objects.filter(vendedor_id= self.request.user.vendedor).all()
        self.fields["tienda"]= forms.ModelChoiceField(
            queryset= tiendasDisponibles, 
            widget=forms.Select,
            required= True,
            empty_label= "Ninguna"
        )
        
class DatosInventarioModelForms(ModelForm):
    class Meta:
        model = Inventario 
        fields = ['tienda','pieza','cantidad']  
        help_texts = {
            'cantidad': ("Indica la cantidad"),
        }  
            
        
        
        
#busqueda de piezas
class BusquedaPiezaModelForm(forms.Form):  
    nombre = forms.CharField(required=False, label="Nombre")
        
        
            
        
        

            
        
        
        
        
        

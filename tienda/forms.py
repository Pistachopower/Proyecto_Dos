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
        fields = ['nombre','descripcion','marca','precio']
        labels = { #esto es lo que va dentro del campo
            "nombre": ("Nombre de la pieza"),
            "descripcion": ("Descripcion de la pieza"),
        }
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
            "descripcion":("Agrega la ficha técnica")
        }
        
        
    def clean(self): #este es para validar 
        
        super().clean() # comprueba las validaciones que tiene por defecto
        
        nombre = self.cleaned_data.get('nombre')
        
        if len(nombre) < 10:
            self.add_error('nombre','Al menos debes indicar 10 caracteres')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data            
        
        
        
        
        
        
        
        
        

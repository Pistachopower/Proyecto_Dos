from django.contrib.auth.forms import UserCreationForm
from django import forms
from tienda.models import *


class RegistroForm(UserCreationForm): 
    roles = (
                (Usuario.CLIENTE, 'cliente'),
                (Usuario.VENDEDOR, 'vendedor'),
            )   
    
    
    rol = forms.ChoiceField(choices=roles)
    
    
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2','rol')
        
        
        
        

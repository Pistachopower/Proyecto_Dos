from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administardor'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'vendedor'),
    )
    
    rol  = models.PositiveSmallIntegerField(
        choices=ROLES,default=2
    )


#cliente y usuario usara los atributos de Usuario 
class Cliente(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.usuario.username  
    


class Vendedor(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.usuario.username
    
    
    
class Pieza(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion= models.TextField()
    marca= models.CharField(max_length=100)
    precio= models.FloatField(default=0.0) 
    
    def __str__(self):
        return self.nombre
    
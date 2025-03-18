from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre + " "+ self.apellidos


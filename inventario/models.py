from django.db import models
from django.contrib.auth.models import AbstractUser, User, Group, Permission

class PerfilUsuario(AbstractUser):
    JEFEBODEGA = 'JF'
    BODEGUERO = 'BD'
    ROLES_USUARIO = [
        (JEFEBODEGA, 'Jefe de Bodega'),
        (BODEGUERO, 'Bodeguero'),
    ]
    rol = models.CharField(max_length=2, choices=ROLES_USUARIO, default=BODEGUERO)

    def es_jefe_bodega(self):
        return self.rol == self.JEFEBODEGA

    def es_bodeguero(self):
        return self.rol == self.BODEGUERO
    
    groups = models.ManyToManyField(Group, related_name='perfil_usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='perfil_usuarios')
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    # Agrega otros atributos relacionados con el producto según tus necesidades

class Bodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Movimiento(models.Model):
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_salida')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_entrada')
    productos = models.ManyToManyField(Producto, through='DetalleMovimiento')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

from django import forms
from inventario.models import Producto, Bodega, Movimiento, DetalleMovimiento
from django.contrib.auth.forms import UserCreationForm
from inventario.models import PerfilUsuario

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = PerfilUsuario
        fields = ('username', 'password1', 'password2', 'rol')


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ('bodega_origen', 'bodega_destino', 'productos',)

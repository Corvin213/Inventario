from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Bodega, Movimiento, DetalleMovimiento
from .forms.forms import ProductoForm, BodegaForm, MovimientoForm, RegistroForm


def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

@login_required
def gestion_bodegas(request):
    bodegas = Bodega.objects.all()
    return render(request, 'gestion_bodegas.html', {'bodegas': bodegas})

@login_required
def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            form.save_m2m()
            return redirect('lista_movimientos')
    else:
        form = MovimientoForm()
    return render(request, 'crear_movimiento.html', {'form': form})

@login_required
def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'lista_movimientos.html', {'movimientos': movimientos})

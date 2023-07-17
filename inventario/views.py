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
def crear_detalle_movimiento(request):
    if request.method == 'POST':
        form = DetalleMovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_bodegas')
    else:
        form = DetalleMovimientoForm()

    return render(request, 'crear_detalle_movimiento.html', {'form': form})

@login_required
def crear_producto(request):
    # Obtener las bodegas existentes
    bodegas = Bodega.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()

            # Asignar la bodega seleccionada al producto
            producto.bodegas.add(form.cleaned_data['bodega'])

            # Crear el detalle de movimiento para agregar la cantidad de productos a la bodega
            DetalleMovimiento.objects.create(movimiento=None, producto=producto, cantidad=1)

            return redirect('gestion_bodegas')
    else:
        form = ProductoForm()

    return render(request, 'crear_producto.html', {'form': form, 'bodegas': bodegas})

@login_required
def gestion_bodegas(request):
    bodegas = Bodega.objects.all().prefetch_related('productos', 'productos__detallemovimiento_set')

    if request.method == 'POST':
        movimiento_form = MovimientoForm(request.POST)
        if movimiento_form.is_valid():
            movimiento = movimiento_form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            movimiento_form.save_m2m()
            return redirect('lista_movimientos')
    else:
        movimiento_form = MovimientoForm()

    detalles_movimiento = {}

    for bodega in bodegas:
        detalles_movimiento[bodega] = {}
        for producto in bodega.productos.all():
            detalles_movimiento[bodega][producto] = producto.detallemovimiento_set.filter(movimiento=None).first()

    return render(request, 'gestion_bodegas.html', {'bodegas': bodegas, 'detalles_movimiento': detalles_movimiento, 'movimiento_form': movimiento_form})

@login_required
def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_bodegas')
    else:
        form = BodegaForm()
    return render(request, 'crear_bodega.html', {'form': form})

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

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

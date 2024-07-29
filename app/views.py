from django.shortcuts import render, redirect, get_object_or_404
from app.models import Rol, Usuario, Ingrediente, Producto,PrecioProducto,PrecioIngrediente, Receta, RecetaIngrediente
from app.forms import RolForm, UsuarioForm, IngredienteForm, ProductoForm,PrecioProductoForm,PrecioIngredienteForm,RecetaForm, RecetaIngredienteFormSet
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
#from django.core.serializers.json import DjangoJSONEncoder
#import json
from django.forms import inlineformset_factory

#from django.db import transaction


# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("home")

@login_required
def signout(request):
    logout(request)
    return redirect("signin")

@login_required
@admin_required
def roles(request):
    roles = Rol.objects.all()
    contexto = {"roles": roles}
    return render(request, "rol/rol.html", contexto)

@login_required
@admin_required
def rol_crear(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("roles")
    else:
        form = RolForm()
    contexto = {"form": form}
    return render(request, "rol/rol_crear.html", contexto)

@login_required
@admin_required
def rol_modificar(request, rol_id):
    rol = get_object_or_404(Rol, id_rol=rol_id)
    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect("roles")
    else:
        form = RolForm(instance=rol)
    contexto = {"form": form}
    return render(request, "rol/rol_modificar.html", contexto)

@login_required
@admin_required
def usuarios(request):
    usuarios = Usuario.objects.all()
    contexto = {"usuarios": usuarios}
    return render(request, "usuario/usuario.html", contexto)

@login_required
@admin_required
def usuario_crear(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios")
    else:
        form = UsuarioForm()
    contexto = {"form": form}
    return render(request, "usuario/usuario_crear.html", contexto)

@login_required
@admin_required
def usuario_modificar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("usuarios")
    else:
        form = UsuarioForm(instance=usuario)
    contexto = {"form": form}
    return render(request, "usuario/usuario_modificar.html", contexto)

@login_required
@admin_required
def ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    contexto = {"ingredientes": ingredientes}
    return render(request, "ingrediente/ingrediente.html", contexto)

@login_required
@admin_required
def ingrediente_crear(request):
    if request.method == "POST":
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ingredientes")
    else:
        form = IngredienteForm()
    contexto = {"form": form}
    return render(request, "ingrediente/ingrediente_crear.html", contexto)

@login_required
@admin_required
def ingrediente_modificar(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id_ingrediente=ingrediente_id)
    if request.method == "POST":
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            return redirect("ingredientes")
    else:
        form = IngredienteForm(instance=ingrediente)
    contexto = {"form": form}
    return render(request, "ingrediente/ingrediente_modificar.html", contexto)

@login_required
@admin_required
def productos(request):
    productos = Producto.objects.all()
    contexto = {"productos": productos}
    return render(request, "producto/producto.html", contexto)

@login_required
@admin_required
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos")
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ProductoForm()

    contexto = {
        "form": form,
    }
    return render(request, "producto/producto_crear.html", contexto)

@login_required
@admin_required
def producto_modificar(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            form.save()
            return redirect("productos")
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ProductoForm(instance=producto)

    contexto = {
        "form": form,
    }
    return render(request, "producto/producto_modificar.html", contexto)

@login_required
@admin_required
def precio_productos(request):
    precios = PrecioProducto.objects.all()
    return render(request, 'precio_producto/precio_productos.html', {'precios': precios})

@login_required
@admin_required
def precio_producto_crear(request):
    if request.method == "POST":
        form = PrecioProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('precio_productos')  # Asegúrate de que este nombre es correcto
    else:
        form = PrecioProductoForm()
    contexto = {"form": form}
    return render(request, "precio_producto/precio_producto_crear.html", contexto)

@login_required
@admin_required
def precio_producto_modificar(request, precio_producto_id):
    precio_producto = get_object_or_404(PrecioProducto, id=precio_producto_id)
    if request.method == "POST":
        form = PrecioProductoForm(request.POST, instance=precio_producto)
        if form.is_valid():
            form.save()
            return redirect("precio_productos")
    else:
        form = PrecioProductoForm(instance=precio_producto)
    contexto = {"form": form}
    return render(request, "precio_producto/precio_producto_modificar.html", contexto)

@login_required
@admin_required
def precio_ingredientes(request):
    precios = PrecioIngrediente.objects.all()
    return render(request, 'precio_ingrediente/precio_ingredientes.html', {'precios': precios})

@login_required
@admin_required
def precio_ingrediente_crear(request):
    if request.method == 'POST':
        form = PrecioIngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('precio_ingredientes')
    else:
        form = PrecioIngredienteForm()
    return render(request, 'precio_ingrediente/precio_ingrediente_crear.html', {'form': form})

@login_required
@admin_required
def precio_ingrediente_modificar(request, precio_ingrediente_id):
    precio_ingrediente = get_object_or_404(PrecioIngrediente, id=precio_ingrediente_id)
    if request.method == 'POST':
        form = PrecioIngredienteForm(request.POST, instance=precio_ingrediente)
        if form.is_valid():
            form.save()
            return redirect('precio_ingredientes')
    else:
        form = PrecioIngredienteForm(instance=precio_ingrediente)
    return render(request, 'precio_ingrediente/precio_ingrediente_modificar.html', {'form': form, 'precio_ingrediente': precio_ingrediente})

@login_required
@admin_required
def recetas(request):
    recetas = Receta.objects.all()
    recetas_con_ingredientes = []

    for receta in recetas:
        ingredientes_info = []
        for ingrediente in receta.ingredientes.all():
            receta_ingrediente = receta.recetaingrediente_set.get(ingrediente=ingrediente)
            ingredientes_info.append({
                'nombre': ingrediente.nombre_ingrediente,
                'cantidad': receta_ingrediente.cantidad,
                'unidad': receta_ingrediente.unidad.nombre
            })
        recetas_con_ingredientes.append({
            'receta': receta,
            'ingredientes': ingredientes_info
        })

    contexto = {'recetas_con_ingredientes': recetas_con_ingredientes}
    return render(request, 'receta/recetas.html', contexto)


@login_required
@admin_required
def receta_crear(request):
    if request.method == "POST":
        receta_form = RecetaForm(request.POST)
        ingrediente_formset = RecetaIngredienteFormSet(request.POST, prefix='ingrediente')
        if receta_form.is_valid() and ingrediente_formset.is_valid():
            receta = receta_form.save()
            ingrediente_formset.instance = receta
            ingrediente_formset.save()
            return redirect('recetas')
        else:
            # Manejo de errores de validación
            print(receta_form.errors)
            print(ingrediente_formset.errors)
    else:
        receta_form = RecetaForm()
        ingrediente_formset = RecetaIngredienteFormSet(prefix='ingrediente')

    contexto = {
        'receta_form': receta_form,
        'ingrediente_formset': ingrediente_formset,
    }
    return render(request, 'receta/receta_crear.html', contexto)

@login_required
@admin_required
def receta_modificar(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == "POST":
        receta_form = RecetaForm(request.POST, instance=receta)
        ingrediente_formset = RecetaIngredienteFormSet(request.POST, instance=receta, prefix='ingrediente')
        if receta_form.is_valid() and ingrediente_formset.is_valid():
            receta = receta_form.save()
            ingrediente_formset.save()
            return redirect('recetas')
        else:
            # Manejo de errores
            print(receta_form.errors)
        
            print(ingrediente_formset.errors)
    else:
        receta_form = RecetaForm(instance=receta)
        ingrediente_formset = RecetaIngredienteFormSet(instance=receta, prefix='ingrediente')

    contexto = {
        'receta_form': receta_form,
        'ingrediente_formset': ingrediente_formset,
    }
    return render(request, 'receta/receta_modificar.html', contexto)


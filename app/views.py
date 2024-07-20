from django.shortcuts import render, redirect, get_object_or_404
from app.models import Rol, Usuario, Ingrediente, Producto, ProductoIngrediente
from app.forms import RolForm, UsuarioForm, IngredienteForm, ProductoForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.core.serializers.json import DjangoJSONEncoder
import json


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
        ingredientes_data = json.loads(request.POST.get('ingredientes', '[]'))

        if not ingredientes_data:
            form.add_error(None, "Debes agregar al menos un ingrediente.")
        
        if form.is_valid() and ingredientes_data:
            producto = form.save()
            
            ingrediente_cantidades = {}
            estado_producto = True 
            
            for ingrediente_data in ingredientes_data:
                ingrediente_id = ingrediente_data.get('id')
                cantidad = float(ingrediente_data.get('cantidad'))
                if ingrediente_id and cantidad:
                    if ingrediente_id in ingrediente_cantidades:
                        ingrediente_cantidades[ingrediente_id] += cantidad
                    else:
                        ingrediente_cantidades[ingrediente_id] = cantidad
                    
                    try:
                        ingrediente = Ingrediente.objects.get(id_ingrediente=ingrediente_id)
                        if not ingrediente.estado_ingrediente:
                            estado_producto = False
                    except Ingrediente.DoesNotExist:
                        continue
            
            for ingrediente_id, cantidad in ingrediente_cantidades.items():
                try:
                    ingrediente = Ingrediente.objects.get(id_ingrediente=ingrediente_id)
                    ProductoIngrediente.objects.create(
                        producto=producto,
                        ingrediente=ingrediente,
                        cantidad=cantidad
                    )
                except Ingrediente.DoesNotExist:
                    continue

            producto.estado_producto = estado_producto
            producto.save()
            
            return redirect("productos")
        else:
            print("Formulario no válido:", form.errors)
            ingredientes_input_value = json.dumps(ingredientes_data, cls=DjangoJSONEncoder)
    else:
        form = ProductoForm()
        ingredientes_input_value = '[]' 
    
    ingredientes = Ingrediente.objects.all()
    
    contexto = {
        "form": form,
        "ingredientes": ingredientes,
        "ingredientes_input_value": ingredientes_input_value
    }
    return render(request, "producto/producto_crear.html", contexto)

@login_required
@admin_required
def producto_modificar(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        ingredientes_data = json.loads(request.POST.get('ingredientes', '[]'))
        
        if not ingredientes_data:
            form.add_error(None, "Debes agregar al menos un ingrediente.")
        
        if form.is_valid() and ingredientes_data:
            producto = form.save()
            
            ingrediente_cantidades = {}
            estado_producto = True 
            
            for ingrediente_data in ingredientes_data:
                ingrediente_id = ingrediente_data.get('id')
                cantidad = float(ingrediente_data.get('cantidad'))
                if ingrediente_id and cantidad:
                    if ingrediente_id in ingrediente_cantidades:
                        ingrediente_cantidades[ingrediente_id] += cantidad
                    else:
                        ingrediente_cantidades[ingrediente_id] = cantidad
                    
                    try:
                        ingrediente = Ingrediente.objects.get(id_ingrediente=ingrediente_id)
                        if not ingrediente.estado_ingrediente:
                            estado_producto = False
                    except Ingrediente.DoesNotExist:
                        continue
            
            ProductoIngrediente.objects.filter(producto=producto).delete()
            
            for ingrediente_id, cantidad in ingrediente_cantidades.items():
                try:
                    ingrediente = Ingrediente.objects.get(id_ingrediente=ingrediente_id)
                    ProductoIngrediente.objects.create(
                        producto=producto,
                        ingrediente=ingrediente,
                        cantidad=cantidad
                    )
                except Ingrediente.DoesNotExist:
                    continue
            producto.estado_producto = estado_producto
            producto.save()
            
            return redirect("productos")
        else:
            print("Formulario no válido:", form.errors)
            ingredientes_input_value = json.dumps(ingredientes_data, cls=DjangoJSONEncoder)
    else:
        form = ProductoForm(instance=producto)
        producto_ingredientes = ProductoIngrediente.objects.filter(producto=producto)
        ingredientes_data = [
            {
                "id": pi.ingrediente.id_ingrediente,
                "cantidad": pi.cantidad
            }
            for pi in producto_ingredientes
        ]
        ingredientes_input_value = json.dumps(ingredientes_data, cls=DjangoJSONEncoder)
    
    ingredientes = Ingrediente.objects.all()
    
    contexto = {
        "form": form,
        "ingredientes": ingredientes,
        "ingredientes_input_value": ingredientes_input_value
    }
    return render(request, "producto/producto_modificar.html", contexto)

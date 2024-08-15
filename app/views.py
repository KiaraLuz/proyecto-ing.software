from django.shortcuts import render, redirect, get_object_or_404
from app.models import Rol, Usuario, Ingrediente, Producto, Receta, RecetaIngrediente, CostoProducto, CostoProductoIngrediente, Ganancia,Venta
from app.forms import RolForm, UsuarioForm, IngredienteForm, ProductoForm, RecetaForm, RecetaIngredienteFormSet, CostoProductoForm, RecetaIngredienteFormSetMod, GananciaForm, ModificarGananciaForm,VentaForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from decimal import Decimal
from datetime import datetime


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
            try:
                form.save()
                return redirect("ingredientes")
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Formulario no válido.")
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
            try:
                form.save()
                return redirect("ingredientes")
            except ValidationError as e:
                messages.error(request, str(e))                
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, "ingrediente/ingrediente_modificar.html", {"form": form})

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
        # Crear un formset con un formulario vacío inicial
        ingrediente_formset = RecetaIngredienteFormSet(prefix='ingrediente', queryset=RecetaIngrediente.objects.none())

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
        ingrediente_formset = RecetaIngredienteFormSetMod(request.POST, instance=receta)

        if receta_form.is_valid() and ingrediente_formset.is_valid():
            receta_form.save()
            ingrediente_formset.save()
            return redirect('recetas')
    else:
        receta_form = RecetaForm(instance=receta)
        ingrediente_formset = RecetaIngredienteFormSetMod(instance=receta)

    contexto = {
        'receta_form': receta_form,
        'ingrediente_formset': ingrediente_formset,
    }
    return render(request, 'receta/receta_modificar.html', contexto)

@login_required
@admin_required
def costos(request):
    costos = CostoProducto.objects.all()
    costos_con_ingredientes = []

    for costo in costos:
        ingredientes_info = []
        costo_ingredientes = costo.costoproductoingrediente_set.all()
        for costo_ingrediente in costo_ingredientes:
            ingredientes_info.append({
                'nombre': costo_ingrediente.ingrediente.nombre_ingrediente,
                'cantidad': costo_ingrediente.cantidad,
                'unidad': costo_ingrediente.unidad.nombre
            })
        costos_con_ingredientes.append({
            'costo': costo,
            'ingredientes': ingredientes_info
        })

    contexto = {'costos_con_ingredientes': costos_con_ingredientes}
    return render(request, 'costo/costos.html', contexto)

@login_required
@admin_required
def costo_crear(request):
    form = CostoProductoForm(request.POST or None)
    ingredientes = []

    if request.method == 'POST':
        if form.is_valid():
            try:
                costo_producto = form.save(commit=False)
                costo_producto.calcular_costo_total()
                costo_producto.save()
                
                producto = form.cleaned_data.get('producto')
                if producto:
                    receta = get_object_or_404(Receta, producto=producto)
                    ingredientes_receta = RecetaIngrediente.objects.filter(receta=receta).select_related('ingrediente', 'unidad')
                    
                    for ingrediente_receta in ingredientes_receta:
                        CostoProductoIngrediente.objects.create(
                            costo_producto=costo_producto,
                            ingrediente=ingrediente_receta.ingrediente,
                            cantidad=ingrediente_receta.cantidad,
                            precio_ingrediente=ingrediente_receta.ingrediente.precio_ingrediente,
                            costo_total=ingrediente_receta.cantidad * ingrediente_receta.ingrediente.precio_ingrediente,
                            unidad=ingrediente_receta.unidad
                        )
                    
                    ingredientes = ingredientes_receta
                return redirect('costos')
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'costo/costo_crear.html', {'form': form, 'ingredientes': ingredientes})
            
    return render(request, 'costo/costo_crear.html', {'form': form, 'ingredientes': ingredientes})

@login_required
@admin_required
def ganancia(request):
    ganancias = Ganancia.objects.all()
    contexto = {'ganancias': ganancias}
    return render(request, 'ganancia/ganancia.html', contexto)

@login_required
@admin_required
def ganancia_crear(request):
    if request.method == 'POST':
        form = GananciaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            margen_ganancia = form.cleaned_data['margen_ganancia']

            precio_con_ganancia = producto.costo_total + (producto.costo_total * margen_ganancia / 100)

            Ganancia.objects.create(
                nombre_producto=producto.producto.nombre_producto,
                costo_producto=producto.costo_total,
                precio_con_ganancia=precio_con_ganancia
            )

            messages.success(request, "Ganancia creada exitosamente.")
            return redirect('ganancias') 

    else:
        form = GananciaForm()

    return render(request, 'ganancia/ganancia_crear.html', {'form': form})

@login_required
@admin_required
def ganancia_modificar(request, ganancia_id):
    ganancia = get_object_or_404(Ganancia, id_ganancia=ganancia_id)

    if request.method == 'POST':
        form = ModificarGananciaForm(request.POST)
        if form.is_valid():
            margen_ganancia = Decimal(form.cleaned_data['margen_ganancia'])

            # Obtener el costo total desde CostoProducto relacionado al producto
            costo_total = CostoProducto.objects.get(producto__nombre_producto=ganancia.nombre_producto).costo_total
            
            # Calcular el nuevo precio con el margen de ganancia
            precio_con_ganancia = costo_total + (costo_total * margen_ganancia / 100)
            
            # Actualizar el precio con ganancia sin guardar el margen
            ganancia.precio_con_ganancia = precio_con_ganancia
            ganancia.save()

            messages.success(request, "El precio de ganancia ha sido actualizado exitosamente.")
            return redirect('ganancias')  # Redirige a la vista de ganancia
    else:
        form = ModificarGananciaForm()

    return render(request, 'ganancia/ganancia_modificar.html', {'form': form, 'ganancia': ganancia})

@login_required
@admin_required
def venta_listar(request):
    ventas = Venta.objects.all()
    return render(request, 'venta/venta_listar.html', {'ventas': ventas})

@login_required
@admin_required
def venta_crear(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('venta_listar')  # Redirige a la vista que lista las ventas
    else:
        form = VentaForm()
        fecha_actual = datetime.now().strftime('%Y-%m-%d') 
    return render(request, 'venta/venta_crear.html',  {'form': form, 'fecha_actual': fecha_actual})

def obtener_precio(request):
    nombre_producto = request.GET.get('nombre_producto')
    try:
        ganancia = Ganancia.objects.get(nombre_producto=nombre_producto)
        precio = ganancia.precio_con_ganancia
    except Ganancia.DoesNotExist:
        precio = 0
    return JsonResponse({'precio': precio})

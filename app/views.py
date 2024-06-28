from django.shortcuts import render, redirect, get_object_or_404
from app.models import Rol, Usuario, Ingrediente
from app.forms import RolForm, UsuarioForm, IngredienteForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def roles(request):
    roles = Rol.objects.all()
    contexto = {'roles': roles}
    return render(request, "rol/rol.html", contexto)

@login_required
def rol_crear(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('roles')
    else:
        form = RolForm()
    contexto = {'form': form}
    return render(request, "rol/rol_crear.html", contexto)

@login_required
def rol_modificar(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)
    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save(commit=True)
            return redirect('roles')
    else:
        form = RolForm(instance=rol)
    contexto = {'form': form}
    return render(request, "rol/rol_modificar.html", contexto)

@login_required
def usuarios(request):
    usuarios = Usuario.objects.all()
    contexto = {'usuarios': usuarios}
    return render(request, "usuario/usuario.html", contexto)

@login_required
def usuario_crear(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    contexto = {'form': form}
    return render(request, "usuario/usuario_crear.html", contexto)

@login_required
def usuario_modificar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save(commit=True)
            return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    contexto = {'form': form}
    return render(request, "usuario/usuario_modificar.html", contexto)

@login_required
def ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    contexto = {'ingredientes': ingredientes}
    return render(request, "ingrediente/ingrediente.html", contexto)

@login_required
def ingrediente_crear(request):
    if request.method == "POST":
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('ingredientes')
    else:
        form = IngredienteForm()
    contexto = {'form': form}
    return render(request, "ingrediente/ingrediente_crear.html", contexto)

@login_required
def ingrediente_modificar(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id_ingrediente=ingrediente_id)
    if request.method == "POST":
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save(commit=True)
            return redirect('ingredientes')
    else:
        form = IngredienteForm(instance=ingrediente)
    contexto = {'form': form}
    return render(request, "ingrediente/ingrediente_modificar.html", contexto)

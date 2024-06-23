from django.shortcuts import render, redirect
from app.models import Rol
from app.forms import RolForm
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
    rol = Rol.objects.get(id=rol_id)
    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save(commit=True)
            return redirect('roles')
    else:
        form = RolForm(instance=rol)
    contexto = {'form': form}
    return render(request, "rol/rol_modificar.html", contexto)
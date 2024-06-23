from django.shortcuts import render, redirect
from app.models import Rol
from app.forms import RolForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def roles(request):
    roles = Rol.objects.all()
    contexto = {'roles': roles}
    return render(request, "rol.html", contexto)

def rol_crear(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('roles')
    else:
        form = RolForm()
    contexto = {'form': form}
    return render(request, "rol_crear.html", contexto)

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
    return render(request, "rol_modificar.html", contexto)
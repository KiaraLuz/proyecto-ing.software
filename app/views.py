from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def roles(request):
    return render(request, "rol.html")
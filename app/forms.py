from django import forms
from .models import Rol, Usuario

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = "__all__"

    id = forms.CharField(
        label="ID", widget=forms.TextInput(attrs={"class": "input"})
    )
    nombre_rol = forms.CharField(
        label="Nombre del Rol", widget=forms.TextInput(attrs={"class": "input"})
    )
    descripcion = forms.CharField(
        label="Descripción", widget=forms.Textarea(attrs={"class": "input"})
    )
    estado = forms.BooleanField(
        label="Estado", required=False, widget=forms.CheckboxInput(attrs={"class": "checkbox"})
    )

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['id'].disabled = True

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"

    id_usuario = forms.CharField(
        label="ID", widget=forms.TextInput(attrs={"class": "input"})
    )
    nombre_usuario = forms.CharField(
        label="Nombre", widget=forms.TextInput(attrs={"class": "input"})
    )
    rol_usuario = forms.ModelChoiceField(
        label="Rol",
        queryset=Rol.objects.all(),
        widget=forms.Select(attrs={"class": "select"}),
    )
    contraseña_usuario = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "input"}),  
    )

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['id_usuario'].disabled = True

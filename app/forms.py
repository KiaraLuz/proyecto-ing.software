from django import forms
from .models import Rol, Usuario,Ingrediente

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
    is_admin = forms.BooleanField(
        label="Nivel Administrador", required=False, widget=forms.CheckboxInput(attrs={"class": "checkbox"})
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
    confirmar_contraseña = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "input"})
    )
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['id_usuario'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        contraseña_usuario = cleaned_data.get("contraseña_usuario")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if contraseña_usuario and confirmar_contraseña and contraseña_usuario != confirmar_contraseña:
            self.add_error('confirmar_contraseña', "Las contraseñas no coinciden.")

        return cleaned_data
    
class IngredienteForm(forms.ModelForm):
    id_ingrediente = forms.CharField(label="ID", widget=forms.TextInput(attrs={"class": "input"}))
    nombre_ingrediente = forms.CharField(label="Nombre del Ingrediente", widget=forms.TextInput(attrs={"class": "input"}))
    cantidad = forms.DecimalField(label="Cantidad", widget=forms.NumberInput(attrs={"class": "input"}))
    unidad = forms.ChoiceField(label="Unidad", choices=[('KG', 'KG'), ('UNID', 'UNID')], widget=forms.Select(attrs={"class": "input"}))
    estado_ingrediente = forms.CharField(label="Estado del Ingrediente", widget=forms.TextInput(attrs={"class": "input"}))

    class Meta:
        model = Ingrediente
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(IngredienteForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['id_ingrediente'].disabled = True

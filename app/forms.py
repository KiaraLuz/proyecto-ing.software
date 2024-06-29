from django import forms
from .models import Rol, Usuario, Ingrediente


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        exclude = ["id_rol"]  # Excluimos id_rol del formulario

    nombre_rol = forms.CharField(
        label="Nombre", widget=forms.TextInput(attrs={"class": "input"})
    )
    descripcion = forms.CharField(
        label="Descripción", widget=forms.Textarea(attrs={"class": "input"})
    )
    estado = forms.BooleanField(
        label="Estado",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )
    is_admin = forms.BooleanField(
        label="Nivel Administrador",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        nombre_rol = cleaned_data.get("nombre_rol")
        descripcion = cleaned_data.get("descripcion")

        if not nombre_rol and not descripcion:
            raise forms.ValidationError("Datos incompletos")
        return cleaned_data


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
        widget=forms.PasswordInput(attrs={"class": "input"}),
    )

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["id_usuario"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        contraseña_usuario = cleaned_data.get("contraseña_usuario")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if (
            contraseña_usuario
            and confirmar_contraseña
            and contraseña_usuario != confirmar_contraseña
        ):
            self.add_error("confirmar_contraseña", "Las contraseñas no coinciden.")

        return cleaned_data


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = "__all__"

    id_ingrediente = forms.CharField(
        label="ID del Ingrediente", widget=forms.TextInput(attrs={"class": "input"})
    )
    nombre_ingrediente = forms.CharField(
        label="Nombre del Ingrediente", widget=forms.TextInput(attrs={"class": "input"})
    )
    cantidad = forms.DecimalField(
        label="Cantidad", widget=forms.NumberInput(attrs={"class": "input"})
    )
    unidad = forms.ChoiceField(
        label="Unidad",
        choices=[("KG", "KG"), ("UNID", "UNID")],
        widget=forms.Select(attrs={"class": "input"}),
    )
    estado_ingrediente = forms.BooleanField(
        label="Estado del Ingrediente",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )

    def __init__(self, *args, **kwargs):
        super(IngredienteForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["id_ingrediente"].disabled = True

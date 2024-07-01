from django import forms
from .models import Rol, Usuario, Ingrediente
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        exclude = ["id_rol"]

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


class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ("username", "email", "password1", "password2", "rol")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol"].required = False


class UsuarioForm(UserChangeForm):
    password = forms.CharField(
        label="Password", required=False, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label="Confirm Password", required=False, widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = (
            "username",
            "password",
            "password_confirm",
            "rol",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Las contraseñas no coinciden. Por favor, inténtelo de nuevo."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
            if commit:
                user.save()
        return user


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        exclude = ["id_ingrediente"]

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

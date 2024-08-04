from django import forms
from django.forms import inlineformset_factory
from .models import Rol, Usuario, Ingrediente, UnidadesMedida, Producto, RecetaIngrediente,Receta, CostoProducto
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
    class Meta:
        model = Usuario
        fields = ("username", "password1", "password2", "rol")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True
        self.fields["rol"].required = True

    def clean_rol(self):
        rol = self.cleaned_data.get("rol")
        if not rol:
            raise forms.ValidationError("Este campo es obligatorio.")
        return rol

class UsuarioChangeForm(UserChangeForm):
    password = forms.CharField(
        label="Contraseña", required=False, widget=forms.PasswordInput
    )
    confirmar_password = forms.CharField(
        label="Confirmar contraseña", required=False, widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = (
            "username",
            "password",
            "confirmar_password",
            "rol",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password and confirmar_password:
            if password != confirmar_password:
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
    unidad = forms.ModelChoiceField(
        label="Unidad",
        queryset=UnidadesMedida.objects.all(),
        widget=forms.Select(attrs={"class": "input"}),
        to_field_name="nombre"
    )
    estado_ingrediente = forms.BooleanField(
        label="Estado del Ingrediente",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )
    precio_ingrediente = forms.DecimalField(
        label="Precio", widget=forms.NumberInput(attrs={"class": "input"})
    )

    def __init__(self, *args, **kwargs):
        super(IngredienteForm, self).__init__(*args, **kwargs)

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ["id_producto"]
        
    nombre_producto = forms.CharField(
        label="Nombre del Producto", widget=forms.TextInput(attrs={"class": "input"})
    )
    descripcion = forms.CharField(
        label="Decripcion", widget=forms.TextInput(attrs={"class": "input"})
    )
    precio_producto = forms.DecimalField(
        label="Precio", widget=forms.NumberInput(attrs={"class": "input"})
    )

class RecetaIngredienteForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente', 'cantidad', 'unidad']
        widgets = {
            'ingrediente': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
        }

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['producto']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
        }

# Para la vista de creación, puedes mantener los formularios adicionales vacíos si es necesario
RecetaIngredienteFormSet = inlineformset_factory(
    Receta,
    RecetaIngrediente,
    form=RecetaIngredienteForm,
    fields=['ingrediente', 'cantidad', 'unidad'],
    can_delete=True,
    extra=1  # O el número de formularios vacíos que desees mostrar inicialmente
)

# Para la vista de modificación, asegúrate de que no se generen formularios vacíos adicionales
RecetaIngredienteFormSetMod = inlineformset_factory(
    Receta,
    RecetaIngrediente,
    form=RecetaIngredienteForm,
    fields=['ingrediente', 'cantidad', 'unidad'],
    can_delete=True,
    extra=0
)

class CostoProductoForm(forms.ModelForm):
    class Meta:
        model = CostoProducto
        fields = ['producto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(receta__isnull=False).distinct()
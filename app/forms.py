from django import forms
from django.forms import inlineformset_factory
from .models import Rol, Usuario, Ingrediente, UnidadesMedida, Producto, RecetaIngrediente,Receta, CostoProducto, Ganancia,Venta, Cliente
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone

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
        label="Descripción", widget=forms.TextInput(attrs={"class": "input"})
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        productos_con_receta = Receta.objects.values_list('producto', flat=True)
        self.fields['producto'].queryset = Producto.objects.exclude(id_producto__in=productos_con_receta)

RecetaIngredienteFormSet = inlineformset_factory(
    Receta,
    RecetaIngrediente,
    form=RecetaIngredienteForm,
    fields=['ingrediente', 'cantidad', 'unidad'],
    can_delete=True,
    extra=1
)

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
        productos_con_costo = CostoProducto.objects.values_list('producto', flat=True)
        self.fields['producto'].queryset = Producto.objects.exclude(id_producto__in=productos_con_costo)

class GananciaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=CostoProducto.objects.all(), label="Producto")
    margen_ganancia = forms.DecimalField(max_digits=5, decimal_places=2, label="Margen de Ganancia (%)")

class ModificarGananciaForm(forms.ModelForm):
    class Meta:
        model = Ganancia
        fields = ['margen_ganancia']

    margen_ganancia = forms.DecimalField(max_digits=5, decimal_places=2, label="Margen de Ganancia (%)")

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()

    def save(self, commit=True):
        venta = super().save(commit=False)
        if commit:
            venta.save()
        return venta

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'correo_cliente', 'telefono_cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['correo_cliente'].required = False
        self.fields['telefono_cliente'].required = False
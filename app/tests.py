from django.test import TestCase
from django.urls import reverse
from .models import Rol
from .forms import RolForm
from .models import Ingrediente
from .forms import IngredienteForm

class RolFormTestCase(TestCase):
    def setUp(self):
        self.rol1 = Rol.objects.create(
            nombre_rol="Admin",
            descripcion="Administrador",
            estado=True,
            is_admin=True,
        )

    def test_crear_rol_form(self):
        form_data = {
            "nombre_rol": "User",
            "descripcion": "Usuario",
            "estado": True,
            "is_admin": False,
        }
        form = RolForm(data=form_data)
        self.assertTrue(form.is_valid())
        rol = form.save()
        self.assertEqual(rol.nombre_rol, "User")
        self.assertEqual(rol.descripcion, "Usuario")
        self.assertEqual(rol.estado, True)
        self.assertEqual(rol.is_admin, False)

    def test_modificar_rol_form(self):
        form_data = {
            "nombre_rol": "SuperAdmin",
            "descripcion": "Super Administrador",
            "estado": True,
            "is_admin": True,
        }
        rol = Rol.objects.get(nombre_rol="Admin")
        form = RolForm(data=form_data, instance=rol)
        self.assertTrue(form.is_valid())
        rol_modificado = form.save()
        self.assertEqual(rol_modificado.nombre_rol, "SuperAdmin")
        self.assertEqual(rol_modificado.descripcion, "Super Administrador")
        self.assertEqual(rol_modificado.estado, True)
        self.assertEqual(rol_modificado.is_admin, True)

    def test_form_validations(self):
        form_data = {
            "nombre_rol": "",
            "descripcion": "",
            "estado": True,
            "is_admin": False,
        }
        form = RolForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nombre_rol", form.errors)
        self.assertIn("descripcion", form.errors)
        self.assertEqual(
            form.errors["__all__"][0],
            "Datos incompletos",
        )

class IngredienteFormTestCase(TestCase):
    def setUp(self):
        self.ingrediente1 = Ingrediente.objects.create(
            nombre_ingrediente="Tomate",
            cantidad=2.0,
            unidad="UNID",
            estado_ingrediente=True,
        )

    def test_crear_ingrediente_form(self):
        form_data = {
            "nombre_ingrediente": "Lechuga",
            "cantidad": 1.0,
            "unidad": "UNID",
            "estado_ingrediente": True,
        }
        form = IngredienteForm(data=form_data)
        self.assertTrue(form.is_valid())
        ingrediente = form.save()
        self.assertEqual(ingrediente.nombre_ingrediente, "Lechuga")
        self.assertEqual(ingrediente.cantidad, 1.0)
        self.assertEqual(ingrediente.unidad, "UNID")
        self.assertEqual(ingrediente.estado_ingrediente, True)

    def test_modificar_ingrediente_form(self):
        form_data = {
            "nombre_ingrediente": "Tomate Cherry",
            "cantidad": 3.0,
            "unidad": "UNID",
            "estado_ingrediente": True,
        }
        ingrediente = Ingrediente.objects.get(nombre_ingrediente="Tomate")
        form = IngredienteForm(data=form_data, instance=ingrediente)
        self.assertTrue(form.is_valid())
        ingrediente_modificado = form.save()
        self.assertEqual(ingrediente_modificado.nombre_ingrediente, "Tomate Cherry")
        self.assertEqual(ingrediente_modificado.cantidad, 3.0)
        self.assertEqual(ingrediente_modificado.unidad, "UNID")
        self.assertEqual(ingrediente_modificado.estado_ingrediente, True)

    def test_form_validations(self):
        form_data = {
            "nombre_ingrediente": "",
            "cantidad": "",
            "unidad": "",
            "estado_ingrediente": True,
        }
        form = IngredienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nombre_ingrediente", form.errors)
        self.assertIn("cantidad", form.errors)
        self.assertIn("unidad", form.errors)

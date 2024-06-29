from django.test import TestCase
from django.urls import reverse
from .models import Rol
from .forms import RolForm


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

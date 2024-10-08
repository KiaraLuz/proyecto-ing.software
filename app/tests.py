from django.test import TestCase
from django.urls import reverse
from .models import Rol, Usuario, Ingrediente
from .forms import RolForm, UsuarioForm, UsuarioChangeForm, IngredienteForm

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
            "nombre_rol": "Vendedor",
            "descripcion": "Es un rol para vendedores",
            "estado": True,
            "is_admin": False,
        }
        form = RolForm(data=form_data)
        self.assertTrue(form.is_valid())
        rol = form.save()
        self.assertEqual(rol.nombre_rol, "Vendedor")
        self.assertEqual(rol.descripcion, "Es un rol para vendedores")
        self.assertEqual(rol.estado, True)
        self.assertEqual(rol.is_admin, False)

    def test_modificar_rol_form(self):
        form_data = {
            "nombre_rol": "Almacén",
            "descripcion": "Es un rol para almacén",
            "estado": True,
            "is_admin": True,
        }
        rol = Rol.objects.get(nombre_rol="Admin")
        form = RolForm(data=form_data, instance=rol)
        self.assertTrue(form.is_valid())
        rol_modificado = form.save()
        self.assertEqual(rol_modificado.nombre_rol, "Almacén")
        self.assertEqual(rol_modificado.descripcion, "Es un rol para almacén")
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

class AuthFormTestCase(TestCase):
    def setUp(self):
        self.rol = Rol.objects.create(
            nombre_rol="Admin",
            descripcion="Administrador",
            estado=True,
            is_admin=True
        )
        self.user = Usuario.objects.create_user(
            username='User_Test',
            password='Password_Test',
            rol=self.rol
        )
        self.login_url = reverse('signin')
        self.home_url = reverse('home')
        self.logout_url = reverse('signout')

    def test_login_page_renders(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'User_Test',
            'password': 'Password_Test',
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'User_Test',
            'password': 'Password_Fail',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'Username or password is incorrect')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username='User_Test', password='Password_Test')
        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class UsuarioFormTestCase(TestCase):
    def setUp(self):
        self.rol_admin = Rol.objects.create(
            nombre_rol="Admin",
            descripcion="Administrador",
            estado=True,
            is_admin=True
        )
        self.rol_usuario = Rol.objects.create(
            nombre_rol="Usuario",
            descripcion="Usuario regular",
            estado=True,
            is_admin=False
        )

    def test_crear_usuario_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "rol": self.rol_usuario.id_rol,
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data.get("password1"))
        usuario.save()
        self.assertEqual(usuario.username, "testuser")
        self.assertTrue(usuario.check_password("testpassword"))
        self.assertEqual(usuario.rol, self.rol_usuario)

    def test_modificar_usuario_form(self):
        usuario = Usuario.objects.create(
            username="testuser",
            rol=self.rol_usuario,
        )
        usuario.set_password("oldpassword")
        usuario.save()

        form_data = {
            "username": "updateduser",
            "password": "newpassword",
            "confirmar_password": "newpassword",
            "rol": self.rol_admin.id_rol,
        }
        form = UsuarioChangeForm(data=form_data, instance=usuario)
        self.assertTrue(form.is_valid())
        usuario_modificado = form.save()
        self.assertEqual(usuario_modificado.username, "updateduser")
        self.assertTrue(usuario_modificado.check_password("newpassword"))
        self.assertEqual(usuario_modificado.rol, self.rol_admin)

    def test_usuario_form_validations(self):
        form_data = {
            "username": "",
            "password1": "",
            "password2": "",
            "rol": None,
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)
        self.assertIn("rol", form.errors)

        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "mismatchpassword",
            "rol": self.rol_usuario.id_rol,
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

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
import re

from django import forms

from app.modelo.curso import Curso, Leccion, Modulo
from app.models import Valoracion
from app.modelo.usuario import Usuario


class CambiarContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(label="Contraseña actual", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}))
    nueva_contrasena = forms.CharField(label="Nueva contraseña", min_length=8, strip=False, widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}))
    confirmar_contrasena = forms.CharField(label="Confirmar nueva contraseña", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}))

    def __init__(self, usuario, *args, **kwargs):
        self.usuario = usuario
        super().__init__(*args, **kwargs)

    def clean_contrasena_actual(self):
        password = self.cleaned_data["contrasena_actual"]
        if not self.usuario.check_password(password):
            raise forms.ValidationError("La contraseña actual no es correcta.")
        return password

    def clean(self):
        datos = super().clean()
        nueva = datos.get("nueva_contrasena")
        confirmar = datos.get("confirmar_contrasena")
        if nueva and confirmar and nueva != confirmar:
            self.add_error("confirmar_contrasena", "Las contraseñas nuevas no coinciden.")
        return datos


class PerfilUsuarioForm(forms.ModelForm):
    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        if not re.fullmatch(r"\d{9}", telefono):
            raise forms.ValidationError("El teléfono debe tener 9 dígitos.")
        return telefono

    class Meta:
        model = Usuario
        fields = ["nombres", "apellidos", "email", "telefono"]
        widgets = {
            "nombres": forms.TextInput(attrs={"class": "form-control", "autocomplete": "given-name"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control", "autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "inputmode": "numeric"}),
        }


class CursoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"

    class Meta:
        model = Curso
        fields = ["nombre", "descripcion", "categoria", "nivel", "duracion_horas", "url_imagen", "objetivos", "requisitos", "instructor", "ofrece_certificado", "publicado"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3}), "objetivos": forms.Textarea(attrs={"rows": 3}), "requisitos": forms.Textarea(attrs={"rows": 2})}


class ModuloForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Modulo
        fields = ["titulo", "descripcion", "orden"]


class LeccionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Leccion
        fields = ["titulo", "contenido", "url_video", "duracion_minutos", "orden"]
        widgets = {"contenido": forms.Textarea(attrs={"rows": 3})}


class ValoracionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    puntuacion = forms.ChoiceField(choices=[(n, f"{n} estrellas") for n in range(5, 0, -1)])

    class Meta:
        model = Valoracion
        fields = ["puntuacion", "comentario"]
        widgets = {"comentario": forms.Textarea(attrs={"rows": 3, "maxlength": 1000})}


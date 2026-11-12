from django import forms

from app.modelo.curso import Curso, Leccion, Modulo
from app.models import Valoracion


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


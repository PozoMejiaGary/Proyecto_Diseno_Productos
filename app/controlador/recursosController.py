from django.shortcuts import render

def seccion_recursos(request):
    recursos_disponibles = [
        {
            'tipo': 'PDF',
            'categoria': 'Guías',
            'titulo': 'Guía para tu primera entrevista',
            'detalle': 'Guía · 8 min de lectura',
        },
        {
            'tipo': 'Plantilla',
            'categoria': 'Plantillas',
            'titulo': 'Plantilla de CV editable',
            'detalle': 'Plantilla · Editable',
        },
        {
            'tipo': 'Video',
            'categoria': 'Videos',
            'titulo': 'Cómo preparar tu presentación',
            'detalle': 'Video · 12 min',
        },
        {
            'tipo': 'Artículo',
            'categoria': 'Artículos',
            'titulo': 'Hábitos para organizar tu dinero',
            'detalle': 'Artículo · 5 min de lectura',
        },
        {
            'tipo': 'PDF',
            'categoria': 'Guías',
            'titulo': 'Checklist del primer día de trabajo',
            'detalle': 'Guía · 4 min de lectura',
        },
        {
            'tipo': 'Artículo',
            'categoria': 'Artículos',
            'titulo': 'Habilidades que buscan las empresas',
            'detalle': 'Artículo · 7 min de lectura',
        },
        {
            'tipo': 'Plantilla',
            'categoria': 'Plantillas',
            'titulo': 'Plantilla de presupuesto mensual',
            'detalle': 'Plantilla · Excel / Sheets',
        },
        {
            'tipo': 'Video',
            'categoria': 'Videos',
            'titulo': 'Estrategias de negociación salarial',
            'detalle': 'Video · 15 min',
        },
    ]
    return render(request, 'recursos.html', {'recursos': recursos_disponibles}) 
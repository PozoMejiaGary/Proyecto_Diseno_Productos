from django.http import Http404, HttpResponse
from django.shortcuts import render


RECURSOS = [
    {
        "slug": "primera-entrevista", "tipo": "Guía", "categoria": "Guías",
        "titulo": "Guía para tu primera entrevista", "detalle": "Guía práctica · 8 min",
        "resumen": "Prepárate antes, durante y después de una entrevista laboral.",
        "contenido": "Antes de la entrevista:\n- Investiga la empresa y el puesto.\n- Prepara tres ejemplos de logros usando situación, acción y resultado.\n- Revisa tu CV y prepara preguntas para el equipo.\n\nDurante la entrevista:\n- Escucha la pregunta completa y responde con ejemplos concretos.\n- Explica qué aprendiste de tus retos.\n- Pregunta cuáles serían las prioridades de los primeros meses.\n\nDespués:\n- Anota lo que salió bien y lo que mejorarías.\n- Envía un mensaje breve de agradecimiento.",
        "destacado": True,
    },
    {
        "slug": "plantilla-cv", "tipo": "Plantilla", "categoria": "Plantillas",
        "titulo": "Plantilla de CV editable", "detalle": "Estructura lista para completar",
        "resumen": "Organiza tu experiencia en una página clara, con logros medibles.",
        "contenido": "NOMBRE Y APELLIDO\nCiudad · correo · teléfono · enlace profesional\n\nPERFIL\nResume en 3 líneas tu experiencia, especialidad y el valor que aportas.\n\nEXPERIENCIA\nPuesto — Empresa | Mes/Año a Mes/Año\n- Acción realizada + herramienta utilizada + resultado medible.\n- Prioriza logros relevantes para el puesto al que postulas.\n\nFORMACIÓN\nTítulo o curso — Institución | Año\n\nHABILIDADES\nIncluye herramientas y habilidades relacionadas con la vacante.",
    },
    {
        "slug": "presentacion-profesional", "tipo": "Guía", "categoria": "Guías",
        "titulo": "Prepara tu presentación profesional", "detalle": "Ejercicio práctico · 12 min",
        "resumen": "Un guion breve para explicar quién eres y qué sabes hacer.",
        "contenido": "Usa esta estructura de 30 a 60 segundos:\n1. Quién eres: tu especialidad o área de interés.\n2. Qué haces: una experiencia, proyecto o habilidad relevante.\n3. Qué buscas: el reto profesional que quieres asumir.\n\nEjemplo:\nSoy analista junior con experiencia académica en organización de datos. En mi último proyecto automaticé un reporte semanal y reduje el tiempo de preparación. Busco integrarme a un equipo donde pueda aplicar análisis y seguir aprendiendo.\n\nPractica en voz alta, adapta el ejemplo a cada oportunidad y evita memorizar palabra por palabra.",
    },
    {
        "slug": "presupuesto-mensual", "tipo": "Plantilla", "categoria": "Plantillas",
        "titulo": "Plantilla de presupuesto mensual", "detalle": "Formato para copiar a Excel o Sheets",
        "resumen": "Ordena ingresos, gastos y metas de ahorro en una tabla sencilla.",
        "contenido": "CONCEPTO | PLANIFICADO | REAL\nIngresos netos | |\nVivienda y servicios | |\nAlimentación | |\nTransporte | |\nSalud y educación | |\nDeudas | |\nAhorro | |\nOtros gastos | |\n\nCálculo: saldo del mes = ingresos netos - suma de gastos.\nRegistra los movimientos semanalmente y ajusta el siguiente mes según tus gastos reales.",
    },
    {
        "slug": "primer-dia", "tipo": "Checklist", "categoria": "Guías",
        "titulo": "Checklist para tu primer día de trabajo", "detalle": "Lista de preparación · 4 min",
        "resumen": "Llega con lo necesario y comienza con claridad.",
        "contenido": "ANTES\n[ ] Confirma horario, ubicación y persona de contacto.\n[ ] Revisa la ruta y prepara documentos solicitados.\n[ ] Deja lista la ropa y configura una alarma.\n\nAL LLEGAR\n[ ] Preséntate con el equipo y ubica los espacios principales.\n[ ] Confirma tus prioridades y canales de comunicación.\n[ ] Anota nombres, procesos y accesos que debas recordar.\n\nAL CERRAR EL DÍA\n[ ] Resume lo aprendido y define tus dudas para el día siguiente.",
    },
    {
        "slug": "habilidades-demandadas", "tipo": "Artículo", "categoria": "Artículos",
        "titulo": "Habilidades que buscan los equipos", "detalle": "Artículo · 7 min de lectura",
        "resumen": "Cómo demostrar colaboración, comunicación y pensamiento crítico.",
        "contenido": "Las habilidades se vuelven visibles cuando las conectas con una situación real. Para cada habilidad, prepara un ejemplo breve:\n\nColaboración: explica cómo coordinaste tareas y resolviste desacuerdos.\nComunicación: muestra cómo adaptaste una explicación a distintas personas.\nPensamiento crítico: describe qué datos revisaste antes de decidir.\nAdaptabilidad: cuenta cómo respondiste a un cambio de prioridad.\n\nEn una entrevista, explica el contexto, las acciones que tomaste y el resultado. Si estás empezando, usa proyectos académicos, voluntariado o responsabilidades personales.",
    },
    {
        "slug": "negociacion-salarial", "tipo": "Guía", "categoria": "Guías",
        "titulo": "Conversaciones sobre compensación", "detalle": "Guía de preparación · 6 min",
        "resumen": "Prepara una conversación informada y profesional sobre compensación.",
        "contenido": "1. Investiga rangos para el puesto, experiencia y ubicación.\n2. Define un rango objetivo y tu mínimo antes de conversar.\n3. Explica el valor que aportarás con ejemplos concretos.\n4. Considera el paquete completo: beneficios, modalidad, horario y desarrollo.\n5. Pide tiempo para revisar una propuesta si lo necesitas.\n\nFrase para iniciar: “Gracias por la propuesta. Por las responsabilidades del puesto y mi experiencia en ____, esperaba conversar sobre un rango de ____ a ____. ¿Hay flexibilidad?”\n\nMantén un tono claro y respetuoso; confirma cualquier acuerdo por escrito.",
    },
    {
        "slug": "organizacion-financiera", "tipo": "Artículo", "categoria": "Artículos",
        "titulo": "Hábitos para organizar tu dinero", "detalle": "Artículo · 5 min de lectura",
        "resumen": "Un método simple para revisar gastos y construir una meta de ahorro.",
        "contenido": "Empieza registrando durante un mes tus ingresos y gastos. Agrupa los gastos por categorías y distingue los fijos de los variables.\n\nElige una meta concreta, como crear un fondo para una compra o cubrir un gasto futuro. Programa una transferencia de ahorro después de recibir tus ingresos y revisa el presupuesto cada semana.\n\nSi tus gastos superan tus ingresos, prioriza necesidades, revisa suscripciones y busca apoyo financiero confiable antes de asumir nueva deuda.",
    },
]


def seccion_recursos(request):
    consulta = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    recursos = RECURSOS
    if consulta:
        termino = consulta.casefold()
        recursos = [r for r in recursos if termino in " ".join((r["titulo"], r["categoria"], r["resumen"], r["contenido"])).casefold()]
    if categoria:
        recursos = [r for r in recursos if r["categoria"] == categoria]
    recurso_destacado = next((r for r in RECURSOS if r.get("destacado")), None)
    categorias = sorted({r["categoria"] for r in RECURSOS})
    return render(request, "recursos.html", {
        "recursos": recursos, "consulta": consulta, "categoria_actual": categoria,
        "categorias": categorias, "recurso_destacado": recurso_destacado,
    })


def detalle_recurso(request, slug):
    recurso = next((r for r in RECURSOS if r["slug"] == slug), None)
    if recurso is None:
        raise Http404("No se encontró el recurso")
    return render(request, "detalle_recurso.html", {"recurso": recurso})


def descargar_recurso(request, slug):
    recurso = next((r for r in RECURSOS if r["slug"] == slug), None)
    if recurso is None:
        raise Http404("No se encontró el recurso")
    contenido = f"{recurso['titulo']}\n{recurso['resumen']}\n\n{recurso['contenido']}\n"
    respuesta = HttpResponse(contenido, content_type="text/plain; charset=utf-8")
    respuesta["Content-Disposition"] = f'attachment; filename="{slug}.txt"'
    return respuesta

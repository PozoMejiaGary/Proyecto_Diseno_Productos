from io import BytesIO

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

AZUL = (0.106, 0.176, 0.420)
AMARILLO = (0.961, 0.773, 0.094)
GRIS = (0.420, 0.478, 0.600)


def _texto_centrado(pdf, x, y, texto, fuente, tamano, ancho_max):
    """Dibuja el texto centrado y lo achica si no cabe en el ancho disponible."""
    while tamano > 12 and pdf.stringWidth(texto, fuente, tamano) > ancho_max:
        tamano -= 1
    pdf.setFont(fuente, tamano)
    pdf.drawCentredString(x, y, texto)


def generar_certificado_pdf(estudiante, curso, fecha):
    """Devuelve los bytes de un certificado simple en PDF (A4 horizontal)."""
    buffer = BytesIO()
    ancho, alto = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=(ancho, alto))
    pdf.setTitle(f"Certificado - {curso.nombre}")
    pdf.setAuthor("Capacitaciones +")

    pdf.setStrokeColorRGB(*AZUL)
    pdf.setLineWidth(6)
    pdf.rect(24, 24, ancho - 48, alto - 48)
    pdf.setStrokeColorRGB(*AMARILLO)
    pdf.setLineWidth(2)
    pdf.rect(38, 38, ancho - 76, alto - 76)

    centro = ancho / 2
    maximo = ancho - 160

    pdf.setFillColorRGB(*GRIS)
    _texto_centrado(pdf, centro, alto - 105, "CAPACITACIONES +", "Helvetica", 14, maximo)

    pdf.setFillColorRGB(*AZUL)
    _texto_centrado(pdf, centro, alto - 160, "Certificado de finalización", "Helvetica-Bold", 36, maximo)

    pdf.setFillColorRGB(*GRIS)
    _texto_centrado(pdf, centro, alto - 215, "Se reconoce que", "Helvetica", 16, maximo)

    pdf.setFillColorRGB(*AZUL)
    _texto_centrado(pdf, centro, alto - 265, f"{estudiante.nombres} {estudiante.apellidos}", "Helvetica-Bold", 32, maximo)
    pdf.setStrokeColorRGB(*AMARILLO)
    pdf.setLineWidth(2)
    pdf.line(centro - 190, alto - 282, centro + 190, alto - 282)

    pdf.setFillColorRGB(*GRIS)
    _texto_centrado(pdf, centro, alto - 318, "ha completado satisfactoriamente el curso", "Helvetica", 16, maximo)

    pdf.setFillColorRGB(*AZUL)
    _texto_centrado(pdf, centro, alto - 362, curso.nombre, "Helvetica-Bold", 26, maximo)

    pdf.setFillColorRGB(*GRIS)
    _texto_centrado(pdf, centro, alto - 400, f"{curso.duracion_horas} horas · {curso.categoria}", "Helvetica", 13, maximo)
    _texto_centrado(pdf, centro, alto - 422, f"Emitido el {fecha:%d/%m/%Y}", "Helvetica", 13, maximo)

    pdf.setStrokeColorRGB(*AZUL)
    pdf.setLineWidth(1)
    pdf.line(centro - 110, 100, centro + 110, 100)
    pdf.setFillColorRGB(*AZUL)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(centro, 82, "Capacitaciones +")

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
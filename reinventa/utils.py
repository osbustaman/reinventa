import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from io import BytesIO

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def validarRut(rut):
    rut = rut.replace(".", "").replace("-", "")  # Eliminar puntos y guiones
    if not re.match(r'^\d{1,8}[0-9K]$', rut):  # Verificar formato
        return False
    rut_sin_dv = rut[:-1]
    dv = rut[-1].upper()  # Obtener dígito verificador
    multiplicador = 2
    suma = 0
    for r in reversed(rut_sin_dv):
        suma += int(r) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado


def getLatitudeLongitude(address):
        # Crear un objeto geolocator utilizando el proveedor Nominatim
        geolocator = Nominatim(user_agent="Nominatim", timeout=10)

        # Obtener la ubicación (latitud, longitud) a partir de la dirección
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return {
                'latitude': latitude, 
                'longitude': longitude
            }
        else:
            return False
        
def isWithinTheDiameter(lat_a, lon_a, lat_b, lon_b, radio_km = 0.1):
    # Crear objetos de ubicación para A y B
    location_a = (lat_a, lon_a)
    location_b = (lat_b, lon_b)

    # Calcular la distancia entre las ubicaciones A y B en kilómetros
    distance_km = geodesic(location_a, location_b).kilometers

    # Verificar si la distancia es menor o igual al radio deseado
    return distance_km <= radio_km


def send_mail():
    # Configura los parámetros del servidor SMTP
    smtp_server = 'smtp.tu_servidor.com'
    smtp_port = 587  # El puerto puede variar según el servidor de correo
    smtp_user = 'tu_correo@gmail.com'
    smtp_password = 'tu_contraseña'

    # Crea un objeto MIME para el mensaje
    msg = MIMEMultipart()
    msg['From'] = 'tu_correo@gmail.com'
    msg['To'] = 'destinatario@example.com'
    msg['Subject'] = 'Asunto del correo'

    # Agrega el cuerpo del mensaje (puede ser HTML)
    body = "Hola, este es un correo de prueba con un archivo PDF adjunto."
    msg.attach(MIMEText(body, 'plain'))


    # Genera un archivo PDF en memoria
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100, 750, "Hola, este es un PDF generado desde Python.")
    pdf.showPage()
    pdf.save()

    # Adjunta el archivo PDF generado
    pdf_attachment_part = MIMEApplication(pdf_buffer.getvalue(), Name='archivo.pdf')
    pdf_attachment_part['Content-Disposition'] = 'attachment; filename="archivo.pdf"'
    msg.attach(pdf_attachment_part)

    # Reinicia el buffer
    pdf_buffer.close()

    # Inicia una conexión segura con el servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        # Envía el correo
        server.sendmail(smtp_user, msg['To'], msg.as_string())

        # Cierra la conexión con el servidor SMTP
        server.quit()
        print("Correo con archivo PDF generado y adjunto enviado con éxito")

    except Exception as e:
        print("Error al enviar el correo:", str(e))
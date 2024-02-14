import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

"""



"""

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_secure, user, password, from_name, bbc):
        """
        Inicializa un objeto EmailSender para enviar correos electrónicos mediante SMTP.

        Args:
            smtp_server (str): Dirección del servidor SMTP.
            smtp_port (int): Puerto del servidor SMTP.
            smtp_secure (bool): Indica si se utiliza una conexión segura SSL/TLS.
            user (str): Dirección de correo electrónico del remitente.
            password (str): Contraseña o clave de aplicación del remitente.
            from_name (str): Nombre del remitente que se mostrará en el correo.
            bbc (str): Dirección de correo electrónico para copia oculta (BCC).
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_secure = smtp_secure
        self.user = user
        self.password = password
        self.from_name = from_name
        self.bbc = bbc

    def send_email(self, to_email, subject, body, is_html=False):
        """
        Envía un correo electrónico al destinatario especificado.

        Args:
            to_email (str): Dirección de correo electrónico del destinatario.
            subject (str): Asunto del correo electrónico.
            body (str): Cuerpo del mensaje del correo electrónico.
            is_html (bool): Indica si el cuerpo del correo es formato HTML.

        Returns:
            bool: True si el correo se envió correctamente, False en caso de error.
        """
        try:
            # Crear el mensaje
            message = MIMEMultipart()
            message["From"] = Header(self.from_name, "utf-8")
            message["To"] = to_email
            message["Subject"] = Header(subject, "utf-8")
            if is_html:
                # Si es HTML, usar MIMEText con tipo "html"
                message.attach(MIMEText(body, "html"))
            else:
                # Si es texto plano, usar MIMEText con tipo "plain"
                message.attach(MIMEText(body, "plain"))

            # Establecer conexión con el servidor SMTP
            if self.smtp_secure:
                servidor = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                servidor = smtplib.SMTP(self.smtp_server, self.smtp_port)

            # Autenticación con el servidor
            servidor.login(self.user, self.password)

            # Configurar destinatario y copia oculta (BBC)
            destinatarios = [to_email]
            if self.bbc:
                destinatarios.append(self.bbc)

            # Enviar el mensaje
            servidor.sendmail(self.user, destinatarios, message.as_string())

            # Cerrar la conexión con el servidor
            servidor.quit()
            print("Correo enviado correctamente.")
            return True

        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
            return False
        
    def attach_pdf(self, pdf_path):
        """
        Adjunta un archivo PDF al correo electrónico.

        Args:
            pdf_path (str): Ruta del archivo PDF que se adjuntará.

        Returns:
            bool: True si el archivo se adjunta correctamente, False en caso de error.
        """
        try:
            # Verificar si el archivo existe
            if not os.path.exists(pdf_path):
                print(f"Error: El archivo PDF no existe en la ruta especificada: {pdf_path}")
                return False

            # Crear el objeto MIME para el archivo adjunto
            with open(pdf_path, "rb") as attachment:
                pdf_part = MIMEBase("application", "pdf")
                pdf_part.set_payload(attachment.read())

            # Codificar el archivo adjunto en base64
            encoders.encode_base64(pdf_part)

            # Establecer las cabeceras del archivo adjunto
            pdf_part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(pdf_path)}")

            # Adjuntar el archivo al mensaje
            self.message.attach(pdf_part)
            print(f"Archivo PDF adjuntado: {os.path.basename(pdf_path)}")
            return True

        except Exception as e:
            print(f"Error al adjuntar el archivo PDF: {str(e)}")
            return False
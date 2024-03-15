import base64
import io
import json
import requests
import tempfile

from applications.account.models import WithdrawalRequestReinventor
from applications.reinventor.api.serializer import WithdrawalRequestReinventorSerializer

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.template.loader import get_template

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from xhtml2pdf import pisa

from applications.reinventor.models import Company
from reinventa.settings.base import BASE_DIR

@permission_classes([AllowAny])
class generatePdfAPIView(generics.GenericAPIView):

    

    def post(self, request, *args, **kwargs):

        wrr_id = request.data['wrr_id']
        type_pdf = request.data['type_pdf']

        html_template = get_template('reinventor/pdf/solicitud.html')

        try:
            object_request = WithdrawalRequestReinventor.objects.get(wrr_id=wrr_id)
        except WithdrawalRequestReinventor.DoesNotExist:
            Response({"error": "No se encontró la solicitud de retiro correspondiente al ID proporcionado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            object_company = Company.objects.all().last()
        except WithdrawalRequestReinventor.DoesNotExist:
            Response({"error": "No se encuentra configurada la empresa en el sistema"}, status=status.HTTP_404_NOT_FOUND)

        # Crear un contexto para el HTML
        context = {
            'base_dir': BASE_DIR,
            "wrr_id": object_request.wrr_id,
            "co_name": object_company.co_name
        }

        # Renderizar el HTML con el contexto
        rendered_html = html_template.render(context)

        # Crear un archivo temporal con extensión .html
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmpfile:

            tmpfile.write(rendered_html.encode())

            # Crear un objeto StringIO para guardar el PDF generado
        pdf_buffer = io.BytesIO()

        # Crear el documento PDF usando xhtml2pdf
        pisa.CreatePDF(rendered_html, dest=pdf_buffer)

        # Obtener el contenido del PDF en bytes
        pdf_bytes = pdf_buffer.getvalue()

        # Convertir el PDF a base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode()

        # Cerrar el buffer del PDF
        pdf_buffer.close()
        tmpfile.close()

        return Response({'pdf_base64': pdf_base64}, status=status.HTTP_200_OK)


# para implementar
@permission_classes([AllowAny])
class WithdrawalRequestUpdateAPIView(generics.UpdateAPIView):
    queryset = WithdrawalRequestReinventor.objects.all()
    serializer_class = WithdrawalRequestReinventorSerializer

    def update(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        reinventor_id = request.data['reinventor_id']
        new_state = request.data['wrr_estaterequest']

        # Verificar si los campos requeridos están presentes en la solicitud
        if not all([user_id, reinventor_id, new_state]):
            return Response(
                {"error": "Se requieren user, reinventor y wrr_estaterequest en la solicitud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener el objeto WithdrawalRequestReinventor basado en los filtros proporcionados
        try:
            withdrawal_request = WithdrawalRequestReinventor.objects.get(
                user_id=user_id, reinventor_id=reinventor_id
            )
        except WithdrawalRequestReinventor.DoesNotExist:
            return Response(
                {"error": "No se encontró la solicitud de retiro correspondiente a los filtros proporcionados."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar el campo wrr_estaterequest y guardar los cambios
        withdrawal_request.wrr_estaterequest = new_state
        withdrawal_request.save()

        # Serializar y devolver la solicitud de retiro actualizada
        serializer = self.get_serializer(withdrawal_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
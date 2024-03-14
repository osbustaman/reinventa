import json
import requests

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from applications.account.models import WithdrawalRequestReinventor
from applications.reinventor.api.serializer import WithdrawalRequestReinventorSerializer


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
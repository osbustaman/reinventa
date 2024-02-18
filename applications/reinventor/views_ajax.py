from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User
from applications.account.models import RequestTracking, WithdrawalRequestReinventor
from applications.reinventor.forms import RequestTrackingForm

@csrf_exempt  
def new_observation(request):
    if request.method == 'POST':
        try:
            RequestTracking.objects.create( 
                user = User.objects.get(id = request.session['id']),
                withdrawalRequestReinventor = WithdrawalRequestReinventor.objects.get(wrr_id=int(request.POST["wrr_id"])),
                rt_observation = request.POST["respuesta"]
            )

            response = {
                'message': 'success',
                'error': False
            }
            response_data = {'response': response}
            return JsonResponse(response_data)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Error al decodificar JSON: {}'.format(str(e))}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
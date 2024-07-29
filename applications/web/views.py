import json

from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from applications.web.models import Applications, Banner, BlockHome, Header, ListItems, Plugins, SocialMediaNews, Testimonials

# Create your views here.
def news(request):

    list_object_banner = Banner.objects.filter(ba_active='Y').order_by('ba_element_order')
    list_social_media_news = SocialMediaNews.objects.filter(smn_active='Y').order_by('sm_element_order')

    instance_header = Header.objects.filter(he_active='Y').first()
    list_items = ListItems.objects.filter(header = instance_header, li_active='Y').order_by('li_order')

    list_block_home = BlockHome.objects.filter(bh_active='Y').order_by('bh_order')

    list_element_block_2 = Plugins.objects.filter(blockHome__bh_type_block=2, plu_active='Y').order_by('plu_order')
    list_element_block_3 = Plugins.objects.filter(blockHome__bh_type_block=3, plu_active='Y').order_by('plu_order')

    list_testimonials = Testimonials.objects.filter(tm_active='Y')

    data = {
        "list_object_banner": list_object_banner,
        "list_social_media_news": list_social_media_news,
        "instance_header": instance_header,
        "list_items": list_items,
        "list_block_home": list_block_home,
        "list_element_block_2": list_element_block_2,
        "list_element_block_3": list_element_block_3,
        "list_testimonials": list_testimonials
    }

    return render(request, 'web/news.html', data)
    

@csrf_exempt  
def ajax_send_message(request):
    if request.method == 'POST':
        try:

            app = Applications()
            app.app_name = request.POST['name']
            app.app_mail = request.POST['email']
            app.app_phone = request.POST['phone']
            app.app_message = request.POST['message']
            app.save()

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
    

@csrf_exempt  
def ajax_to_subscribe(request):
    if request.method == 'POST':
        try:

            app = Applications()
            app.app_mail = request.POST['email']
            app.save()

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
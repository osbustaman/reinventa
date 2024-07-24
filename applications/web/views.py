from django.shortcuts import render

from applications.web.models import Banner, SocialMediaNews

# Create your views here.
def news(request):

    is_web = request.GET.get('web', None)

    if is_web:

        list_object_banner = Banner.objects.filter(ba_active='Y').order_by('ba_element_order')
        list_social_media_news = SocialMediaNews.objects.filter(smn_active='Y').order_by('sm_element_order')

        data = {
            "list_object_banner": list_object_banner,
            "list_social_media_news": list_social_media_news,
        }
        return render(request, 'web/news.html', data)
    
    else:
        return render(request, 'web/page_in_construction.html')
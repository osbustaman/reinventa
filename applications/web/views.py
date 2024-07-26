from django.shortcuts import render

from applications.web.models import Banner, BlockHome, Header, ListItems, Plugins, SocialMediaNews, Testimonials

# Create your views here.
def news(request):

    is_web = request.GET.get('web', None)

    if is_web:

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
    
    else:
        return render(request, 'web/page_in_construction.html')
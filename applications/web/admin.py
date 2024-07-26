from django.contrib import admin

from applications.web.models import Applications, Banner, BlockHome, Plugins, RequestWeb, Services, SocialMediaNews, ListItems, Header, Image, SocialNetwork, Testimonials

# Register your models here.

class ListItemsAdmin(admin.ModelAdmin):
    list_display = ['li_id', 'header', 'li_name', 'li_active']
    list_filter = ['li_name', 'li_active']
    search_fields = ['header']
    list_per_page = 10

class HeaderAdmin(admin.ModelAdmin):
    list_display = ['he_id', 'he_logo', 'he_email', 'he_phone', 'he_active']
    list_per_page = 10


class ImageAdmin(admin.ModelAdmin):
    list_display = ('img_id', 'img_code', 'img_name',
                    'img_image', 'img_typeimage')
    list_per_page = 10

class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('sn_id', 'sn_name', 'sn_icon')
    list_per_page = 10


class RequestWebAdmin(admin.ModelAdmin):
    list_display = ('rw_id', 'rw_namecontact', '_typeServices', 'rw_phonocontact', 'rw_mailcontact')
    list_per_page = 10


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('serv_id', 'serv_name', 'serv_title',
                    'serv_icon', 'serv_image')
    list_per_page = 10

    
class BlockHomeAdmin(admin.ModelAdmin):
    list_display = ('bh_id', 'bh_name', 'bh_active')
    list_per_page = 10


class PluginsAdmin(admin.ModelAdmin):
    list_display = ('plu_id', 'blockHome', 'plu_elementname', 'plu_title', 'plu_linkactive', 'plu_active')
    list_per_page = 10

class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('tm_id', 'tm_nameperson', 'tm_positionperson', 'tm_image', 'tm_active')
    list_per_page = 10

class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'app_name', 'app_mail', 'app_phone', 'app_message')
    list_per_page = 10

admin.site.register(Banner)
admin.site.register(SocialMediaNews)
admin.site.register(ListItems, ListItemsAdmin)
admin.site.register(Header, HeaderAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(RequestWeb, RequestWebAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(BlockHome, BlockHomeAdmin)
admin.site.register(Plugins, PluginsAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Applications, ApplicationsAdmin)
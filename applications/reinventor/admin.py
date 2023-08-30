from django.contrib import admin

from applications.account.models import Comuna, Pais, Region, Reinventor, RequestTracking, UserReinventor, WithdrawalRequestReinventor

# Register your models here.
admin.site.register(Pais)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Reinventor)
admin.site.register(UserReinventor)
admin.site.register(WithdrawalRequestReinventor)
admin.site.register(RequestTracking)
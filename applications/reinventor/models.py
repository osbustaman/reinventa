from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from applications.account.models import Comuna, Pais, Region


# Create your models here.

class Company(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    co_id = models.AutoField("Key", primary_key=True)
    co_name = models.CharField("Nombre Empresa", max_length=255)
    co_address = models.CharField("Dirección de la empresa", help_text="ej: calle siempre viva 1010", max_length=255)
    pais = models.ForeignKey(Pais, verbose_name="País",
                                    db_column="co_pais_id", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="co_region_id", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Comuna, verbose_name="Comuna", db_column="co_comuna_id", on_delete=models.PROTECT)
    
    co_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    co_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    co_logo = models.ImageField(
        "Logo Empresa", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='image/logo/', null=True, blank=True)
    
    co_active = models.CharField(
        "Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.co_id

    def __str__(self):
        return f"{ self.co_id } - { self.co_name }"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Company, self).save(*args, **kwargs)

    class Meta:
        db_table = 'com_company'
        ordering = ['co_id']

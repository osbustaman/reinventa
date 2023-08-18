from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.

class Pais(TimeStampedModel):
    pa_id = models.AutoField("Key", primary_key=True)
    pa_nombre = models.CharField("Nombre país", max_length=255)
    pa_codigo = models.IntegerField("Código area país", unique=True)

    def __int__(self):
        return self.pa_id

    def __str__(self):
        return "{n}".format(n=self.pa_nombre.title())

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Pais, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_pais'
        ordering = ['pa_id']


class Region(TimeStampedModel):
    re_id = models.AutoField("Key", primary_key=True)
    re_nombre = models.CharField("Nombre región", max_length=255)
    pais = models.ForeignKey(Pais, verbose_name="País", blank=True, null=True, on_delete=models.PROTECT,
                             db_column="re_pais")
    re_numeroregion = models.CharField(
        "Sigla de región", blank=True, null=True, max_length=5)
    re_numero = models.IntegerField("Número de región", db_index=True)

    def __int__(self):
        return self.re_id

    def __str__(self):
        return "{n}".format(n=self.re_nombre.title())

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Region, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_region'
        ordering = ['re_id']


class Comuna(TimeStampedModel):
    com_id = models.AutoField("Key", primary_key=True)
    com_nombre = models.CharField("Nombre comuna", max_length=255)
    com_numero = models.IntegerField("Numero comuna", default=0)
    region = models.ForeignKey(Region, verbose_name="Región", blank=True, null=True, on_delete=models.PROTECT,
                               db_column="com_region")

    def __int__(self):
        return self.com_id

    def __str__(self):
        return "{n}".format(n=self.com_nombre.title())

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Comuna, self).save(*args, **kwargs)

    class Meta:
        db_table = 'conf_comuna'
        ordering = ['com_id']

class Reinventor(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    re_id = models.AutoField("Key", primary_key=True)
    re_nameentity = models.CharField("Nombre empresa", max_length=255)
    re_namereinventor = models.CharField("Nombre completo persona a cargo", max_length=255)
    re_address = models.CharField("Dirección de la empresa", help_text="ej: calle siempre viva 1010", max_length=255)
    pais = models.ForeignKey(Pais, verbose_name="País",
                             db_column="re_pais_id", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="re_region_id", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Comuna, verbose_name="Comuna", db_column="re_comuna_id", on_delete=models.PROTECT)
    
    re_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    re_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    re_logo = models.ImageField(
        "Logo Empresa", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='image/logo/', null=True, blank=True)
    
    re_active = models.CharField(
        "Activo", choices=OPTIONS, max_length=1, default="Y")
    

    def __int__(self):
        return self.re_id
    
    def __str__(self):
        return f"{self.re_id} - {self.re_nameentity}"
    
    def __create_address(self):
        return f"""{ self.re_address }, { self.comuna.com_nombre }, { self.region.re_nombre }, { self.pais.pa_nombre }"""

    re_createaddress = property(__create_address)

    def save(self, *args, **kwargs):
        super(Reinventor, self).save(*args, **kwargs)

    class Meta:
        db_table = "re_reinventor"
        ordering = ['re_id']


class UserReinventor(TimeStampedModel):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    TYPE_USER = (
        (0, ' [Seleccione] '),
        (1, 'ADMINISTRADOR REINVENTA'),
        (2, 'REINVENTOR'),
    )

    ur_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="User",
                             db_column="ur_user_id", on_delete=models.PROTECT)
    reinventor = models.ForeignKey(Reinventor, verbose_name="Reinventor",
                             db_column="ur_reinventor_id", on_delete=models.PROTECT, null=True, blank=True)
    ur_typeuser = models.IntegerField(
        "Tipo de usuario", choices=TYPE_USER, default=0)
    ur_active = models.CharField(
        "Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.ur_id
    
    def __str__(self):
        return f"{ self.ur_id } - { self.user.username }"

    def save(self, *args, **kwargs):
        super(UserReinventor, self).save(*args, **kwargs)

    class Meta:
        db_table = "re_user_reinventor"
        ordering = ['ur_id']


class WithdrawalRequestReinventor(TimeStampedModel):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    ESTATE_REQUEST = (
        (0, ' [Seleccione] '),
        (1, 'REINVENTOR SOLICITA'),
        (2, 'VISTA POR REINVENTA'),
        (3, 'REINVENTA VA EN RUTA'),
        (4, 'RETIRADO POR REINVENTA'),
    )

    wrr_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="User",
                             db_column="ur_user_id", on_delete=models.PROTECT)
    reinventor = models.ForeignKey(Reinventor, verbose_name="Reinventor",
                             db_column="ur_reinventor_id", on_delete=models.PROTECT)
    wrr_dateout = models.DateField("Fecha de retiro", null=True, blank=True)
    wrr_hourout = models.CharField("Hora del retiro", null=True, blank=True, max_length=10)
    wrr_quantityliters = models.FloatField("Litros de aceite", null=True, blank=True)
    wrr_estaterequest = models.IntegerField(
        "Estado de la solicitud", choices=ESTATE_REQUEST, default=1)
    wrr_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.wrr_id
    
    def __str__(self):
        return f"{ self.wrr_id } - { self.user.username } - { self.reinventor.re_nameentity }"

    def save(self, *args, **kwargs):
        super(WithdrawalRequestReinventor, self).save(*args, **kwargs)

    class Meta:
        db_table = "re_withdrawal_request_reinventor"
        ordering = ['wrr_id']
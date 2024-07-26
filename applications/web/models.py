from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from unidecode import unidecode
from ckeditor.fields import RichTextField


# Create your models here.
class Image(TimeStampedModel):

    TYPE_IMAGE = (
        (1, 'Home'),
        (2, 'Pages'),
    )

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    BLOCKS = (
        (1, 'nuestra_historia'),
        (2, 'reinventores'),
        (3, 'que_hacemos'),
        (4, 'testimonios'),
    )

    img_id = models.AutoField("Key", primary_key=True)
    img_type_block = models.IntegerField("Tipo de bloque", choices=BLOCKS, default=1)
    img_name = models.CharField("nombre imagen", max_length=100)
    img_code = models.CharField(
        "código imagen", null=True, blank=True, help_text="no es obligación", max_length=100)
    img_image = models.ImageField(
        "subir imagen", help_text="Formatos .jpg|.png|.gif|.jpeg", upload_to='image/')
    img_typeimage = models.IntegerField("tipo imagen", choices=TYPE_IMAGE)
    img_description = models.TextField(
        "Descripción de la imagen", help_text="Necesario para el SEO del sitio")
    img_active = models.CharField("Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.img_image

    def __str__(self) -> str:
        return self.img_name

    def save(self, *args, **kwargs):
        self.img_code = f'[image_{self.img_id}]'
        super(Image, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_image'
        ordering = ['img_id']
        verbose_name_plural = 'Imagenes'

class BlockHome(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    BLOCKS = (
        (1, 'nuestra_historia'),
        (2, 'reinventores'),
        (3, 'que_hacemos'),
        (4, 'testimonios'),
    )

    bh_id = models.AutoField("Key", primary_key=True)
    bh_type_block = models.IntegerField("Tipo de bloque", choices=BLOCKS, default=1)
    bh_name = models.CharField(
        "nombre bloque", help_text="es el tipo de elemento que se verá en la página", max_length=100)
    bh_html = RichTextField("HTML o texto para el bloque", help_text="Ingrese el texto utilizando CKEditor.")
    bh_order = models.IntegerField("orden de posición", default=0)
    image = models.ForeignKey(
        Image, verbose_name="Image", db_column="bh_image_id", null=True, blank=True, on_delete=models.PROTECT)
    bh_active = models.CharField("bloque activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.bh_id

    def __str__(self) -> str:
        return self.bh_name

    def save(self, *args, **kwargs):
        super(BlockHome, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_block_home'
        ordering = ['bh_id']
        verbose_name_plural = 'Bloques Home'

class Services(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    serv_id = models.AutoField("Key", primary_key=True)
    serv_name = models.CharField("nombre servicio", max_length=100)
    serv_title = models.CharField("titulo servicio", max_length=100)
    serv_subtitle = models.CharField("sub-titulo servicio", max_length=100)
    serv_icon = models.CharField("icon servicio", max_length=100, null=True, blank=True)
    serv_image = models.ImageField(
        "subir imagen", help_text="tamaño de la imagen 1920x1080, solo formatos .jpg|.png|.gif|.jpeg", upload_to='image/', null=True, blank=True)
    serv_htmlshort = models.TextField("HTML o texto corto para el servicio", null=True, blank=True)
    serv_isactive = models.IntegerField(
        "servicio activo", choices=OPTIONS, default="Y")

    def __int__(self):
        return self.serv_id

    def __str__(self) -> str:
        return self.serv_name

    def save(self, *args, **kwargs):
        super(Services, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_services'
        ordering = ['serv_id']
        verbose_name_plural = 'Servicios'

class RequestWeb(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    rw_id = models.AutoField("Key", primary_key=True)
    rw_namecontact = models.CharField("nombre del contacto", max_length=100, null=True, blank=True)
    services = models.ForeignKey(Services, verbose_name="Services",
                                on_delete=models.PROTECT, db_column="rw_services_id", null=True, blank=True)
    rw_phonocontact = models.CharField("teléfono del contacto", max_length=20, null=True, blank=True)
    rw_mailcontact = models.CharField("mail del contacto", max_length=150, null=True, blank=True)
    rw_mesagge = models.TextField("Mensaje del contacto", null=True, blank=True)
    rw_active = models.CharField("Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.rw_id

    def __str__(self) -> str:
        return f'{self.rw_namecontact}'
    
    def typeServices(self) -> str:
        try:
            typeService = self.services.serv_name
            return typeService
        except:
            typeService = f'{self.rw_id}'
            return typeService
        
    _typeServices = property(typeServices)

    def save(self, *args, **kwargs):
        super(RequestWeb, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_request_web'
        ordering = ['rw_id']
        verbose_name_plural = 'Solicitud'

class SocialNetwork(TimeStampedModel):

    ICON_NETWORK = (
        (1, 'fab fa-twitter fw-normal'),
        (2, 'fab fa-facebook-f fw-normal'),
        (3, 'fab fa-linkedin-in fw-normal'),
        (4, 'fab fa-instagram fw-normal'),
        (5, 'fab fa-youtube fw-normal'),
    )

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    sn_id = models.AutoField("Key", primary_key=True)
    sn_name = models.CharField("nombre red", max_length=100)
    sn_icon = models.IntegerField("icon red", choices=ICON_NETWORK)
    sn_active = models.CharField("Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.sn_id

    def __str__(self) -> str:
        return self.sn_name

    def save(self, *args, **kwargs):
        super(SocialNetwork, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_social_network'
        ordering = ['sn_id']
        verbose_name_plural = 'Redes Sociales'

class Banner(TimeStampedModel):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    ba_id = models.AutoField("Key", primary_key=True)
    ba_title_up = models.CharField("Bajada de título superior", max_length=255)
    ba_title = models.CharField("Bajada de título", max_length=255)
    ba_download_title = models.CharField("Bajada de título", max_length=255)
    ba_logo = models.ImageField("Imagen banner", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='image/logo/', null=True, blank=True)
    ba_element_order = models.IntegerField("Orden", null=True, blank=True)
    ba_active = models.CharField("Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.ba_id

    def __str__(self):
        return f"{self.ba_title.title()}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Banner, self).save(*args, **kwargs)

    class Meta:
        db_table = 'banner'
        ordering = ['ba_id']

class SocialMediaNews(TimeStampedModel):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    SOCIAL_NETWORKS = (
        ('F', 'Facebook'),
        ('I', 'Instagram'),
        ('TT', 'Tik Tok'),
    )

    smn_id = models.AutoField("Key", primary_key=True)
    smn_name = models.CharField("nombre noticia ", max_length=255)
    smn_link = models.TextField("link script")
    smn_image = models.ImageField("Imagen banner", help_text="Formatos .jpg|.png|.gif|.jpeg, es opcional", upload_to='image/logo/', null=True, blank=True)
    smn_social_network = models.CharField("Tipo red social", choices=SOCIAL_NETWORKS, max_length=2, null=True, blank=True)
    sm_element_order = models.IntegerField("Orden", null=True, blank=True)
    smn_active = models.CharField("Activo", choices=OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.smn_id

    def __str__(self):
        return f"{self.smn_name.title()}"

    def save(self, *args, **kwargs):
        super(SocialMediaNews, self).save(*args, **kwargs)

    class Meta:
        db_table = 'social_media_news'
        ordering = ['smn_id']

class Header(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    he_id = models.AutoField("Key", primary_key=True)
    he_logo = models.ImageField(
        "Logo Header", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='image/')
    he_address = models.CharField("Dirección", max_length=255)
    he_email = models.EmailField("Correo", max_length=255)
    he_phone = models.CharField("Teléfono", max_length=255)
    he_search = models.CharField("Tiene buscador?", max_length=1, choices=ACTIVE, default="Y")
    he_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.he_id
    
    def __str__(self):
        return f"{self.he_id} - {self.he_email}"
    
    def save(self, *args, **kwargs):
        super(Header, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Header de la página"
        db_table = "web_header"
        ordering = ['he_id']

class ListItems(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    IS_ANCHOR = (
        ("Y", "YES"),
        ("N", "NO")
    )

    li_id = models.AutoField("Key", primary_key=True)
    header = models.ForeignKey(Header, verbose_name="Header",
                                                    db_column="li_header_id", on_delete=models.PROTECT)
    li_name = models.CharField("Nombre Menú", max_length=100)
    li_anchor = models.CharField("Tiene ancla", max_length=1, choices=IS_ANCHOR, default="Y")
    li_link = models.CharField("link o ancla", max_length=100, null=True, blank=True)
    li_order = models.IntegerField("Posición del item", null=True, blank=True)
    li_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.li_id
    
    def __str__(self):
        return f"{self.li_id} - {self.li_name}"
    
    def save(self, *args, **kwargs):
        super(ListItems, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de Items"
        db_table = "web_items"
        ordering = ['li_id']

    
class Plugins(TimeStampedModel):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    plu_id = models.AutoField("Key", primary_key=True)
    blockHome = models.ForeignKey(BlockHome, verbose_name="BlockHome",
                                on_delete=models.PROTECT, db_column="plu_block_home", null=True, blank=True)
    plu_elementname = models.CharField("nombre del elemento", max_length=100)
    plu_icon = models.CharField(
        "icono del elemento", max_length=100, null=True, blank=True)
    plu_title = models.CharField(
        "título del elemento", max_length=100, null=True, blank=True)
    plu_text = models.TextField("texto", null=True, blank=True)
    plu_linkactive = models.TextField("link activo", choices=OPTIONS, default=1)
    plu_link = models.TextField("link del elemento", null=True, blank=True)
    plu_order = models.IntegerField("Posición del plugin", null=True, blank=True)
    plu_image = models.ImageField(
        "subir imagen", help_text="Formatos .jpg|.png|.gif|.jpeg", upload_to='company_images/', null=True, blank=True)
    plu_active = models.TextField("plugin activo", choices=OPTIONS, default=1)

    def __int__(self):
        return self.plu_id

    def __str__(self) -> str:
        return self.plu_elementname

    def save(self, *args, **kwargs):
        super(Plugins, self).save(*args, **kwargs)

    class Meta:
        db_table = 'web_plugins'
        ordering = ['plu_id']
        verbose_name_plural = 'Plugins'

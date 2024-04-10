from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.

class Banner(TimeStampedModel):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    ba_id = models.AutoField("Key", primary_key=True)
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
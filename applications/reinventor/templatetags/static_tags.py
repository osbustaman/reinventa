# -*- encoding: utf-8 -*-
from django import template
from django.conf import settings
from django.templatetags.static import *

register = template.Library()

@register.simple_tag
def statics_tag(file):
    return '%s%s%s' % (settings.STATIC_URL , 'gentella/' , file)


@register.simple_tag
def statics_tag_maps(file):
    return '%s%s%s' % (settings.STATIC_URL , 'maps/' , file)


@register.simple_tag
def statics_tag_all(file):
    return '%s%s%s' % (settings.STATIC_URL , 'static/' , file)

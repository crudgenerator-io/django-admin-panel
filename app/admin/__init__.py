from .sites import site
from django.utils.module_loading import autodiscover_modules
from .options import ModelAdmin
from django.contrib.admin import register

def autodiscover():
    autodiscover_modules('admin', register_to=site)
    autodiscover_modules('django.contrib.admin', register_to=site)


__all__ = ["site", 'register', 'autodiscover', 'ModelAdmin']

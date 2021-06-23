from django import template
import mimetypes
from django.db.models.fields.files import FieldFile

register = template.Library()


@register.filter(name="file_info")
def file_info(value):
    if not value or type(value) != FieldFile:
        return ''
    name = value.url.split("/")[-1]
    val = {
        "name": name,
        "ext": mimetypes.guess_type(name)[0],
        "size": str(round(value.file.size / 1024, 1)) + "KB",
        "url": value.url
    }
    return f'{val["name"]};{val["ext"]};{val["size"]};{val["url"]}'

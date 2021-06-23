from admin import register
from django.utils.translation import gettext as _
from admin.admin import UserAdmin as BaseUserAdmin
from admin.options import ModelAdmin
from .models import User, EmptyClass


@register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('last_name', 'first_name', 'email', 'username', 'is_superuser', 'type', 'last_login', 'info')
    sortable_by = ('last_name', 'first_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), { 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional'), {
                'fields':
                    (
                        'state',
                        'zip',
                        'is_privileged_associate',
                        'created',
                        'deletion_scheduled',
                        'activation_time',
                        'profile_picture',
                        'times_accessed_platform_anonymously',
                        'info',
                        'balance',
                        'type'
                    )
            }
        )
    )


@register(EmptyClass)
class PraznaKlasaAdmin (ModelAdmin):
    pass

from .models import Text

@register(Text)
class TextAdmin(ModelAdmin):
   list_display = ('text_1', 'text_2', 'text_3',)
   sortable = ('text_1', 'text_2', 'text_3',)
   fieldsets = (
     (_('Textual'), {'fields': ('text_1', 'text_2', 'text_3', )}),
  )

from .models import Decimal

@register(Decimal)
class DecimalAdmin(ModelAdmin):
   list_display = ('dec_1', 'dec_2', 'dec_3',)
   sortable = ('dec_1', 'dec_2', 'dec_3',)
   fieldsets = (
     (_('Decimals'), {'fields': ('dec_1', 'dec_2', 'dec_3', )}),
  )

from .models import Enumeration

@register(Enumeration)
class EnumerationAdmin(ModelAdmin):
   list_display = ('e1', 'e2', 'e3',)
   sortable = ('e1', 'e2', 'e3',)
   fieldsets = (
     (_('Enumerations'), {'fields': ('e1', 'e2', 'e3', )}),
  )

from .models import Time

@register(Time)
class TimeAdmin(ModelAdmin):
    list_display = ('time_1', 'time_2', 'time_3', 'time_4', )
    sortable = ('time_1', 'time_2', 'time_3', 'time_4', )
    fieldsets = (
        (_('Date & Time'), {'fields': ('time_1', 'time_2', 'time_3', 'time_4', )}),
    )

from .models import File

@register(File)
class FileAdmin(ModelAdmin):
    list_display = ('f1', 'f2', 'f3', )
    sortable = ('f1', 'f2', 'f3', )
    fieldsets = (
        (_('Files'), {'fields': ('f1', 'f2', 'f3', )}),
    )

from .models import Char

@register(Char)
class CharAdmin(ModelAdmin):
    list_display = ('char_1', 'char_2', 'char_3', 'char_4', 'char_5',)
    sortable = ('char_1', 'char_2', 'char_3', 'char_4', 'char_5',)
    fieldsets = (
        (_('Chars'), {'fields': ('char_1', 'char_2', 'char_3', 'char_4', 'char_5',)}),
    )


from .models import Boolean

@register(Boolean)
class BooleanAdmin(ModelAdmin):
    list_display = ('bool_1', 'bool_2', 'bool_3',)
    sortable = ('bool_1', 'bool_2', 'bool_3',)
    fieldsets = (
        (_('Booleans'), {'fields': ('bool_1', 'bool_2', 'bool_3',)}),
    )

from .models import Datetime

@register(Datetime)
class DatetimeAdmin(ModelAdmin):
    list_display = ('dt_1', 'dt_2', 'dt_3',)
    sortable = ('dt_1', 'dt_2', 'dt_3',)
    fieldsets = (
        (_('Date & Time'), {'fields': ('dt_1', 'dt_2', 'dt_3',)}),
    )

from .models import Integer


@register(Integer)
class IntegerAdmin(ModelAdmin):
    list_display = ('int_1', 'int_2', 'int_3',)
    sortable = ('int_1', 'int_2', 'int_3',)
    fieldsets = (
        (_('Integers'), {'fields': ('int_1', 'int_2', 'int_3',)}),
    )

from .models import Date

@register(Date)
class DateAdmin(ModelAdmin):
    list_display = ('date_1', 'date_2', 'date_3', 'date_4', )
    sortable = ('date_1', 'date_2', 'date_3', 'date_4', )
    fieldsets = (
        (_('Date & Time'), {'fields': ('date_1', 'date_2', 'date_3', 'date_4', )}),
    )

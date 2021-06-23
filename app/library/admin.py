from django.contrib import admin
from admin.admin import UserAdmin
from admin import ModelAdmin
from django.utils.translation import gettext as _
from admin import register

# Register your models here.
from .models import (Catalog,Member,Account,Library,Book,Author)


from .forms import CatalogForm
@register(Catalog)
class CatalogAdmin(ModelAdmin):
   list_display = ('discount', )
   sortable = ('discount', )
   fieldsets = (
     (_('Chars'), {'fields': ('discount', )}),
     (_('Relationships'), {'fields': ('book_set', )}),
  )
   form = CatalogForm


from .forms import MemberForm
@register(Member)
class MemberAdmin(ModelAdmin):
   list_display = ('name', )
   sortable = ('name', )
   fieldsets = (
     (_('Chars'), {'fields': ('name', )}),
     (_('Relationships'), {'fields': ('account_ref', )}),
  )
   form = MemberForm


from .forms import AccountForm
@register(Account)
class AccountAdmin(ModelAdmin):
   list_display = ('number', 'opened', 'state', )
   sortable = ('number', 'opened', 'state', )
   fieldsets = (
     (_('Numbers'), {'fields': ('number', )}),
     (_('Date & Time'), {'fields': ('opened', )}),
     (_('Enumerations'), {'fields': ('state', )}),
     (_('Relationships'), {'fields': ('member', 'book_set', )}),
  )
   form = AccountForm


from .forms import LibraryForm
@register(Library)
class LibraryAdmin(ModelAdmin):
   list_display = ('city', 'country', 'name', )
   sortable = ('city', 'country', 'name', )
   fieldsets = (
     (_('Chars'), {'fields': ('city', 'country', 'name', )}),
     (_('Relationships'), {'fields': ('book_set', )}),
  )
   form = LibraryForm


from .forms import BookForm
@register(Book)
class BookAdmin(ModelAdmin):
   list_display = ('format', 'isbn', 'language_acr', 'name', 'price', 'publication_date', 'publisher', 'subject', )
   sortable = ('format', 'isbn', 'language_acr', 'name', 'price', 'publication_date', 'publisher', 'subject', )
   fieldsets = (
     (_('Chars'), {'fields': ('isbn', 'language_acr', 'name', 'publisher', 'subject', )}),
     (_('Numbers'), {'fields': ('price', )}),
     (_('Date & Time'), {'fields': ('publication_date', )}),
     (_('Enumerations'), {'fields': ('format', )}),
     (_('Relationships'), {'fields': ('catalog', 'library', 'account', 'author_set', )}),
  )
   form = BookForm


@register(Author)
class AuthorAdmin(ModelAdmin):
   list_display = ('biography', 'birth_date', 'name', )
   sortable = ('biography', 'birth_date', 'name', )
   fieldsets = (
     (_('Chars'), {'fields': ('name', )}),
     (_('Texts'), {'fields': ('biography', )}),
     (_('Date & Time'), {'fields': ('birth_date', )}),
     (_('Relationships'), {'fields': ('book', )}),
  )
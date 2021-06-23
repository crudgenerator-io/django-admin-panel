from django import forms
from django.contrib import admin

# Create your forms here.
from .models import (Catalog,Member,Account,Library,Book,Author)



class CatalogForm(forms.ModelForm):
    book_set = forms.ModelMultipleChoiceField(queryset=Book.objects.all())

    class Meta:
        model = Catalog
        exclude = ()
    def get_initial_for_field(self, field, field_name):
        if field_name == 'book_set':
            try:
                return self.instance.book_set.all()
            except ValueError:
                pass
        return super().get_initial_for_field(field, field_name)
    def save(self, commit=True):
        if 'book_set' in self.changed_data:
            updated_links = self.cleaned_data['book_set']
            prev_links = self.instance.book_set.all()
            for prev_link in prev_links:
                if prev_link not in updated_links:
                    prev_link.delete()
            self.instance.save()
            self.instance.book_set.set(updated_links)
        return super().save(commit)

class MemberForm(forms.ModelForm):
    account_ref = forms.ModelChoiceField(queryset=Account.objects.all(), required=False, blank=True, help_text='Note: Removing or changing this connection will cause currently selected entity to be removed')

    class Meta:
        model = Member
        exclude = ()
    def get_initial_for_field(self, field, field_name):
        if field_name == 'account_ref':
            try:
                return self.instance.account
            except self._meta.model.account.RelatedObjectDoesNotExist:
                pass
        return super().get_initial_for_field(field, field_name)
    def save(self, commit=True):
        if 'account_ref' in self.changed_data:
            new_link = self.cleaned_data['account_ref']
            if new_link:
                try:
                    self.instance.account.delete()
                except self._meta.model.account.RelatedObjectDoesNotExist:
                    pass
                self.instance.account = new_link
                self.instance.save()
                new_link.member = self.instance
                new_link.save()
            else:
                self.instance.account.delete()
        return super().save(commit)

class AccountForm(forms.ModelForm):
    book_set = forms.ModelMultipleChoiceField(queryset=Book.objects.all(), required=False, blank=True)

    class Meta:
        model = Account
        exclude = ()
    def get_initial_for_field(self, field, field_name):
        if field_name == 'book_set':
            return self.instance.book_set.all()
        return super().get_initial_for_field(field, field_name)
    def save(self, commit=True):
        if 'book_set' in self.changed_data:
            updated_links = self.cleaned_data['book_set']
            for existing_link in self.instance.book_set.all():
                if existing_link not in updated_links:
                    self.instance.book_set.remove(existing_link)
            for updated_link in updated_links:
                try:
                    if updated_link.account and updated_link.account != self:
                        updated_link.account = None
                        updated_link.save()
                except Account.DoesNotExist:
                    pass
            self.instance.save()
            self.instance.book_set.set(updated_links)
        return super().save(commit)

class LibraryForm(forms.ModelForm):
    book_set = forms.ModelMultipleChoiceField(queryset=Book.objects.all(), required=False, blank=True, help_text='Note: Unselecting any of the currently selected entities will cause corresponding entity/ies to be removed.')

    class Meta:
        model = Library
        exclude = ()
    def get_initial_for_field(self, field, field_name):
        if field_name == 'book_set':
            return self.instance.book_set.all()
        return super().get_initial_for_field(field, field_name)
    def save(self, commit=True):
        if 'book_set' in self.changed_data:
            updated_links = self.cleaned_data['book_set']
            for existing_link in self.instance.book_set.all():
                if existing_link not in updated_links:
                    existing_link.delete()
            self.instance.save()
            self.instance.book_set.set(updated_links)
        return super().save(commit)

class BookForm(forms.ModelForm):
    author_set = forms.ModelMultipleChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Book
        exclude = ()
    def get_initial_for_field(self, field, field_name):
        if field_name == 'author_set':
            try:
                return self.instance.author_set.all()
            except ValueError:
                pass
        return super().get_initial_for_field(field, field_name)
    def save(self, commit=True):
        if 'author_set' in self.changed_data:
            updated_links = self.cleaned_data['author_set']
            prev_links = self.instance.author_set.all()
            for prev_link in prev_links:
                if prev_link not in updated_links:
                    prev_link.delete()
            self.instance.save()
            self.instance.author_set.set(updated_links)
        return super().save(commit)


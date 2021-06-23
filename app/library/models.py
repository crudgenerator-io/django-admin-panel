from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, localtime
from datetime import datetime, date, time

# Create your models here.


class Catalog(models.Model):
    discount = models.CharField(max_length=3, default='10%')



class Member(models.Model):
    name = models.CharField(max_length=255)



class Account(models.Model):
    number = models.IntegerField(unique=True)
    opened = models.DateTimeField()
    state = models.CharField(max_length=6, choices=[('ACTIVE', 'active'), ('FROZEN', 'frozen'), ('CLOSED', 'closed')], default='ACTIVE')
    member = models.OneToOneField(Member, on_delete=models.CASCADE)



class Library(models.Model):
    city = models.CharField(max_length=85)
    country = models.CharField(max_length=56)
    name = models.CharField(max_length=150)



class Book(models.Model):
    format = models.CharField(max_length=9, choices=[('PAPERBACK', 'paperback'), ('HARDCOVER', 'hardcover'), ('AUDIOBOOK', 'audiobook'), ('AUDIO CD', 'audio cd'), ('MP3 CD', 'mp3 cd'), ('PDF', 'pdf')])
    isbn = models.CharField(max_length=1, unique=True)
    language_acr = models.CharField(max_length=3)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=True, blank=True)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    catalog = models.ManyToManyField(Catalog, blank=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)



class Author(models.Model):
    biography = models.TextField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    book = models.ManyToManyField(Book, blank=True)


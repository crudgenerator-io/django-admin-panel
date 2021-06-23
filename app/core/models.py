from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import datetime, date, time

# Create your models here.

class User(AbstractUser):
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=12)
    is_privileged_associate = models.BooleanField(default=False)
    created = models.DateField(default=now)
    deletion_scheduled = models.DateTimeField(default=now)
    activation_time = models.TimeField(default=now)
    profile_picture = models.FileField(upload_to="media/employee/profile_pictures", null=False, blank=False)
    times_accessed_platform_anonymously = models.IntegerField(default=0)
    info = models.TextField(null=True, blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)
    type = models.CharField(
        max_length=255,
        choices=[
            ("REGULAR", "Regular"),
            ("PRIVILEGED", "Privileged"),
            ("BLACKLISTED", "Blacklisted")
        ],
        default="REGULAR"
    )


class EmptyClass (models.Model):
    pass


class Text (models.Model):
    text_1 = models.TextField(max_length=156)
    text_2 = models.TextField(default='initial ?', null=True, blank=True)
    text_3 = models.TextField(help_text="This is help text specified in the model")



class Decimal (models.Model):
    dec_1 = models.DecimalField(decimal_places=2, max_digits=6, default=-222.22, unique=True)
    dec_2 = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=True, blank=True)
    dec_3 = models.DecimalField(decimal_places=2, max_digits=2, default=.99, null=True, blank=True, help_text="This is help text specified in the model")



class Enumeration (models.Model):
    e1 = models.CharField(max_length=255, choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], null=True, blank=True)
    e2 = models.CharField(max_length=255, default='enum1 val', choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], blank=False, null=False)
    e3 = models.CharField(max_length=255, default='enum3 val', choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], null=True, blank=True, help_text="This is help text specified in the model")



class Time (models.Model):
    time_1 = models.TimeField(default=time.fromisoformat("00:30"), unique=True)
    time_2 = models.TimeField(default=time.fromisoformat("13:31"), null=True, blank=True)
    time_3 = models.TimeField(null=True, blank=True)
    time_4 = models.TimeField(help_text="This is help text specified in the model")



class File (models.Model):
    f1 = models.FileField()
    f2 = models.FileField(null=True, blank=True)
    f3 = models.FileField(help_text="This is help text specified in the model")



class Char (models.Model):
    char_1 = models.CharField(max_length=255, default='This is default text', unique=True)
    char_2 = models.CharField(max_length=255, null=True, blank=True)
    char_3 = models.CharField(max_length=255, null=True, blank=True)
    char_4 = models.CharField(max_length=5, unique=True)
    char_5 = models.CharField(max_length=5, help_text="This is help text specified in the model")



class Boolean (models.Model):
    bool_1 = models.BooleanField(default=True)
    bool_2 = models.BooleanField(default=False)
    bool_3 = models.BooleanField(help_text="This is help text specified in the model")



class Datetime (models.Model):
    dt_1 = models.DateTimeField(null=True, blank=True)
    dt_2 = models.DateTimeField(default=datetime.fromisoformat("2021-05-05 00:30"))
    dt_3 = models.DateTimeField()



class Integer (models.Model):
    int_1 = models.IntegerField(default=35)
    int_2 = models.IntegerField(null=True, blank=True, unique=True)
    int_3 = models.IntegerField(help_text="This is help text specified in the model")


class Date (models.Model):
    date_1 = models.DateField(null=True, blank=True)
    date_2 = models.DateField(null=True, blank=True)
    date_3 = models.DateField(default=date.fromisoformat("2021-05-07"))
    date_4 = models.DateField(unique=True, help_text="This is help text specified in the model")

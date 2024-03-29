# Generated by Django 3.1.5 on 2021-06-09 01:21

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boolean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bool_1', models.BooleanField(default=True)),
                ('bool_2', models.BooleanField(default=False)),
                ('bool_3', models.BooleanField(help_text='This is help text specified in the model')),
            ],
        ),
        migrations.CreateModel(
            name='Char',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_1', models.CharField(default='This is default text', max_length=255, unique=True)),
                ('char_2', models.CharField(blank=True, max_length=255, null=True)),
                ('char_3', models.CharField(blank=True, max_length=255, null=True)),
                ('char_4', models.CharField(max_length=5, unique=True)),
                ('char_5', models.CharField(help_text='This is help text specified in the model', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_1', models.DateField(blank=True, null=True)),
                ('date_2', models.DateField(blank=True, null=True)),
                ('date_3', models.DateField(default=datetime.date(2021, 5, 7))),
                ('date_4', models.DateField(help_text='This is help text specified in the model', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Datetime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_1', models.DateTimeField(blank=True, null=True)),
                ('dt_2', models.DateTimeField(default=datetime.datetime(2021, 5, 5, 0, 30))),
                ('dt_3', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Decimal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec_1', models.DecimalField(decimal_places=2, default=-222.22, max_digits=6, unique=True)),
                ('dec_2', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('dec_3', models.DecimalField(blank=True, decimal_places=2, default=0.99, help_text='This is help text specified in the model', max_digits=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmptyClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Enumeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e1', models.CharField(blank=True, choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], max_length=255, null=True)),
                ('e2', models.CharField(choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], default='enum1 val', max_length=255)),
                ('e3', models.CharField(blank=True, choices=[('ENUM1 VAL', 'Enum1 Val'), ('ENUM2 VAL', 'Enum2 Val'), ('ENUM3 VAL', 'Enum3 Val'), ('ENUM4 VAL', 'Enum4 Val')], default='enum3 val', help_text='This is help text specified in the model', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f1', models.FileField(upload_to='')),
                ('f2', models.FileField(blank=True, null=True, upload_to='')),
                ('f3', models.FileField(help_text='This is help text specified in the model', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Integer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_1', models.IntegerField(default=35)),
                ('int_2', models.IntegerField(blank=True, null=True, unique=True)),
                ('int_3', models.IntegerField(help_text='This is help text specified in the model')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_1', models.TextField(max_length=156)),
                ('text_2', models.TextField(blank=True, default='initial ?', null=True)),
                ('text_3', models.TextField(help_text='This is help text specified in the model')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_1', models.TimeField(default=datetime.time(0, 30), unique=True)),
                ('time_2', models.TimeField(blank=True, default=datetime.time(13, 31), null=True)),
                ('time_3', models.TimeField(blank=True, null=True)),
                ('time_4', models.TimeField(help_text='This is help text specified in the model')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('state', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=12)),
                ('is_privileged_associate', models.BooleanField(default=False)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('deletion_scheduled', models.DateTimeField(default=django.utils.timezone.now)),
                ('activation_time', models.TimeField(default=django.utils.timezone.now)),
                ('profile_picture', models.FileField(upload_to='media/employee/profile_pictures')),
                ('times_accessed_platform_anonymously', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('type', models.CharField(choices=[('REGULAR', 'Regular'), ('PRIVILEGED', 'Privileged'), ('BLACKLISTED', 'Blacklisted')], default='REGULAR', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-07 01:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import django_resized.forms
import packages.integerId
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('contact_request_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('testimonial_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('rating', models.PositiveIntegerField(default=5)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=60, null=True)),
                ('photo', django_resized.forms.ResizedImageField(crop=None, default='media/user.jpg', force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to='users/')),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_user', models.BooleanField(default=False)),
                ('is_worker', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('bio', django_ckeditor_5.fields.CKEditor5Field(blank=True, default='Hi there,...', max_length=200)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('portfolio_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('before_image', models.ImageField(upload_to='portfolio/before/')),
                ('after_image', models.ImageField(upload_to='portfolio/after/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='portfolios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Residential', 'Residential'), ('Commercial', 'Commercial'), ('Industrial', 'Industrial'), ('Historical', 'Historical')], max_length=20)),
                ('image', models.ImageField(upload_to='services/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EstimateRequest',
            fields=[
                ('estimate_id', packages.integerId.IntegerIDField(default=packages.integerId.uniqueID, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('details', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed'), ('Approved', 'Approved')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estimates', to='paint.service')),
            ],
        ),
    ]

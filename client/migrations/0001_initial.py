# Generated by Django 3.1.14 on 2024-07-13 08:09

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUser',
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
                ('role', models.CharField(choices=[('CL', 'Client'), ('TH', 'Therapist')], max_length=2)),
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
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('age', models.IntegerField(default=1)),
                ('description', models.TextField(blank=True, default='', max_length=255, null=True)),
                ('condition', models.CharField(choices=[('Celebral Palsy', 'Celebral Palsy'), ('Autism', 'Autism'), ('Down Syndrome', 'Down Syndrome'), ('ADHD', 'ADHD'), ('Hydrocephalus', 'Hydrocephalus'), ('Epilepsy', 'Epilepsy'), ('Developmental Delay', 'Developmental Delay'), ('Learning Disability', 'Learning Disability'), ('Intellectual Disability', 'Intellectual Disability'), ('Hearing Impairment', 'Hearing Impairment'), ('Visual Impairment', 'Visual Impairment'), ('Speech and Language Disorder', 'Speech and Language Disorder'), ('Physical Disability', 'Physical Disability'), ('Mental Health Disorder', 'Mental Health Disorder'), ('Multiple Disabilities', 'Multiple Disabilities'), ('Other', 'Other')], default='Other', max_length=255)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='client.clientuser')),
            ],
        ),
        migrations.CreateModel(
            name='TherapistProfile',
            fields=[
                ('experience', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('occupation', models.CharField(choices=[('Occupational Therapist', 'Occupational Therapist'), ('Physiotherapist', 'Physiotherapist'), ('Speech Therapist', 'Speech Therapist'), ('Special Education Teacher', 'Special Education Teacher'), ('Psychologist', 'Psychologist'), ('Psychiatrist', 'Psychiatrist'), ('Counselor', 'Counselor'), ('Social Worker', 'Social Worker'), ('ABA Therapist', 'ABA Therapist'), ('Music Therapist', 'Music Therapist'), ('Art Therapist', 'Art Therapist'), ('Dance Therapist', 'Dance Therapist'), ('Recreational Therapist', 'Recreational Therapist'), ('Nutritionist', 'Nutritionist'), ('Other', 'Other')], default='Other', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('location', models.CharField(default='', max_length=100)),
                ('therapist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='client.clientuser')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('client.clientuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
            ],
            options={
                'verbose_name': 'Therapist',
                'verbose_name_plural': 'Therapists',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('client.clientuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

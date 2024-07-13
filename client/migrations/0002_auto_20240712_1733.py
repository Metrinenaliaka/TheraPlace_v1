# Generated by Django 3.1.14 on 2024-07-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofile',
            name='age',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='description',
            field=models.TextField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='role',
            field=models.CharField(choices=[('CL', 'Client'), ('TH', 'Therapist')], default=None, max_length=2),
        ),
        migrations.AlterField(
            model_name='therapistprofile',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='therapistprofile',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='therapistprofile',
            name='occupation',
            field=models.CharField(choices=[('Occupational Therapist', 'Occupational Therapist'), ('Physiotherapist', 'Physiotherapist'), ('Speech Therapist', 'Speech Therapist'), ('Special Education Teacher', 'Special Education Teacher'), ('Psychologist', 'Psychologist'), ('Psychiatrist', 'Psychiatrist'), ('Counselor', 'Counselor'), ('Social Worker', 'Social Worker'), ('ABA Therapist', 'ABA Therapist'), ('Music Therapist', 'Music Therapist'), ('Art Therapist', 'Art Therapist'), ('Dance Therapist', 'Dance Therapist'), ('Recreational Therapist', 'Recreational Therapist'), ('Nutritionist', 'Nutritionist'), ('Other', 'Other')], default='Other', max_length=100),
        ),
        migrations.AlterField(
            model_name='therapistprofile',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

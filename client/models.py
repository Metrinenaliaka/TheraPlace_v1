from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver

class ClientUser(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'CL', 'Client'
        THERA = 'TH', 'Therapist'
    # base_role = Role.CLIENT
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            # self.role = self.base_role
            return super().save(*args, **kwargs)

class Client(ClientUser):
    base_role = ClientUser.Role.CLIENT

    class Meta:
        proxy = True
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class ClientProfile(models.Model):
    COND_CATEGORIES = [
        ('Celebral Palsy', 'Celebral Palsy'),
        ('Autism', 'Autism'),
        ('Down Syndrome', 'Down Syndrome'),
        ('ADHD', 'ADHD'),
        ('Hydrocephalus', 'Hydrocephalus'),
        ('Epilepsy', 'Epilepsy'),
        ('Developmental Delay', 'Developmental Delay'),
        ('Learning Disability', 'Learning Disability'),
        ('Intellectual Disability', 'Intellectual Disability'),
        ('Hearing Impairment', 'Hearing Impairment'),
        ('Visual Impairment', 'Visual Impairment'),
        ('Speech and Language Disorder', 'Speech and Language Disorder'),
        ('Physical Disability', 'Physical Disability'),
        ('Mental Health Disorder', 'Mental Health Disorder'),
        ('Multiple Disabilities', 'Multiple Disabilities'),
        ('Other', 'Other'),
    ]
    age = models.IntegerField(default=1)
    description = models.TextField(max_length=255, blank=True, null=True, default='')
    condition = models.CharField(max_length=255, choices=COND_CATEGORIES, default='Other')
    client = models.OneToOneField(ClientUser, on_delete=models.CASCADE)                

class Therapist(ClientUser):
    base_role = ClientUser.Role.THERA

    class Meta:
        proxy = True
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapists'

    
class TherapistProfile(models.Model):

    OCC_CHOICES = [
        ('Occupational Therapist', 'Occupational Therapist'),
        ('Physiotherapist', 'Physiotherapist'),
        ('Speech Therapist', 'Speech Therapist'),
        ('Special Education Teacher', 'Special Education Teacher'),
        ('Psychologist', 'Psychologist'),
        ('Psychiatrist', 'Psychiatrist'),
        ('Counselor', 'Counselor'),
        ('Social Worker', 'Social Worker'),
        ('ABA Therapist', 'ABA Therapist'),
        ('Music Therapist', 'Music Therapist'),
        ('Art Therapist', 'Art Therapist'),
        ('Dance Therapist', 'Dance Therapist'),
        ('Recreational Therapist', 'Recreational Therapist'),
        ('Nutritionist', 'Nutritionist'),
        ('Other', 'Other'),
    ]
    experience = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True, default='')
    occupation = models.CharField(max_length=100, choices=OCC_CHOICES, default='Other')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=100, default='')
    therapist = models.OneToOneField(ClientUser, on_delete=models.CASCADE)


@receiver(pre_save, sender=ClientUser)
def create_user_profile(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created:
        if instance.role == ClientUser.Role.CLIENT:
            ClientProfile.objects.create(client=instance)
        elif instance.role == ClientUser.Role.THERA:
            TherapistProfile.objects.create(therapist=instance)
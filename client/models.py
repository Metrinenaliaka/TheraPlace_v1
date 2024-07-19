"""
This module contains the models for the client app
"""
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

class ClientUser(AbstractUser):
    """
    This class is a model for the user
    """
    class Role(models.TextChoices):
        """
        This class defines the roles that a user can have
        """
        CLIENT = 'CL', 'Client'
        THERA = 'TH', 'Therapist'
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
    )

    def save(self, *args, **kwargs):
        """
        This function saves the user
        """
        if not self.pk:
            # self.role = self.base_role
            return super().save(*args, **kwargs)

class Client(ClientUser):
    """
    This class is a proxy model for the client user
    """
    base_role = ClientUser.Role.CLIENT

    class Meta:
        """
        This class defines the metadata for the model
        """
        proxy = True
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class ClientProfile(models.Model):
    """
    This class is a model for the client profile
    """
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
    client = models.OneToOneField(ClientUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        """
        This function returns the username of the client
        """
        return self.client.username            

class Therapist(ClientUser):
    """
    This class is a proxy model for the therapist user
    """
    base_role = ClientUser.Role.THERA
    class Meta:
        """
        This class defines the metadata for the model
        """
        proxy = True
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapists'

    
class TherapistProfile(models.Model):
    """
    This class is a model for the therapist profile
    """

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
    therapist = models.OneToOneField(ClientUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        """
        This function returns the username of the client
        """
        return self.therapist.username
    
    def respond_to_appointment(self, appointment_id, response):
        appointment = Appointments.objects.get(id=appointment_id)
        if response == 'approve':
            appointment.status = 'Approved'
            # Send email to client
            client_email_subject = 'Appointment Approved'
            client_email_message = f'Your appointment on {appointment.date} at {appointment.time} has been approved.'
            send_mail(client_email_subject, client_email_message, settings.DEFAULT_FROM_EMAIL, [appointment.client.client.email])
        elif response == 'decline':
            appointment.status = 'Declined'
            # Send email to client
            client_email_subject = 'Appointment Declined'
            client_email_message = f'Your appointment on {appointment.date} at {appointment.time} has been declined.'
            send_mail(client_email_subject, client_email_message, settings.DEFAULT_FROM_EMAIL, [appointment.client.client.email])
        appointment.save()
class Appointments(models.Model):
    """
    setting up models for client appointments
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    therapist = models.ForeignKey(TherapistProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(max_length=255, blank=True, null=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.client.client.username} with {self.therapist.therapist.username} on {self.date} at {self.time}"


@receiver(pre_save, sender=ClientUser)
def create_user_profile(sender, instance, **kwargs):
    """
    This function creates a profile for the user before user is saved
    """
    created = kwargs.get('created')
    if created:
        if instance.role == ClientUser.Role.CLIENT:
            ClientProfile.objects.create(client=instance)
        elif instance.role == ClientUser.Role.THERA:
            TherapistProfile.objects.create(therapist=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    creates a token for users as they are saved
    """
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Appointments)
def send_appointment_email(sender, instance, created, **kwargs):
    """
    post save to send client booking email
    """
    if created:
        # Construct email message
        subject = 'Appointment Scheduled'
        message = f'Your appointment on {instance.date} at {instance.time} with {instance.therapist.therapist.username} has been scheduled and is pending approval.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.client.client.email

        # Send email
        send_mail(subject, message, from_email, [to_email])

@receiver(post_save, sender=Appointments)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.status != 'Pending':
        if instance.status == 'Approved':
            # Send approval email to client
            subject = 'Appointment Approved'
            message = f'Your appointment on {instance.date} at {instance.time} with {instance.therapist.therapist.username} has been approved.'
        elif instance.status == 'Declined':
            # Send decline email to client
            subject = 'Appointment Declined'
            message = f'Your appointment on {instance.date} at {instance.time} with {instance.therapist.therapist.username} has been declined.'
        
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.client.client.email

        # Send email
        send_mail(subject, message, from_email, [to_email])
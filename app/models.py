"""
model for Users
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model for users
    """
    USER_CATEGORIES = [
        ('client', 'Client'),
        ('therapist', 'Therapist'),
    ]
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=USER_CATEGORIES)

    def __str__(self):
        return self.user.username


class ClientProfile(models.Model):
    """
    Additional details for clients
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
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100, choices=COND_CATEGORIES)
    age = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} (Client)"

class TherapistProfile(models.Model):
    """
    Additional details for therapists
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
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    experience = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, choices=OCC_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.profile.user.username} (Therapist)"
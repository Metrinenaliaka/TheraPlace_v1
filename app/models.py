"""
custom models for my users it extends the AbstractUser model
"""
import hashlib
from django.db import models
from django.contrib.auth.hashers import make_password
from PIL import Image

class Base(models.Model):
    """
    custom user model for my users
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.CharField(max_length=255)
    description = models.TextField()
    password1 = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        """
        defines my save, hashing my password before saving
        """
        self.email = hashlib.sha256(self.email.encode()).hexdigest()
        self.phone = hashlib.sha256(self.phone.encode()).hexdigest()
        self.password1 = make_password(self.password1)
        self.password2 = make_password(self.password2)
        super(Base, self).save(*args, **kwargs)

    class Meta:
        """
        metadata for the model
        """
        abstract = True

class Client(Base):
    """
    custom user model for my clients
    """
    condition = models.CharField(max_length=255)
    age = models.IntegerField()

    def save(self, *args, **kwargs):
        """
        generating image thumbnail
        """
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Therapist(Base):
    """
    custom user model for my therapists
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    experience = models.IntegerField()
    qualification = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        generating image thumbnail
        """
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)


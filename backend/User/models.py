"""
User models module.

This module defines the models for the User application, including the UserProfile model.

Classes:
    UserProfile: Represents a user's profile, with fields for phone number and date of birth.

Functions:
    create_user_profile: Creates a UserProfile instance when a User is created.
    save_user_profile: Saves the UserProfile instance when a User is saved.

Signals:
    post_save: Receives the post_save signal from the User model to create or save the UserProfile instance.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    '''
    Model representing a user profile with fields for phone number and date of birth.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile instance when a User is created.

    This is a receiver for the post_save signal. If the User is newly created,
    it creates a UserProfile with the User instance as the user.

    Args:
        sender: The User model class.
        instance: The User instance that was just created.
        created: A boolean indicating whether the instance was created.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile instance when a User is saved.

    This is a receiver for the post_save signal. When a User is saved, it
    saves the UserProfile instance associated with the User instance.

    Args:
        sender: The User model class.
        instance: The User instance that was just saved.
    """
    instance.profile.save()

from localflavor.us.us_states import STATE_CHOICES
# STATE_CHOICES=()

from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


# Create your models here.
class ExtendUser(models.Model):
    r = models.OneToOneField(User, on_delete=models.CASCADE)
    # date_of_birth = models.DateField(null=True)

    '''
    In default User:

    username
    password
    email
    first_name
    last_name
    '''

    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.r.username
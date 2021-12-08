from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

import datetime
from django.urls import reverse

class User(AbstractUser):
    pass

#User.add_to_class('is_manager', models.BooleanField(default=False, verbose_name='role')


class Parking(models.Model):
    name = models.CharField(max_length=100)

class List_periods(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return 'hour: {}'.format(self.name)

class Booking_session(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    parking_lot = models.ForeignKey(Parking, on_delete= models.CASCADE)
    list_of_periods = models.ManyToManyField(List_periods, blank=True, related_name="hours_list")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True, related_name="user_del")
    updated_at = models.DateTimeField(blank=True, null=True,)
    updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True,related_name="user_upd")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'user: {}, parking_lot: {}'.format(self.user.username, self.parking_lot.name)


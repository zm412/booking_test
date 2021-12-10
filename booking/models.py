from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

import datetime
from django.urls import reverse

def get_periods_t(times):
    listT = []
    for t in list(range(times)):
        if(t < 10):
            listT.append('0%s' % t)
        else:
            listT.append('%s' % t)
    return listT


class User(AbstractUser):
    pass


class Parking(models.Model):
    name = models.CharField(max_length=100)


class List_periods(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return 'hour: {}'.format(self.name)


class Reservation_day(models.Model):
    name = models.CharField(max_length=8)
    parking_lot = models.ForeignKey(Parking, on_delete= models.CASCADE)
    list_of_periods = models.ManyToManyField(List_periods, blank=True, related_name="hours_list")

    def free_hours(self):
        listH = get_periods_t(24)
        list_of_free_hours = []
        for l in get_periods_t(24):
            try:
                self.hours_list.get(name=l)
            except List_periods.DoesNotExist:
                list_of_free_hours.append(l)
        return list_of_free_hours


    def is_not_full(self):
        listH = get_periods_t(24)
        flag = false
        for l in get_periods_t(24):
            try:
                List_periods.object.get(name=l)
            except List_periods.DoesNotExist:
                flag = true
                break
        return flag

    def __str__(self):
        return 'day: {}'.format(self.name)


class Booking_session(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    reservation_day = models.ManyToManyField(Reservation_day, blank=True, related_name="days_list")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True, related_name="user_del")
    updated_at = models.DateTimeField(blank=True, null=True,)
    updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True,related_name="user_upd")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'user: {}'.format(self.user.username)


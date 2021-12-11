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
    parking_name = models.CharField(max_length=100)

    def __str__(self):
        return 'parking_name: {}'.format(self.parking_name)



class Reservation_day(models.Model):
    day_name = models.CharField(max_length=10)
    users_list = models.ManyToManyField(User, blank=True, related_name="users_days")
    is_active = models.BooleanField(default=True)

    def serialize(self):
        return {
            'day_name': self.day_name,
            'hours': [d for d in self.day_connection.all()]
        }


class Booking_session(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,blank=True)
    days_list = models.ManyToManyField(Reservation_day, blank=True, related_name="book_days")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True, related_name="user_del")
    updated_at = models.DateTimeField(blank=True, null=True,)
    updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True,related_name="user_upd")


class List_periods(models.Model):
    hour_name = models.CharField(max_length=2)
    day = models.ForeignKey(Reservation_day, on_delete= models.CASCADE,blank=True, related_name="day_connection")
    session = models.ForeignKey(Booking_session, on_delete= models.CASCADE,blank=True, related_name="booking_connection")
    parking_lot = models.ForeignKey(Parking, on_delete= models.CASCADE)

    def make_selection_by_day(self, user):
        querySet = Reservation_day.objects.all()
        selection = List_periods.objects.filter(day=self.day, session__user=user)
        print(selection, 'selection')

    def __str__(self):
        return 'hour: {}, day: {}'.format(self.hour_name, self.day.day_name)

    def serialize(self):
        return {
            'hour': self.hour_name,
            'day': self.day.day_name,
            'parking_lot': self.parking_lot.id,
            'parking_lot_name': self.parking_lot.parking_name,
            'user_name': self.session.user.username,
            'user_id': self.session.user.id
        }










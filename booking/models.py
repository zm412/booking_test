from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

import datetime
from django.urls import reverse

class User(AbstractUser):
    pass


class Parking(models.Model):
    parking_name = models.CharField(max_length=100)

    def __str__(self):
        return 'parking_name: {}'.format(self.parking_name)



class Reservation_day(models.Model):
    day_name = models.CharField(max_length=10)
    parking_lot = models.ForeignKey(Parking, on_delete= models.CASCADE,related_name='session_parking' )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True, related_name="user_del")
    updated_at = models.DateTimeField(blank=True, null=True,)
    updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True,related_name="user_upd")

    def __str__(self):
        return 'day: {}, day_id: {}, parking_lot:{}, created_at: {},  deleted_by'.format(
            self.day_name, self.id, self.parking_lot.parking_name, self.created_at, self.deleted_by)


    def serialize(self):
        return {
            'day': self.day_name,
            'hours': [d.serialize() for d in self.day_connection.all()],
            'parking_lot_id': self.parking_lot.id,
            'parking_lot_name': self.parking_lot.parking_name,
            'created_at': self.created_at,
            'deleted_by': self.deleted_by,
            'ubpdated_at': self.created_at,
            'ubpdated_by': self.deleted_by,
        }


    def turn_to_date(self):
        d = str(self.day_name).split('.')
        date_result = datetime.date(int(d[2]), int(d[1]), int(d[0]))
        return date_result > datetime.date.today()

    def filter_by_user(self, user):
        return self.day_connection.filter(user = user)





class List_periods(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,blank=True)
    hour_name = models.CharField(max_length=2)
    day = models.ForeignKey(Reservation_day, on_delete= models.CASCADE,blank=True, related_name="day_connection")

    def clean_date(self):
        return self.day.turn_to_date()

    def __str__(self):
        return 'hour: {}, day: {}'.format(self.hour_name, self.day.day_name)

    def serialize(self):
        return {
            'hour': self.hour_name,
            'day': self.day.day_name,
            'user_name': self.user.username,
            'user_id': self.user.id,
        }










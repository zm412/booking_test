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


class Reservation_day(models.Model):
    name = models.CharField(max_length=10)
    parking_lot = models.ForeignKey(Parking, on_delete= models.CASCADE)
    is_active = models.BooleanField(default=True)

    def turn_to_date(self):
        d = self.name.split('.')
        date_result = datetime(d[2], d[1], d[0])
        if(date_result < datetime.now()):
            self.is_active = False
            self.save()

    def get_users_list(self):
        querySet = self.booking_sess.all()
        return [{'id': b.user.id,'name': b.user.username, "created_at": b.created_at } for b in querySet]



    def serialize(self):
        return {
            'date': self.name,
            'user': self.get_users_list(),
        }

    def free_hours(self):
        listH = get_periods_t(24)
        list_of_free_hours = []
        for l in get_periods_t(24):
            try:
                self.days_list.get(name=l)
            except List_periods.DoesNotExist:
                list_of_free_hours.append(l)
        return list_of_free_hours

class List_periods(models.Model):
    name = models.CharField(max_length=2)
    day = models.ForeignKey(Reservation_day, on_delete= models.CASCADE,blank=True, related_name="day_conn")

    def __str__(self):
        return 'hour: {}'.format(self.name)

    def get_booking_sess_info(self):
        querySet = Booking_session.objects.filter(reservation_day=self.day,reservation_day__day_conn = self)
        return [{'username': b.user.username, 'user_id': b.user.id, 'created_at': b.created_at} for b in querySet]


    def serialize(self):
        return {
            'hour': self.name,
            'day': self.day.name,
            'parking_lot': self.day.parking_lot.id,
            'parking_lot_name': self.day.parking_lot.name,
            'user': self.get_booking_sess_info()
        }


class Booking_session(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    reservation_day = models.ManyToManyField(Reservation_day, blank=True, related_name="booking_sess")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True, related_name="user_del")
    updated_at = models.DateTimeField(blank=True, null=True,)
    updated_by = models.ForeignKey(User, on_delete = models.DO_NOTHING, blank=True, null=True,related_name="user_upd")

    def __str__(self):
        return 'user: {}'.format(self.user.username)

    def get_hours_ses(self):
        querySet = self.reservation_day.all()
        return [q for q in querySet]



    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'booked': self.crated_at,
            'days': self.get_days_list(),
        }


















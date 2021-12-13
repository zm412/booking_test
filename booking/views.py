import json
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Parking, List_periods, Reservation_day
from django import forms

def index(request):
    if request.user.is_authenticated:
        return render(request, "booking/index.html", {
            'parking': Parking.objects.all(),
        })
    else:
        return render(request, "booking/login.html")

def get_all_hours(request):
    all_hours = [b.serialize() for b  in Reservation_day.objects.all() if b.turn_to_date()==True]
    all_hours1 = [b.serialize() for b  in List_periods.objects.all() if b.clean_date()==True]
    filtered = [{
        'day_id': d.id,
        'day': d.day_name,
        'parking_lot_id': d.parking_lot.id,
        'parking_lot_name': d.parking_lot.parking_name,
        'hours': [ p.serialize() for p in  d.filter_by_user(request.user)]
    } for d in Reservation_day.objects.all() if len( [ p.serialize() for p in  d.filter_by_user(request.user)] ) > 0]

    return JsonResponse({
        'bookings': all_hours,
        'filtered': filtered
        })

def manage_items(request):
    return render(request, "booking/add_parking.html")

def delete_reservation(request, day_id, lot_id):
    session = Reservation_day.objects.get(id=day_id)
    hours = session.day_connection.filter(user=request.user).delete()
    print(session, 'SESSSION')
    #session.delete()
    return HttpResponseRedirect(reverse("open_parking_lot", args=[ lot_id ]))

def update_reservation(request):
    print(request.body, 'POSTLKJLJ')
    if request.method == "POST":
        data = json.loads(request.body)
        day = Reservation_day.objects.get(id=data['day_id'])
        for d in data['hours']:
            if d in data['original']:
                continue
            else:
                period = List_periods.objects.create(user=request.user, hour_name=d, day=day)
                continue
        for p in data['original']:
            if p not in data['hours']:
                period = day.day_connection.get(hour_name=p)
                period.delete()

    return HttpResponseRedirect(reverse("open_parking_lot", args=[data['lot']]))



def save_hour(day_id, hour_name, user_for_book):
    day = Reservation_day.objects.get(id=day_id)
    period = List_periods.objects.create(user=user_for_book, hour_name=hour_name, day=day)
    day_x = Reservation_day.objects.get_or_create(day_name=c, parking_lot=parking_lot)




"""
        parking_lot = Parking.objects.get(id=data['parking_lot'])
        booking = Booking_session.objects.create(user=request.user)

        for c in data['dates_set']:
            day_x = Reservation_day.objects.get_or_create(day_name=c, parking_lot=parking_lot)
            request.user.users_days.add(day_x[0])
            day_x[0].book_days.add(booking)
            for t in data[c]:
                period = List_periods.objects.create(hour_name=t,
                                                     day=day_x[0],
                                                     session=booking
                                                     )
    return HttpResponseRedirect(reverse("open_parking_lot", args=[data['parking_lot']]))

    session = Booking_session.objects.get(id=session_id)
    session.update()
    return HttpResponseRedirect(reverse("open_parking_lot", args=[ lot_id ]))
"""

def add_parking_lot(request):
    if request.method == "POST":
        parking = Parking(parking_name=request.POST['name'])
        parking.save()
    return HttpResponseRedirect(reverse("index"))

def open_parking_lot(request, id_lot):
    parking = Parking.objects.get(id=id_lot)
    my_booking = [{
                'day_id': d.id,
                'day': d.day_name,
                 'parking_lot_id': d.parking_lot.id,
                'parking_lot_name': d.parking_lot.parking_name,
                'hours': [ p.serialize() for p in  d.filter_by_user(request.user)]
    } for d in Reservation_day.objects.all() if len( [ p.serialize() for p in  d.filter_by_user(request.user)] ) > 0]

    return render(request, "booking/book_page.html", {
            'parking_lot': id_lot,
            'parking_lot_name': parking.parking_name,
            'my_bookings': my_booking,
                                                      })


def book_parking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        parking_lot = Parking.objects.get(id=data['parking_lot'])
        for c in data['dates_set']:
            day_x = Reservation_day.objects.get_or_create(day_name=c, parking_lot=parking_lot)
            for t in data[c]:
                period = List_periods.objects.create(user=request.user, hour_name=t, day=day_x[0])
    return HttpResponseRedirect(reverse("open_parking_lot", args=[data['parking_lot']]))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "booking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "booking/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "booking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "booking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"), {'status': 'OK'})
    else:
        return render(request, "booking/register.html")

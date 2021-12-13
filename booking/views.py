import json
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Parking, List_periods, Booking_session, Reservation_day
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
    filtered = [{ 'day': d.day_name,
                 'parking_lot_id': d.parking_lot.id,
                 'session_id': [ s.serialize() for s in d.book_days.all() ],
                'parking_lot_name': d.parking_lot.parking_name,
                'hours': [ p.serialize() for p in  d.filter_by_user(request.user)]
                } for d in Reservation_day.objects.all()]
    my_booking = Booking_session.objects.filter(user=request.user)
    return JsonResponse({
        'bookings': all_hours,
        'my_bookings': [b.serialize() for b in my_booking],
        'filtered': filtered
        })

def manage_items(request):
    return render(request, "booking/add_parking.html")

def delete_reservation(request, session_id, lot_id):
    session = Booking_session.objects.get(id=session_id)
    session.delete()
    return HttpResponseRedirect(reverse("open_parking_lot", args=[ lot_id ]))

def update_reservation(request):
    print(request.body, 'POSTLKJLJ')
    if request.method == "POST":
        data = json.loads(request.body)

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

def change_queryset(queryset):
    listQ = {}
    for q in queryset:
        if q.day not in listQ:
            listQ.day = q.day
        else:
            pass

def open_parking_lot(request, id_lot):
    parking = Parking.objects.get(id=id_lot)
    my_book =  List_periods.objects.filter(session__user_id = request.user.id)
    my_booking = Reservation_day.objects.filter(users_list__id=request.user.id).distinct()
    my_booking2 = Booking_session.objects.filter(user=request.user)
    print(my_book, 'my_book')
    return render(request, "booking/book_page.html", {
            'parking_lot': id_lot,
            'parking_lot_name': parking.parking_name,
            'my_bookings': [b.serialize() for b in my_booking2],
                                                      })

def book_parking(request):
    if request.method == "POST":
        data = json.loads(request.body)

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

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
    print(Parking.objects.all())
    print(List_periods.objects.all())
    print(Booking_session.objects.all(), "BOOKINGS1")

    if request.user.is_authenticated:
        return render(request, "booking/index.html", {'parking': Parking.objects.all()})
    else:
        return render(request, "booking/login.html")

def get_all_hours(request):
    return JsonResponse({
            'bookings': [b.serialize() for b in List_periods.objects.filter(day__is_active=True)],
        })

def manage_items(request):
    print(List_periods.objects.all())
    return render(request, "booking/add_parking.html")

def add_parking_lot(request):
    print(request.POST)
    if request.method == "POST":
        parking = Parking(name=request.POST['name'])
        parking.save()
    return HttpResponseRedirect(reverse("index"))

def open_parking_lot(request, id_lot):
    return render(request, "booking/book_page.html", {'parking_lot': id_lot})



def book_parking(request):
    print(request.body, 'pOST')
    if request.method == "POST":
        data = json.loads(request.body)
        print(data, 'Data')

        parking_lot = Parking.objects.get(id=data['parking_lot'])
        booking = Booking_session.objects.create(user=request.user)

        for c in data['dates_set']:
            print(c, 'c')
            day_x = Reservation_day.objects.get_or_create(name=c, parking_lot=parking_lot)
            for t in data[c]:
                print(t, "TTTTTTTTTt")
                print(day_x, "dxxxxxxxxxxxxx")
                period = List_periods.objects.get_or_create(name=t, day=day_x[0])
                print(period, 'PERIOD')
        booking.reservation_day.add(day_x[0])
        print(Booking_session.objects.all(), "BOOKINGS")
    return render(request, "booking/index.html", {'parking': Parking.objects.all()})

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

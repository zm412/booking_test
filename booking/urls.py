
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("manage_items", views.manage_items, name="manage_items"),
    path("add_parking_lot", views.add_parking_lot, name="add_parking_lot"),
    path("book_parking/<int:id_lot>", views.book_parking, name="book_parking"),
    path("open_parking_lot/<int:id_lot>", views.open_parking_lot, name="open_parking_lot"),
]

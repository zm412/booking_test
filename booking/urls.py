
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("manage_items", views.manage_items, name="manage_items"),
    path("add_parking_lot", views.add_parking_lot, name="add_parking_lot"),
    path("delete_parking/<int:id_lot>", views.delete_parking, name="delete_parking"),
    path("change_parking_name/<int:id_lot>", views.change_parking_name, name="change_parking_name"),

    path("open_parking_lot/<int:id_lot>", views.open_parking_lot, name="open_parking_lot"),
    path("open_parking_lot/book_parking", views.book_parking, name="book_parking"),
    path("book_parking/", views.book_parking, name="book_parking"),
    path('delete_reservation/<int:day_id>/<int:lot_id>/<str:role>', views.delete_reservation, name="delete_reservation"),
    path('update_reservation/', views.update_reservation, name="update_reservation"),
    path("get_all_hours/", views.get_all_hours, name="get_all_hours"),

]


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import RoomList,BookingList,RoomDetailView,CancelBookingView,booked
app_name='hotel'
urlpatterns=[
    path('',RoomList,name="RoomList"),
    path('booking_list/',BookingList.as_view(),name="BookingList"),
    path('booking/cancel/<pk>',CancelBookingView.as_view(),name="CancelBookingView"),
    path('room/<str:category>',RoomDetailView.as_view(),name="RoomDetailView"),
    path('booked/',booked,name="booked")
]
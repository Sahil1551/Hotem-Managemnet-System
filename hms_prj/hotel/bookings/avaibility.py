import datetime
from hotel.models import Room,Bookings
def check_avaibility(room,check_in,check_out):
    avail_list=[]
    booking_list=Bookings.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in>check_out or booking.check_out<check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)            
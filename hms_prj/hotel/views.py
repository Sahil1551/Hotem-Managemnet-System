from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import ListView,FormView,View,DeleteView
from django.urls import reverse,reverse_lazy
from .models import Room,Bookings
from .forms import AvaibilityForm
from django.contrib import messages
from hotel.bookings.avaibility import check_avaibility 
def RoomList(request):
    room=Room.objects.all()[0]
    room_categories=dict(room.ROOM_CATEGORIES)
    
    room_values=room_categories.values()
    room_list=[]
    for room_category in room_categories:
        room=room_categories.get(room_category)
        room_url=reverse('hotel:RoomDetailView',kwargs={'category':room_category})
        room_list.append((room,room_url))
    context={
        "room_list":room_list
    }
    return render(request,'room_list.html',context)
class BookingList(ListView):
    model=Bookings
    def get_queryset(self,*args,**kwargs) :
        if self.request.user.is_staff:
            booking_list=Bookings.objects.all()
            return booking_list
        else:
            booking_list=Bookings.objects.filter(user=self.request.user)
            return booking_list   
class RoomDetailView(View):
    def get(self,request,*args,**kwargs):
        category=self.kwargs.get('category',None)
        room_list=Room.objects.filter(category=category)
        form=AvaibilityForm()
        if len(room_list)>0:
            room=room_list[0]
            room_category=dict(room.ROOM_CATEGORIES).get(room.category,None)
            context={
            'room_category': room_category,
            'form':form,
             }
            return render(request,'room_detail_view.html',context)
        else:
            return HttpResponse("Category Not Exist") 
    def post(self,request,*args,**kwargs):
        category=self.kwargs.get('category',None)
        room_list=Room.objects.filter(category=category)
        available_rooms=[]
        form=AvaibilityForm(self.request.POST)
        if form.is_valid():
            data=form.cleaned_data
        for room in room_list:
            if check_avaibility(room,data['check_in'],data['check_out']):
                available_rooms.append(room)
        if(len(available_rooms)>0):
            room=available_rooms[0]
            booking=Bookings.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
                )
            booking.save()
            return HttpResponse("booked")
        else:
            return HttpResponse("This Category Of rooms are booked")

class BookingView(FormView):
    form_class=AvaibilityForm
    template_name='avaibility_form.html'
    def form_valid(self, form):
        data=form.cleaned_data
        room_list=Room.objects.filter(category=data['room_category'])
        available_rooms=[]
        for room in room_list:
            if check_avaibility(room,data['check_in'],data['check_out']):
                available_rooms.append(room)
        if(len(available_rooms)>0):
            room=available_rooms[0]
            booking=Bookings.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
                )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse("This Category Of rooms are booked")
class CancelBookingView(DeleteView):
    model = Bookings
    template_name='booking_cancel_view.html'
    success_url=reverse_lazy('hotel:BookingList')
def booked(request):
    messages.success(request, 'Your message was successfully sent!')
    return render(request,'room_list.html')
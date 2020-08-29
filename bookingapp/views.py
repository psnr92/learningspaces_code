from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking
from .forms import AvailabilityForm
from bookingapp.booking_functions.availability import check_availability
from .filters import RaumFilter

# Create your views here.

# Erstellt eine Liste der Räume
class RoomList(ListView):
    model=Room


# Erstellt eine Liste aller Buchungen
# context filter wird für die Suchfunktion verwendet
class BookingList(ListView):
    model=Booking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RaumFilter(self.request.GET, queryset=self.get_queryset())
        return context

# Raumbuchungsfunktion & gleichzeitige Prüfung auf Raumverfügbarkeit
class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category=data['room_category'])
        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('Zeitslot für diese Art Raumkategorie bereits belegt. Bitte versuchen Sie einen anderen Zeitslot oder wählen Sie eine andere Raumkategorie.')


# Löschfunktion für Buchungen
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingList')
import django_filters

from .models import *

# Suchfunktion nach Raum und/oder Benutzer

class RaumFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = 'room', 'user',
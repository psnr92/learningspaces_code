from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.

# Klasse Raum mit den 4 Kategorien und den jeweiligen Attributen

class Room(models.Model):
    ROOM_CATEGORIES = (
        ('Unterrichtsraum', 'Unterrichtsraum'),
        ('Hörsaal', 'Hörsaal'),
        ('PC-Raum', 'PC-Raum'),
        ('Selbstlernecke', 'Selbstlernecke'),
    )
    raumID = models.CharField(max_length=10)
    category = models.CharField(max_length=15, choices=ROOM_CATEGORIES)
    anzahl_plaetze = models.IntegerField()
    anzahl_pc = models.IntegerField()

    def __str__(self):
        return f'{self.raumID} | {self.category} | Sitzplätze: {self.anzahl_plaetze} | Anzahl PCs: {self.anzahl_pc}'

# Klasse Buchung mit den jeweiligen Attributen  Buchugsbestätigung

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

# Buchugsbestätigung

    def __str__(self):
        return f'{self.user} hat {self.room} gebucht. || Check-In: {self.check_in} , Check-Out: {self.check_out}'

    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args=[self.pk, ])
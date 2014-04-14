from django.contrib import admin

from equipment.models import Equipment, Book, Reservation

admin.site.register(Equipment)
admin.site.register(Book)
admin.site.register(Reservation)

from django.contrib import admin

from equipment.models import Equipment, Book, Reservation

class EquipmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('author','title',)}

admin.site.register(Equipment,EquipmentAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Reservation)

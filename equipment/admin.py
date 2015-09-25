from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from equipment.models import Status, Equipment, Book, Reservation


def delete_selected(self, request, obj):
    for o in obj.all():
        o.delete()


# Define an inline admin descriptor for Person model
class StatusInline(admin.StackedInline):
    model = Status
    can_delete = False
    verbose_name_plural = 'person'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (StatusInline,)


class EquipmentAdmin(admin.ModelAdmin):
    readonly_fields = ('recent_checkouts',)


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('recent_checkouts',)


class ReservationAdmin(admin.ModelAdmin):
    actions = [delete_selected]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reservation, ReservationAdmin)

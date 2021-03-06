import datetime
from tzlocal import get_localzone

from django.core.management.base import BaseCommand

from equipment.models import Reservation
from equipment.utils import send_checkout_reminder, send_return_reminder, send_late_reminder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get current time
        localtz = get_localzone()
        now = localtz.localize(datetime.datetime.now())

        # Constrain search range
        range_start = localtz.localize(datetime.datetime.now()) - datetime.timedelta(hours=48)
        range_end = localtz.localize(datetime.datetime.now()) + datetime.timedelta(hours=48)

        reservations = Reservation.objects.filter(start_date__gte=range_start, end_date__lte=range_end)

        for reservation in reservations:
            # Check for reservations beginning in less than 24 hours
            if now.date() + datetime.timedelta(
                    hours=24) >= reservation.start_date.date() and not reservation.checkout_reminder_sent:
                send_checkout_reminder(reservation)
                reservation.checkout_reminder_sent = True
                reservation.save()

            # Check for reservations ending in less than 24 hours (that that don't start and end on the same day)
            elif now.date() + datetime.timedelta(
                    hours=24) >= reservation.end_date.date() and reservation.start_date.date() != reservation.end_date.date() \
                    and not reservation.return_reminder_sent:
                send_return_reminder(reservation)
                reservation.return_reminder_sent = True
                reservation.save()

            # Check for late reservations
            elif now.date() >= reservation.end_date.date() + datetime.timedelta(
                    hours=24) and not reservation.returned and not reservation.late_reminder_sent:
                send_late_reminder(reservation)
                reservation.late_reminder_sent = True
                reservation.save()

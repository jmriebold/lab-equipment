import datetime
from tzlocal import get_localzone

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from equipment.models import Status


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get current time
        localtz = get_localzone()
        now = localtz.localize(datetime.datetime.now())
        now = now.date()

        users = Status.objects.filter(privilege_expiry__lte=now)

        for user in users:
            #user_status = Status.objects.get(user__exact=user)
            user.privilege_level = 4
            user.lab_membership = 'n'
            user.privilege_expiry = None
            user.save()

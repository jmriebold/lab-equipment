import datetime

from tzlocal import get_localzone
from django.core.management.base import BaseCommand

from equipment.models import Status


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get current time
        localtz = get_localzone()
        now = localtz.localize(datetime.datetime.now())
        now = now.date()

        # Find users with expired permissions
        users = Status.objects.filter(privilege_expiry__lte=now)

        # Reset permissions to default
        for user in users:
            user.privilege_level = 4
            user.lab_membership = 'n'
            user.privilege_expiry = None
            user.save()

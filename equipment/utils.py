# Claire Jaja & John Riebold
# 4/14/14
# This module provides various functions for the equipment app, including automatically resizing images,
# to the maximum allowed width, adding reservations to the Google Calendars, and sending reminder emails.

from PIL import Image
from django.conf import settings
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery


def autoresize_image(image_path):
    image = Image.open(image_path)
    width = image.size[0]

    if width > settings.IMAGE_MAX_WIDTH:
        height = image.size[1]
        reduce_factor = settings.IMAGE_MAX_WIDTH / float(width)
        reduced_width = int(width * reduce_factor)
        reduced_height = int(height * reduce_factor)
        image = image.resize((reduced_width, reduced_height), Image.ANTIALIAS)
        image.save(image_path)

    thumbnail = create_thumbnail(image)
    split_image_path = image_path.split(".")
    thumbnail.save(".".join(split_image_path[:-1]) + "_thumbnail." + split_image_path[-1])


def create_thumbnail(image):
    width = image.size[0]
    height = image.size[1]
    reduce_factor = settings.THUMBNAIL_WIDTH / float(width)
    reduced_width = int(width * reduce_factor)
    reduced_height = int(height * reduce_factor)
    thumbnail = image.resize((reduced_width, reduced_height), Image.ANTIALIAS)

    return thumbnail


# Add reservation to Google Calendar
def add_to_calendar(user, equipment, start_date, end_date):
    start_date = str(start_date).replace(' ', 'T')
    end_date = str(end_date).replace(' ', 'T')

    # Get Google credentials
    service_account_email = '275676223429-p0g1vpujgfric1gjoo020e898lhui6pa@developer.gserviceaccount.com'

    with open('/home/calendar/privatekey.pem') as f:
        private_key = f.read()

    credentials = SignedJwtAssertionCredentials(
        service_account_email,
        private_key,
        scope='https://www.googleapis.com/auth/calendar'
    )

    # Create service
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)

    # Define event
    event = {
        'summary': str(user) + ': ' + str(equipment),
        'description': 'Checked out by ' + str(user),
        'start': {
            'dateTime': start_date,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_date,
            'timeZone': 'America/Los_Angeles',
        },
    }

    # Save to calendar
    event = service.events().insert(calendarId='lbchkout@uw.edu', body=event).execute()

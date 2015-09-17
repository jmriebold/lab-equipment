# Claire Jaja & John Riebold
# 4/14/14
# This module provides various functions for the equipment app, including automatically resizing images,
# to the maximum allowed width, adding reservations to the Google Calendars, and sending reminder emails.

import re
import smtplib

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


# Convert lab code to lab name
def get_lab(lab):
    return lab.replace('P', 'phonlab').replace('S', 'sociolab')


def get_equip_details(equipment):
    equipment = str(equipment)
    # Strip formatting
    equipment = re.sub('.*: |[<>[]]', '', equipment)
    # Split into fields
    equipment = equipment.split(',')
    # Store values
    equip_cat = equipment[0]
    equip_name = equipment[1]
    equip_model = ' '.join(equipment[2:4])
    equip_lab = get_lab(equipment[4])

    return equip_cat, equip_name, equip_model, equip_lab


# Add reservation to Google Calendar
def add_to_calendar(name, email, equipment, start_date, end_date, purpose):
    start_date = str(start_date).replace(' ', 'T')
    end_date = str(end_date).replace(' ', 'T')

    equip_cat, equip_name, equip_model, equip_lab = get_equip_details(equipment)

    service_account_email = '275676223429-p0g1vpujgfric1gjoo020e898lhui6pa@developer.gserviceaccount.com'

    with open('/home/calendar/privatekey.pem') as f:
        private_key = f.read()

    # Get Google credentials
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
        'summary': name + ': ' + equip_model + ' (' + equip_lab + ')',
        'description': purpose + '\n\nContact: ' + name + ' (' + email + ')',
        'start': {
            'dateTime': start_date,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_date,
            'timeZone': 'America/Los_Angeles',
        },
    }

    # Find calendar
    cal_id = get_calendar(equip_lab, equip_cat, equip_name)

    # Save to calendar
    event = service.events().insert(calendarId=cal_id, body=event).execute()


def get_calendar(lab, category, name):
    # Dict storing calendar IDs for lab equipment
    calendars = {
        'phonlab': {
            'rec': {
                'Flash recorder 3': 'mmdmuahdqftv87neh31absdhts@group.calendar.google.com',
                'Flash recorder 4': 'tfhu3bhi7apnv17l23qj1fr3e0@group.calendar.google.com',
                'Flash recorder 5': 'mfhl73covk8tkqplrkn0p7iok4@group.calendar.google.com',
                'Flash recorder 6': 'ir9r7nf35vj9ft6890crl4ebgo@group.calendar.google.com',
                'Flash recorder 7': 'mb3p8toe9oettoki3o1krm679k@group.calendar.google.com',
                'Flash recorder 8': 'ro88t9o5a7b3m6i3v03fesdfus@group.calendar.google.com'
            },
            'comp': {
                'Gambit': 'u1l74m9g9r93f85goetjanjrfs@group.calendar.google.com',
                'Nightcrawler': 'p9jahh5ia3nj3dll630jonegns@group.calendar.google.com'
            },
            'booth': {
                'Magneto': '7tp04hggfn4fq9am8n4sbgso3k@group.calendar.google.com'
            },
            'oth': '9se5b0fvkvfrn62tuicp4d1h1o@group.calendar.google.com'
        },
        'sociolab': {
            'rec': {
                'Flash recorder 1': 'u9mubhqkqrdaqmt62okdulfras@group.calendar.google.com',
                'Flash recorder 2': '9mdgkl5e5nrclr7c4m8f74d3ts@group.calendar.google.com',
                'Flash recorder 3': 'n4kbm7q8taflqn20qooti85qlg@group.calendar.google.com'
            },
            'comp': {
                'Abaddon': 'ev9pb2dmu2j3fleskd8o6tgvnk@group.calendar.google.com',
                'Astrid': 'teo2on31gmtl61lkln0vd0ql0c@group.calendar.google.com',
                'Caan': 'qa61uu0o9jlne7kphc7aofj6i0@group.calendar.google.com',
                'Chesterton': '7hnn52hibggqriv6i36uslcavo@group.calendar.google.com'
            },
        }
    }

    return calendars[lab][category][name]


def send_email(recipient, message):
    username = 'lbchkout@uw.edu'
    with open('/home/calendar/email_account.txt', 'r') as f:
        password = f.readline()

    message = 'From: %s\n%s' % ('UW Linguistics Equipment Checkout', message)

    # Login to server and send email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipient, message)
    server.close()


def send_confirmation(recipient, email, equipment, start_date, end_date):
    equip_cat, equip_name, equip_model, equip_lab = get_equip_details(equipment)

    subject = 'Reservation Confirmation'
    text = 'Dear ' + recipient + '\nYou have reserved %s (%s) from the %s from %s to %s.' % (
        equip_name, equip_model, equip_lab, start_date, end_date)
    message = 'Subject: %s\n\n%s' % (subject, text)

    send_email(email, message)

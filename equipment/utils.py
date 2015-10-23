# Claire Jaja & John Riebold
# 4/14/14
# This module provides various functions for the equipment app, including automatically resizing images,
# to the maximum allowed width, adding reservations to the Google Calendars, and sending reminder emails.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

    # Shrink by largest dimension
    if width > height:
        reduce_factor = settings.THUMBNAIL_SIZE / float(width)
    else:
        reduce_factor = settings.THUMBNAIL_SIZE / float(height)

    reduced_width = int(width * reduce_factor)
    reduced_height = int(height * reduce_factor)
    thumbnail = image.resize((reduced_width, reduced_height), Image.ANTIALIAS)

    return thumbnail


# Get the ID of the calendar for a piece of equipment
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
            'oth': '9se5b0fvkvfrn62tuicp4d1h1o@group.calendar.google.com',
            'default': 'aqi89vl90b8i44uogtojbmnctk@group.calendar.google.com'
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
            'booth': {
                'Whole lab': '6o63676u7ji2su97469o83s6so@group.calendar.google.com'
            },
            'default': '3qp44cj94aba19alvj997ivrb0@group.calendar.google.com'
        }
    }

    # If equipment doesn't have a special calendar, return main lab calendar
    try:
        calendar = calendars[lab][category][name]
    except KeyError:
        calendar = calendars[lab]['default']

    return calendar


# Create Google Calendar service
def create_service():
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

    return service


# Add reservation to Google Calendar
def add_to_calendar(name, email, equipment, start_date, end_date, purpose):
    start_date = str(start_date).replace(' ', 'T')
    end_date = str(end_date).replace(' ', 'T')
    equip_lab = equipment.lab.replace('p', 'phonlab').replace('s', 'sociolab')

    service = create_service()

    # Define event
    event = {
        'summary': name + ': ' + equipment.model + ' (' + equip_lab + ')',
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
    cal_id = get_calendar(equip_lab, equipment.category, equipment.name)

    # Save to calendar
    event = service.events().insert(calendarId=cal_id, body=event).execute()

    return cal_id, event


def remove_from_calendar(cal_id, event_id):
    service = create_service()

    service.events().delete(calendarId=cal_id, eventId=event_id).execute()


# Get details of reservation for email methods
def get_details(reservation):
    name = reservation.reserved_by.get_full_name()
    if name == '':
        name = str(reservation.reserved_by)
    email = reservation.reserved_by.email
    if email == '':
        email == str(reservation.reserved_by) + '@uw.edu'
    equipment_list = ['%s (%s %s)' % (equip.name, equip.manufacturer, equip.model) for equip in
                      reservation.equipment.all()]
    if len(equipment_list) > 1:
        equipment_list = ', '.join(equipment_list)
    else:
        equipment_list = equipment_list[0]
    equip_lab = reservation.equipment.all()[0].lab.replace('p', 'phonlab').replace('s', 'sociolab')

    return name, email, equipment_list, equip_lab, reservation.start_date, reservation.end_date


def send_email(recipient, subject, body):
    # Create message container
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = 'UW Linguistics Equipment Checkout'
    message['To'] = ', '.join(recipient)
    body = MIMEText(body, 'html')
    message.attach(body)

    username = 'lbchkout@uw.edu'
    with open('/home/calendar/email_account.txt', 'r') as f:
        password = f.readline()

    # Login to server and send email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipient, message.as_string())
    server.close()


# Send a confirmation email on successful reservation
def send_confirmation(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    subject = 'Reservation Confirmation'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           You have reserved %s from the %s from %s to %s.<br><br>
           For links to equipment manuals and guides, see the <a href="https://zeos.ling.washington.edu/equipment-reservations/equipment/all-equipment">equipment details page</a>.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab, start_date, end_date)

    send_email([email], subject, body)


# Send a confirmation email on successful cancellation
def send_cancel_confirmation(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    subject = 'Cancellation Confirmation'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           You have canceled your reservation of %s from the %s from %s to %s.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab, start_date, end_date)

    send_email([email], subject, body)


# Send a confirmation email on successful return
def send_return_confirmation(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    subject = 'Return Confirmation'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           You have successfully returned %s from the %s. If any equipment was marked lost or deleted, the appropriate lab director will be notified.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab)

    send_email([email], subject, body)


# Send a reminder email for upcoming reservations
def send_checkout_reminder(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    subject = 'Upcoming Reservation'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           This is a reminder that you have a reservation starting tomorrow. You have reserved %s from the %s from %s to %s.<br><br>
           For links to equipment manuals and guides, see the <a href="https://zeos.ling.washington.edu/equipment-reservations/equipment/all-equipment">equipment details page</a>.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab, start_date, end_date)

    send_email([email], subject, body)


# Send a reminder email for upcoming returns
def send_return_reminder(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    subject = 'Equipment Due Tomorrow'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           This is a reminder that your reservation of %s from the %s is due tomorrow. Please ensure that after returning the equipment you mark the it as returned and indicate its condition on the <a href="https://zeos.ling.washington.edu/equipment-reservations/equipment/your-reservations">your reservations page</a>.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab)

    send_email([email], subject, body)


# Send a reminder email for upcoming returns
def send_late_reminder(reservation):
    recipient, email, equipment, equip_lab, start_date, end_date = get_details(reservation)

    if equip_lab == 'phonlab':
        email = [email, 'rawright@uw.edu']
    else:
        email = [email, 'wassink@uw.edu']

    subject = 'Equipment Late'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
           This is a reminder that your reservation of %s from the %s was due yesterday. Please return it immediately, as other lab members may be waiting to check it out. After returning the equipment, please mark it as returned and indicate its condition on the <a href="https://zeos.ling.washington.edu/equipment-reservations/equipment/your-reservations">your reservations page</a>.<br><br>
           This is an automated email. If you have any questions or concerns, please contact the lab SA or the requisite lab director.
        </p>
      </body>
    </html>
    """ % (recipient, equipment, equip_lab)

    send_email(email, subject, body)


# Send notification about damaged/lost equipment
def notify_labdirector(reservation, equipment, condition):
    name = reservation.reserved_by.get_full_name()
    if name == '':
        name = str(reservation.reserved_by)
    equip_lab = equipment.lab

    condition = condition.replace('br', 'broken').replace('ls', 'lost')

    subject = 'Equipment ' + condition

    if equip_lab == 'p':
        lab_director = 'Richard'
        email = 'rawright@uw.edu'
    else:
        lab_director = 'Alicia'
        email = 'wassink@uw.edu'

    # Create HTML message body
    body = """\
    <html>
      <head></head>
      <body>
        <p>Dear %s,<br>
            %s has reported that %s has been %s.
        </p>
      </body>
    </html>
    """ % ([lab_director], name, equipment, condition)

    send_email(email, subject, body)

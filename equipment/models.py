from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from utils import autoresize_image, add_to_calendar, remove_from_calendar, send_confirmation


# Extend Django's User model with lab-specific fields
class Status(models.Model):
    PRIVILEGE_LEVELS = ((1, 'director'), (2, 'lab member'), (3, 'student'), (4, 'none'))
    LAB_MEMBERSHIP = (('b', 'both'), ('s', 'sociolab'), ('p', 'phonlab'), ('n', 'neither'))

    user = models.OneToOneField(User)

    # default privilege level is student, default lab membership is neither
    privilege_level = models.IntegerField(choices=PRIVILEGE_LEVELS, default=4)
    lab_membership = models.CharField(max_length=1, choices=LAB_MEMBERSHIP, default='n')


# This class is for all the equipment in the lab.
class Equipment(models.Model):
    # all equipment associated with either Phonetics or Sociolinguistics Lab
    LAB_CHOICES = (('P', 'Phonetics'), ('S', 'Sociolinguistics'),)

    # equipment for use in lab or in field or both
    LAB_OR_FIELD = (('lab', 'lab'), ('field', 'field'), ('both', 'lab or field'),)
    
    # equipment categories
    CATEGORY_CHOICES = (
        ('comp', 'computer'),
        ('mic', 'microphone'),
        ('rec', 'recorder'),
        ('head', 'headphones'),
        ('booth', 'booth'),
        ('amp', 'amplifier'),
        ('cam', 'camera'),
        ('acc', 'accessories'),
        ('oth', 'other'),
    )

    # equipment has a physical location
    LOCATION_CHOICES = (
        ('Phonlab', (
            ('cab1_draw1', 'cabinet 1 drawer 1'),
            ('cab1_draw2', 'cabinet 1 drawer 2'),
            ('cab1_draw3', 'cabinet 1 drawer 3'),
            ('cab1_draw4', 'cabinet 1 drawer 4'),
            ('bookshelf1', 'bookshelf 1'),
            ('cab2', 'cabinet 2'),
        )
         ),
        ('Sociolab', (
            ('cab1_draw1', 'cabinet 1 drawer 1'),
            ('cab1_draw2', 'cabinet 1 drawer 2'),
        )
         ),
        ('unknown', 'unknown')
    )

    STATUS = (('ok', 'OK'), ('ls', 'lost'), ('br', 'broken'))

    # equipment has privilege level that says who can check it out
    PRIVILEGE_LEVELS = ((1, 'director'), (2, 'lab member'), (3, 'student'))

    name = models.CharField(max_length=200)  # unique name for each piece of equipment
    slug = models.SlugField()
    lab = models.CharField(max_length=1, choices=LAB_CHOICES)
    lab_or_field = models.CharField(max_length=5, choices=LAB_OR_FIELD)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(max_length=200)  # equipment manufacturer
    model = models.CharField(max_length=200)  # what the equipment is exactly i.e. H4 Zoom
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS, blank=False, default='ok')
    reservable = models.BooleanField(default=True)  # whether or not people can reserve/check out this equipment
    max_reservation_length = models.IntegerField(blank=True, null=True)  # maximum allowed reservation in hours
    privilege_level = models.IntegerField(choices=PRIVILEGE_LEVELS, blank=True)
    image = models.ImageField(upload_to='equipment_images/', default='equipment_images/null.jpg')
    manual = models.URLField(blank=True)
    guide = models.URLField(blank=True)

    def __unicode__(self):
        return u"%s: %s %s (%s)" % (
        self.name, self.manufacturer, self.model, self.lab.replace('P', 'phonlab').replace('S', 'sociolab'))

    def clean(self):
        # max reservation length and privilege level required if reservable
        if self.reservable:
            if self.max_reservation_length is None or self.privilege_level == '':
                raise ValidationError(
                    "All reservable equipment must have a maximum reservation length and a privilege level.")

    def save(self, *args, **kwargs):
        # Mark as not reservable if lost or broken
        if self.status != 'ok':
            self.reservable = False

        super(Equipment, self).save(*args, **kwargs)

        if self.image:
            autoresize_image(self.image.path)


class Book(models.Model):
    # all books associated with either Phonetics or Sociolinguistics Lab
    LAB_CHOICES = (('P', 'Phonetics'), ('S', 'Sociolinguistics'),)

    # books also have a physical location
    LOCATION_CHOICES = (
        ('Phonlab', (
            ('cab1_draw1', 'cabinet 1 drawer 1'),
            ('cab1_draw2', 'cabinet 1 drawer 2'),
            ('cab1_draw3', 'cabinet 1 drawer 3'),
            ('cab1_draw4', 'cabinet 1 drawer 4'),
            ('bookshelf1', 'bookshelf 1'),
            ('cab2', 'cabinet 2'),
        )
         ),
        ('Sociolab', (
            ('cab1_draw1', 'cabinet 1 drawer 1'),
            ('cab1_draw2', 'cabinet 1 drawer 2'),
        )
         ),
        ('unknown', 'unknown')
    )

    PRIVILEGE_LEVELS = ((1, 'director'), (2, 'lab member'), (3, 'student'))

    STATUS = (('ok', 'OK'), ('ls', 'lost'), ('br', 'broken'))

    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    lab = models.CharField(max_length=1, choices=LAB_CHOICES)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS, blank=False, default='ok')
    reservable = models.BooleanField(default=True)  # whether or not people can reserve/check out this book
    max_reservation_length = models.IntegerField(blank=True, null=True)  # maximum allowed reservation in hours
    privilege_level = models.IntegerField(choices=PRIVILEGE_LEVELS, blank=True)
    image = models.ImageField(upload_to='equipment_images/', default='equipment_images/null.jpg')

    def __unicode__(self):
        return u"%s by %s" % (self.title, self.author)

    def clean(self):
        # max reservation length and privilege level required if reservable
        if self.reservable:
            if self.max_reservation_length is None or self.privilege_level is None:
                raise ValidationError(
                    "All reservable equipment must have a maximum reservation length and a privilege level.")
            else:
                raise ValidationError("privilege level is " + self.privilege_level)

    def save(self, *args, **kwargs):
        # Mark as not reservable if lost or damaged
        if self.status != 'ok':
            self.reservable = False

        super(Book, self).save(*args, **kwargs)

        if self.image:
            autoresize_image(self.image.path)


class Reservation(models.Model):
    equipment = models.ManyToManyField(Equipment)  # what's being reserved, can be multiple items
    reserved_by = models.ForeignKey(User)  # who's reserving it
    purpose = models.CharField(max_length=500)  # what's the purpose and where they're taking it
    course = models.CharField(max_length=20, blank=True)  # optional, if it's being used for a course, which course
    start_date = models.DateTimeField()  # when the equipment is checked out
    end_date = models.DateTimeField()  # when the equipment will be returned
    calendar_id = models.CharField(max_length=1000, default='', editable=False)  # The Google Calendar ID
    calendar_event = models.CharField(max_length=1000, default='', editable=False)  # The event ID on the Google Calendar
    returned = models.BooleanField(blank=False, default=False)

    def delete(self, using=None):
        for i, event in enumerate(self.calendar_event.split('-')):
            event_id = event
            cal_id = self.calendar_id.split('-')[i]
            remove_from_calendar(cal_id, event_id)

        super(Reservation, self).delete()

    def __unicode__(self):
        return u"Reservation by %s from %s to %s" % (self.reserved_by, self.start_date, self.end_date)


# Add/remove calendar event(s) and send confirmation email when equipment is added/removed
@receiver(m2m_changed, sender=Reservation.equipment.through)
def tasks(sender, instance, action, **kwargs):
    if action == 'post_add':
        # Get name and email
        name = instance.reserved_by.get_full_name()
        if name == '':
            name = str(self.reserved_by)
        email = instance.reserved_by.email
        if email == '':
            email == str(instance.reserved_by) + '@uw.edu'

        events = ''
        cal_ids = ''
        equipment_list = []
        equip_lab = instance.equipment.all()[0].lab.replace('P', 'phonlab').replace('S', 'sociolab')

        # Add calendar events for each equipment, store names
        for i, equip in enumerate(instance.equipment.all()):
            cal_id, event = add_to_calendar(name, email, equip, instance.start_date, instance.end_date, instance.purpose)
            events += str(event['id']) + '-'
            cal_ids += cal_id + '-'

            equipment_list.append('%s (%s %s)' % (equip.name, equip.manufacturer, equip.model))

        # Save calendar event IDs to model
        instance.calendar_event = events.strip('-')
        instance.calendar_id = cal_ids.strip('-')
        instance.save()

        send_confirmation(name, email, equipment_list, equip_lab, instance.start_date, instance.end_date)

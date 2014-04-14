from django.db import models
from django.contrib.auth.models import User

# Going to use Django's Users class
#
# This class is for people who can check out equipment.
# Will update with different privilege levels maybe.
#class Person(models.Model):
#    # my options for privilege levels
#    PRIVILEGE_LEVELS = ((3,'director'),(2,'lab member'),(1,'student'),)
#
#    netid = models.CharField(max_length=50)
#    email = models.EmailField()
#    first_name = models.CharField(max_length=50)
#    last_name = models.CharField(max_length=50)
#    department = models.CharField(max_length=50)
#    # default privilege level as student, will need approval from director to change to 2 or 3
#    privilege_level = models.CharField(max_length=1, choices=PRIVILEGE_LEVELS, default=1) 
#
#    def __unicode__(self):
#        return self.netid


# This class is for all the equipment in the lab.
class Equipment(models.Model):
    # defining some choices for fields

    # all equipment associated with either Phonetics or Sociolinguistics Lab
    LAB_CHOICES = (('P', 'Phonetics'),('S', 'Sociolinguistics'),)

    # equipment for use in lab or in field or both
    LAB_OR_FIELD = (('lab','lab'),('field','field'),('both','lab or field'),)
    
    # equipment categories
    # need to update with actual categories
    CATEGORY_CHOICES = (
        ('mic','microphone'),
        ('rec','recorder'),
        ('booth','booth'),
        ('book','book'),
        ('head','headphones')
    )

    # equipment has a physical location
    # need to update with actual possible locations
    LOCATION_CHOICES = (
        ('PhonLab', (
                ('cab1_draw1','cabinet 1 drawer 1'),
                ('cab1_draw2','cabinet 1 drawer 2'),
                ('cab1_draw3','cabinet 1 drawer 3'),
                ('cab1_draw4','cabinet 1 drawer 4'),
                ('bookshelf1','bookshelf 1'),
                ('cab2','cabinet 2'),
            )
        ),
        ('SocioLab', (
                ('cab1_draw1','cabinet 1 drawer 1'),
                ('cab1_draw2','cabinet 1 drawer 2'),
             )
        ),
        ('unknown','unknown')   
    )

    # equipment has privilege level that says who can check it out
    # this can be checked against a user's privilege level
    # ideally, will implement so can be overridden by lab director
    PRIVILEGE_LEVELS = (('3','director only'),('2','lab member or director only'),('1','lab member, director, or student'),)

    name = models.CharField(max_length=200) # unique name for each piece of equipment
    lab = models.CharField(max_length=1, choices=LAB_CHOICES)
    lab_or_field = models.CharField(max_length=5, choices=LAB_OR_FIELD)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(max_length=200) # equipment manufacturer
    equip_model = models.CharField(max_length=200) # what the equipment is exactly i.e. H4 Zoom
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    reservable = models.BooleanField() # whether or not people can reserve/check out this equipment
    max_reservation_length = models.IntegerField() # maximum allowed reservation in hours
    privilege_level = models.CharField(max_length=1, choices=PRIVILEGE_LEVELS)
    image = models.ImageField(upload_to='equipment_images/', default='equipment_images/null.jpg')

    # can check if is currently available by checking if there's any current reservation

    def __unicode__(self):
        return u"%s : %s" % (self.name, self.equip_model)

class Book(models.Model):
    # all books associated with either Phonetics or Sociolinguistics Lab
    LAB_CHOICES = (('P', 'Phonetics'),('S', 'Sociolinguistics'),)

    # books also have a physical location
    # need to update with actual possible locations
    LOCATION_CHOICES = (
        ('PhonLab', (
                ('cab1_draw1','cabinet 1 drawer 1'),
                ('cab1_draw2','cabinet 1 drawer 2'),
                ('cab1_draw3','cabinet 1 drawer 3'),
                ('cab1_draw4','cabinet 1 drawer 4'),
                ('bookshelf1','bookshelf 1'),
                ('cab2','cabinet 2'),
            )
        ),
        ('SocioLab', (
                ('cab1_draw1','cabinet 1 drawer 1'),
                ('cab1_draw2','cabinet 1 drawer 2'),
             )
        ),
        ('unknown','unknown')   
    )

    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    lab = models.CharField(max_length=1, choices=LAB_CHOICES)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    reservable = models.BooleanField() # whether or not people can reserve/check out this book

    def __unicode__(self):
        return u"%s by %s" % (self.title, self.author)

class Reservation(models.Model):
    equipment = models.ManyToManyField(Equipment) # what's being reserved, can be multiple items
    reserved_by = models.ForeignKey(User) # who's reserving it
    purpose = models.CharField(max_length=500) # what's the purpose and where they're taking it
    course = models.CharField(max_length=20) # optional, if it's being used for a course, which course
    start_date = models.DateTimeField() # when the equipment is checked out
    end_date = models.DateTimeField() # when the equipment will be returned


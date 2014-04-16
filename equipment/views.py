from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from equipment.models import Equipment, Book, Reservation
from collections import defaultdict
import datetime

def index(request):
    return render(request, 'equipment/index.html')

def all_equipment(request):
    equip = {}
    for category in Equipment.CATEGORY_CHOICES:
        equip[category] = Equipment.objects.filter(category=category[0])
    context = {'equip': equip}
    return render(request, 'equipment/equipment.html', context)

def equip_category(request,category):
    equip = Equipment.objects.filter(category=category)
    context = {'equip': equip}
    return render(request, 'equipment/equipment.html', context)

def equip_detail(request,slug):
    equip = Equipment.objects.filter(slug=slug)
    context = {'equip': equip}
    return render(request, 'equipment/equipment-detail.html', context)

def current_reservations(request):
    reservations = Reservation.objects.all().order_by('start_date')
    context = {'reservations': reservations}
    return render(request, 'equipment/current-reservations.html', context)

def reserve(request):
    return render(request, 'equipment/reserve/index.html')

def reserve_dates(request,start_date,end_date):
    # find any conflicting reservations
    start_date_split,start_time = start_date.split('T')
    year,month,day = [int(x) for x in start_date_split.split('-')]
    hour,minute = [int(x) for x in start_time.split(':')]
    start_datetime = datetime.datetime(year,month,day,hour,minute)
    end_date_split,end_time = end_date.split('T')
    year,month,day = [int(x) for x in end_date_split.split('-')]
    hour,minute = [int(x) for x in end_time.split(':')]
    end_datetime = datetime.datetime(year,month,day,hour,minute)
    conflicting_reservations = Reservation.objects.filter(end_date__gt=start_datetime,start_date__lt=end_datetime)

    # any equipment reserved in a conflicting reservation is unavailable for this one
    unavailable_equipment = set()
    for reservation in conflicting_reservations:
        for equipment in reservation.equipment.all():
            unavailable_equipment.add(equipment.id)

    equipment = Equipment.objects.exclude(id__in=unavailable_equipment)

    context = {'equipment': equipment,'start_date':start_date,'end_date':end_date}
    return render(request, 'equipment/reserve/reserve_dates.html',context)

def reserve_confirmation(request,start_date,end_date,equipment):
    # convert strings for dates into datetimes
    start_date,start_time = start_date.split('T')
    year,month,day = [int(x) for x in start_date.split('-')]
    hour,minute = [int(x) for x in start_time.split(':')]
    start_date = datetime.datetime(year,month,day,hour,minute)
    end_date,end_time = end_date.split('T')
    year,month,day = [int(x) for x in end_date.split('-')]
    hour,minute = [int(x) for x in end_time.split(':')]
    end_date = datetime.datetime(year,month,day,hour,minute)
    # convert string for equipment ids into list of equipment ids
    equipment = [int(x) for x in equipment.split('-')]
    equipment = Equipment.objects.filter(id__in=equipment)
    context = {'start_date':start_date, 'end_date':end_date, 'equipment':equipment}
    return render(request,'equipment/reserve/reserve_confirmation.html',context)

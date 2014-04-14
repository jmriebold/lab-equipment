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
    year,month,day = [int(x) for x in start_date.split('-')]
    start_date = datetime.date(year,month,day)
    year,month,day = [int(x) for x in end_date.split('-')]
    end_date = datetime.date(year,month,day)
    conflicting_reservations = Reservation.objects.filter(end_date__gt=start_date,start_date__lt=end_date)

    # any equipment reserved in a conflicting reservation is unavailable for this one
    unavailable_equipment = set()
    for reservation in conflicting_reservations:
        for equipment in reservation.equipment.all():
            unavailable_equipment.add(equipment.id)

    equipment = Equipment.objects.exclude(id__in=unavailable_equipment)

    context = {'equipment': equipment}
    return render(request, 'equipment/reserve/reserve_dates.html',context)


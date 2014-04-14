from django.shortcuts import render
from django.http import HttpResponse
from equipment.models import Equipment, Book, Reservation

def index(request):
    return render(request, 'equipment/index.html')

def all_equipment(request):
    equip = Equipment.objects.all().order_by('manufacturer')
    context = {'equip': equip}
    return render(request, 'equipment/equipment.html', context)

def equip_category(request,category):
    equip = Equipment.objects.filter(category=category)
    context = {'equip': equip}
    return render(request, 'equipment/equipment.html', context)

def equip_detail(request,name):
    equip = Equipment.objects.filter(name=name)
    context = {'equip': equip}
    return render(request, 'equipment/equipment-detail.html', context)

def current_reservations(request):
    reservations = Reservation.objects.all().order_by('start_date')
    context = {'reservations': reservations}
    return render(request, 'equipment/current-reservations.html', context)

def reserve(request):
    return render(request, 'equipment/reserve/index.html')

def reserve_lab(request):
    equipment = Equipment.objects.exclude(lab_or_field='field')
    context = {'equipment': equipment}
    return render(request, 'equipment/reserve/2.html',context)

def reserve_field(request):
    equipment = Equipment.objects.exclude(lab_or_field='lab')
    context = {'equipment': equipment}
    return render(request, 'equipment/reserve/2.html',context)

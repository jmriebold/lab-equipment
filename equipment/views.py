import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from equipment.models import Equipment, Reservation


def index(request):
    return render(request, 'equipment/index.html')


# List all equipment
def all_equipment(request):
    equip_list = Equipment.objects.all()
    end_equip_list = []

    for equip in equip_list:
        split_image_url = equip.image.url.split(".")
        thumbnail = ".".join(split_image_url[:-1]) + "_thumbnail." + split_image_url[-1]
        end_equip_list.append((equip, thumbnail))

    context = {'equip_list': end_equip_list}

    return render(request, 'equipment/equipment.html', context)


# List equipment by category
def equip_category(request, category):
    equip_list = Equipment.objects.filter(category=category)
    context = {'equip_list': equip_list}

    return render(request, 'equipment/equipment.html', context)


# List equipment details
def equip_detail(request, slug):
    equip = Equipment.objects.filter(slug=slug)
    context = {'equip': equip}

    return render(request, 'equipment/equipment-detail.html', context)


# Display current reservations
def current_reservations(request):
    reservations = Reservation.objects.exclude(end_date__lt=datetime.datetime.now()).order_by('start_date')
    context = {'reservations': reservations}

    return render(request, 'equipment/current-reservations.html', context)


# Display user's reservations
def your_reservations(request):
    remote_user = request.environ.get('REMOTE_USER')
    user = User.objects.get(username__exact=remote_user)

    past_reservations = Reservation.objects.filter(reserved_by=user).filter(
        end_date__lt=datetime.datetime.now()).order_by('start_date')
    current_reservations = Reservation.objects.filter(reserved_by=user).exclude(
        end_date__lt=datetime.datetime.now()).order_by('start_date')
    context = {'past_reservations': past_reservations, 'current_reservations': current_reservations}

    return render(request, 'equipment/your-reservations.html', context)


def reserve(request):
    return render(request, 'equipment/reserve/index.html')


def reserve_dates(request, start_date, end_date):
    # find any conflicting reservations
    start_date_split, start_time = start_date.split('T')
    year, month, day = [int(x) for x in start_date_split.split('-')]
    hour, minute = [int(x) for x in start_time.split(':')]
    start_datetime = datetime.datetime(year, month, day, hour, minute)

    # reservations must be made 24 hours in advance
    if not datetime.datetime.now() + datetime.timedelta(hours=24) < start_datetime:
        return render(request, 'equipment/reserve/index.html', {
            'error_message': "Reservations must be made at least 24 hours in advance! Please input a start date more than 24 hours from now."})
    else:
        end_date_split, end_time = end_date.split('T')
        year, month, day = [int(x) for x in end_date_split.split('-')]
        hour, minute = [int(x) for x in end_time.split(':')]
        end_datetime = datetime.datetime(year, month, day, hour, minute)

        # calculate reservation length in hours
        reservation_length = end_datetime - start_datetime
        reservation_length = reservation_length.seconds / 60 / 60 + reservation_length.days * 24

        if not reservation_length > 0:
            return render(request, 'equipment/reserve/index.html', {
                'error_message': "Invalid time span! Please enter an end date that is after your start date."})
        else:
            conflicting_reservations = Reservation.objects.filter(end_date__gt=start_datetime,
                                                                  start_date__lt=end_datetime)

            # any equipment reserved in a conflicting reservation is unavailable for this one
            unavailable_equipment = set()
            for reservation in conflicting_reservations:
                for equipment in reservation.equipment.all():
                    unavailable_equipment.add(equipment.id)

            # exclude unavailable equipment, equipment that isn't reservable, and equipment whose max reservation
            # length is less than the requested reservation length
            available_equipment = Equipment.objects.exclude(id__in=unavailable_equipment).exclude(
                reservable=False).exclude(max_reservation_length__lt=reservation_length)
            unavailable_equipment = Equipment.objects.filter(id__in=unavailable_equipment)
            nonreservable_equipment = Equipment.objects.filter(reservable=False)
            shorter_reservation_equipment = Equipment.objects.exclude(id__in=unavailable_equipment).filter(
                reservable=True).filter(max_reservation_length__lt=reservation_length)

            context = {'available_equipment': available_equipment, 'unavailable_equipment': unavailable_equipment,
                       'nonreservable_equipment': nonreservable_equipment,
                       'shorter_reservation_equipment': shorter_reservation_equipment, 'start_date': start_date,
                       'end_date': end_date}

            return render(request, 'equipment/reserve/reserve_dates.html', context)


def reserve_confirmation(request, start_date, end_date, equipment):
    # convert strings for dates into datetimes
    start_date_string = start_date
    end_date_string = end_date
    start_date, start_time = start_date.split('T')
    year, month, day = [int(x) for x in start_date.split('-')]
    hour, minute = [int(x) for x in start_time.split(':')]
    start_date = datetime.datetime(year, month, day, hour, minute)
    end_date, end_time = end_date.split('T')
    year, month, day = [int(x) for x in end_date.split('-')]
    hour, minute = [int(x) for x in end_time.split(':')]
    end_date = datetime.datetime(year, month, day, hour, minute)

    # Get UW NetID
    remote_user = request.environ.get('REMOTE_USER')
    netid = remote_user.split('@')[0]

    # convert string for equipment ids into list of equipment ids
    equipment_string = equipment
    equipment = [int(x) for x in equipment.split('-')]
    equipment = Equipment.objects.filter(id__in=equipment)

    context = {"netid": netid, 'start_date': start_date, 'start_date_string': start_date_string, 'end_date': end_date,
               'end_date_string': end_date_string, 'equipment': equipment, 'equipment_string': equipment_string}

    return render(request, 'equipment/reserve/reserve_confirmation.html', context)


def make_reservation(request):
    start_date_string = request.POST['start_date_string']
    end_date_string = request.POST['end_date_string']
    equipment_string = request.POST['equipment_string']
    purpose = request.POST['purpose'].strip()
    course = request.POST['course']

    if purpose == '' or len(purpose) < 3:
        return render(request, 'equipment/reserve/index.html', {
            'error_message': "Invalid purpose! You must give a reason for checking out the equipment."})

    # Get current user, name, and email
    remote_user = request.environ.get('REMOTE_USER')
    user = User.objects.get(username__exact=remote_user)
    name = user.get_full_name()
    if name == '':
        name = user.split('@')[0]
    email = str(user)

    # convert strings to objects
    start_date, start_time = start_date_string.split('T')
    year, month, day = [int(x) for x in start_date.split('-')]
    hour, minute = [int(x) for x in start_time.split(':')]
    start_date = datetime.datetime(year, month, day, hour, minute)
    end_date, end_time = end_date_string.split('T')
    year, month, day = [int(x) for x in end_date.split('-')]
    hour, minute = [int(x) for x in end_time.split(':')]
    end_date = datetime.datetime(year, month, day, hour, minute)

    # convert string for equipment ids into list of equipment ids
    equipment = [int(x) for x in equipment_string.split('-')]
    equipment = Equipment.objects.filter(id__in=equipment)

    reservation = Reservation(purpose=purpose, course=course, start_date=start_date, end_date=end_date,
                              reserved_by=user)
    reservation.save()
    reservation.equipment.add(*equipment)

    return HttpResponseRedirect(reverse('done'))


def cancel_confirmation(request):
    reservation_id = request.POST['reservation_id']
    reservation_start_date = request.POST['reservation_start_date']
    reservation_end_date = request.POST['reservation_end_date']

    context = {'reservation_id': reservation_id, 'reservation_start_date': reservation_start_date,
               'reservation_end_date': reservation_end_date}

    return render(request, 'equipment/reserve/cancel_confirmation.html', context)


def cancel_reservation(request):
    reservation_id = request.POST['reservation_id']

    remote_user = request.environ.get('REMOTE_USER')
    user = User.objects.get(username__exact=remote_user)

    reservation = Reservation.objects.get(id=reservation_id)

    # Ensure owner of reservation is the one making the request
    if reservation.reserved_by == user:
        reservation.delete()
    else:
        return render(request, 'equipment/index.html', {
                'error_message': "Invalid user! You can only cancel your own reservations."})

    return your_reservations(request)


def done(request):
    return render(request, 'equipment/reserve/done.html')

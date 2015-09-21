from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from equipment import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^equipment/all-equipment$', views.all_equipment, name="all_equipment"),
    url(r'^equipment/(?P<category>\w+)$', views.equip_category, name="equip_category"),
    url(r'^equipment/(?P<slug>[A-Za-z0-9\-]+)/$', views.equip_detail, name="equip_detail"),
    url(r'^current-reservations$', views.current_reservations, name="current_reservations"),
    url(r'reserve$', views.reserve, name="reserve"),
    url(r'^reserve/(?P<start_date>[0-9\-]+T[0-9:]+)/(?P<end_date>[0-9\-]+T[0-9:]+)$', views.reserve_dates, name="reserve_dates"),
    url(r'^reserve/(?P<start_date>[0-9\-]+T[0-9:]+)/(?P<end_date>[0-9\-]+T[0-9:]+)/(?P<equipment>[0-9\-]+)$', views.reserve_confirmation, name="reserve_confirmation"),
    url(r'^reserve/make_reservation$', views.make_reservation, name="make_reservation"),
    url(r'^reserve/cancel_confirmation$', views.cancel_confirmation, name="cancel_confirmation"),
    url(r'^reserve/your-reservations$', views.cancel_reservation, name="cancel_reservation"),
    url(r'^reserve/done$', views.done, name="done"),
    url(r'^your-reservations$',views.your_reservations,name="your_reservations"),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

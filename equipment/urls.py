from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from equipment import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^equipment/all-equipment$', views.all_equipment, name="all_equipment"),
    url(r'^equipment/(?P<category>\w+)$', views.equip_category, name="equip_category"),
    url(r'^equipment/(\w+)/(?P<name>[A-Za-z0-9\-]+)/$', views.equip_detail, name="equip_detail"),
    url(r'^current-reservations$', views.current_reservations, name="current_reservations"),
    url(r'^reserve$', views.reserve, name="reserve"),
    url(r'^reserve/lab$', views.reserve_lab, name="reserve_lab"),
    url(r'^reserve/field$', views.reserve_field, name="reserve_field"),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
from . import views

app_name = 'cal'

urlpatterns= [
    url('calendar/', views.CalendarView.as_view(), name='calendar'),
    url('event/new/', views.event, name='new'),
    url(r'^event/edit/(?P<id>\d+)/$', views.event, name='event_edit'),
    url(r'^event/detail/(?P<day>\d+)/$', views.event_detail, name='event_detail'),
]
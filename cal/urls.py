from django.conf.urls import url
from . import  views

app_name = 'cal'

urlpatterns= [
    url('', views.CalendarView.as_view(), name='cal'),
]
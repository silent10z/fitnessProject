from django.forms import ModelForm, DateInput
from cal.models import Event


class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      # 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['title', 'work_weight', 'duration', 'work_set', 'repeat_count']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)



class detailForm(ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'workout_done', 'duration']



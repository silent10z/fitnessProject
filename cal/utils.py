from datetime import datetime, timedelta
from calendar import HTMLCalendar
from django.db.models import Q

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Event


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):

		events_per_day = events.filter(start_time__day=day)

		total_date = plus_date(self.year, self.month, day)

		d = ''

		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			return f"<td name='day_td' value='{total_date}'><span class='date'><a href='/cal/event/detail/{total_date}'>{day}</a></span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True,):
		input_date = '-'.join([str(self.year), str(self.month), "1"])
		format_date = datetime.strptime(input_date, "%Y-%m-%d").date()
		event = Event.objects.filter(writer=self.user)
		events = event.filter(start_time__year=format_date.year, start_time__month=format_date.month)


		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		cal += f'</table></div></main>'
		return cal


# 날짜 8자리로 만들어 주는 매소드
def plus_date(year, month, day):
	total_date = ''
	month_plus = month
	day_plus = day

	if month_plus < 10:
		month_plus = '0' + str(month_plus)

	if day_plus < 10:
		day_plus = '0' + str(day_plus)

	total_date = str(year) + str(month_plus) + str(day_plus)

	return total_date
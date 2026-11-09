"""
List filters for the Suit change list search bar.

DateRangeFilter comes from django-suit-daterange-filter
(https://github.com/f213/django-suit-daterange-filter),
Copyright (c) 2016 Fedor Borshev, MIT License.
"""
from datetime import datetime, time

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import pgettext

from .widgets import SuitDateWidget


class DateRangeForm(forms.Form):
    """
    "From" and "To" date fields named ``<field_name>_start`` and
    ``<field_name>_end``.
    """

    def __init__(self, *args, field_name='date', title='Date', **kwargs):
        self.field_name = field_name
        super().__init__(*args, **kwargs)

        placeholder = str(title).title()
        self.fields['%s_start' % field_name] = forms.DateField(
            widget=SuitDateWidget(attrs={'placeholder': placeholder}),
            label=pgettext('date', 'From'), required=False)
        self.fields['%s_end' % field_name] = forms.DateField(
            widget=SuitDateWidget(attrs={'placeholder': placeholder}),
            label=pgettext('date', 'To'), required=False)

    def _date(self, suffix, at):
        if not self.is_valid():
            return None
        value = self.cleaned_data.get('%s_%s' % (self.field_name, suffix))
        if not value:
            return None
        value = datetime.combine(value, at)
        return timezone.make_aware(value) if settings.USE_TZ else value

    def start_date(self):
        """The "From" date at 00:00, or None"""
        return self._date('start', time.min)

    def end_date(self):
        """The "To" date at 23:59:59.999999, or None"""
        return self._date('end', time.max)


class DateRangeFilter(admin.FieldListFilter):
    """
    Filters a date or datetime field by an inclusive "From" / "To" date
    range, shown as two date inputs in the change list search bar::

        from suit.filters import DateRangeFilter

        class OrderAdmin(admin.ModelAdmin):
            list_filter = (('created_at', DateRangeFilter),)
    """
    template = 'admin/date_range_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def expected_parameters(self):
        return ['%s_start' % self.field_path, '%s_end' % self.field_path]

    def choices(self, changelist):
        return [{'query_string': ''}]

    def get_form(self, request):
        return DateRangeForm(data=request.GET, field_name=self.field_path,
                             title=self.title)

    @property
    def media(self):
        """Calendar scripts of the date inputs, see suit_list_filters_media"""
        return self.form.media

    def queryset(self, request, queryset):
        filter_args = {}
        start, end = self.form.start_date(), self.form.end_date()
        if start:
            filter_args['%s__gte' % self.field_path] = start
        if end:
            filter_args['%s__lte' % self.field_path] = end
        return queryset.filter(**filter_args) if filter_args else queryset

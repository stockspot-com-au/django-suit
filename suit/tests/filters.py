from datetime import date, datetime

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from suit.filters import DateRangeFilter, DateRangeForm
from suit.tests.mixins import UserTestCaseMixin
from suit.tests.models import Event, EventAdmin


class DateRangeFormTestCase(TestCase):
    def form(self, **data):
        return DateRangeForm(data=data, field_name='happened_at')

    def test_field_names(self):
        self.assertEqual(list(DateRangeForm().fields), ['date_start', 'date_end'])
        self.assertEqual(list(self.form().fields),
                         ['happened_at_start', 'happened_at_end'])

    def test_title_is_the_placeholder(self):
        form = DateRangeForm(field_name='x', title='date joined')
        self.assertEqual(form.fields['x_start'].widget.attrs['placeholder'],
                         'Date Joined')

    def test_range_covers_whole_days(self):
        form = self.form(happened_at_start='2016-01-15',
                         happened_at_end='2016-02-10')
        self.assertEqual(form.start_date(), timezone.make_aware(
            datetime(2016, 1, 15)))
        self.assertEqual(form.end_date(), timezone.make_aware(
            datetime(2016, 2, 10, 23, 59, 59, 999999)))

    @override_settings(USE_TZ=False)
    def test_without_timezone(self):
        form = self.form(happened_at_start='2016-01-15',
                         happened_at_end='2016-02-10')
        self.assertEqual(form.start_date(), datetime(2016, 1, 15))
        self.assertEqual(form.end_date(),
                         datetime(2016, 2, 10, 23, 59, 59, 999999))

    def test_empty_or_invalid(self):
        self.assertIsNone(self.form().start_date())
        self.assertIsNone(self.form().end_date())
        self.assertIsNone(self.form(happened_at_start='nope').start_date())


class DateRangeFilterTestCase(UserTestCaseMixin):
    def setUp(self):
        self.login_superuser()
        for day in (1, 10, 20):
            Event.objects.create(name='day-%s' % day, happened_at=timezone.make_aware(
                datetime(2026, 3, day, 12)))

    def changelist(self, **params):
        self.response = self.client.get(
            reverse('filters:tests_event_changelist'), params)
        self.assertEqual(self.response.status_code, 200)
        return self.response.context_data['cl']

    def names(self, **params):
        return sorted(e.name for e in self.changelist(**params).result_list)

    def test_filters_inclusive_range(self):
        self.assertEqual(self.names(), ['day-1', 'day-10', 'day-20'])
        self.assertEqual(self.names(happened_at_start='2026-03-10'),
                         ['day-10', 'day-20'])
        self.assertEqual(self.names(happened_at_end='2026-03-10'),
                         ['day-1', 'day-10'])
        self.assertEqual(self.names(happened_at_start='2026-03-10',
                                    happened_at_end='2026-03-10'), ['day-10'])

    def test_invalid_date_is_ignored(self):
        self.assertEqual(self.names(happened_at_start='nope'),
                         ['day-1', 'day-10', 'day-20'])

    def test_renders_in_search_bar(self):
        self.changelist(happened_at_start=date(2026, 3, 10).isoformat())
        self.assertContains(self.response, '<div class="date_range_filter">')
        self.assertContains(self.response, 'name="happened_at_start"')
        self.assertContains(self.response, 'value="2026-03-10"')
        self.assertContains(self.response, 'name="happened_at_end"')
        self.assertContains(self.response, 'placeholder="Happened At"')
        self.assertContains(self.response, 'admin/js/calendar.js', count=1)

    def test_calendar_scripts_load_once_for_several_filters(self):
        filters = EventAdmin.list_filter
        EventAdmin.list_filter = filters + (('id', DateRangeFilter),)
        try:
            self.changelist()
        finally:
            EventAdmin.list_filter = filters
        self.assertContains(self.response, 'name="id_start"')
        self.assertContains(self.response, 'admin/js/calendar.js', count=1)
        self.assertContains(
            self.response, 'admin/js/admin/DateTimeShortcuts.js', count=1)

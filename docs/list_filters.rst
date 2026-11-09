List filters
============

Change list filters (``list_filter``) are shown as drop-downs in the search bar above the list.


DateRangeFilter
---------------

Filters a date or datetime field by an inclusive "From" / "To" date range, shown as two date inputs with a calendar::

    from suit.filters import DateRangeFilter

    class OrderAdmin(admin.ModelAdmin):
        list_filter = (
            'status',
            ('created_at', DateRangeFilter),
        )

The query string parameters are ``<field>_start`` and ``<field>_end``, for example ``?created_at_start=2026-01-01``. With ``USE_TZ`` the range runs from 00:00 of the "From" date to the end of the "To" date in the current time zone.

The markup comes from the ``admin/date_range_filter.html`` template, which you can override.

``DateRangeFilter`` replaces the separate `django-suit-daterange-filter <https://github.com/f213/django-suit-daterange-filter>`_ package. To switch, change ``from date_range_filter import DateRangeFilter`` to ``from suit.filters import DateRangeFilter``, then remove ``date_range_filter`` from ``INSTALLED_APPS`` and uninstall the package. The parameter names are the same, so saved filter links keep working.

from django.db import models
from django.contrib import admin

from suit.filters import DateRangeFilter


def test_app_label():
    return Book._meta.app_label


class Book(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)


class Album(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class BookAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name',)
    list_display = ('id', 'name',)

    def suit_row_attributes(self, obj, request):
        return {'class': 'suit_row_attr_class-%s' % obj.name,
                'data': obj.pk,
                'data-request': request}

    def suit_cell_attributes(self, obj, column):
        return {'class': 'suit_cell_attr_class-%s-%s' % (column, obj.name),
                'data': obj.pk}


class AlbumAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj):
        """No request defined to test backward-compatibility"""
        return {'class': 'suit_row_album_attr_class-%s' % obj.name,
                'data-album': obj.pk}


class User(models.Model):
    """
    Class to test menu marking as active if two apps have model with same name
    """
    name = models.CharField(max_length=64)


class Event(models.Model):
    name = models.CharField(max_length=64)
    happened_at = models.DateTimeField()

    def __str__(self):
        return self.name


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'happened_at')
    list_filter = (('happened_at', DateRangeFilter),)


admin.site.register(Book, BookAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(User)

# On its own site, so the menu tests' model counts of admin.site don't change
filters_site = admin.AdminSite(name='filters')
filters_site.register(Event, EventAdmin)

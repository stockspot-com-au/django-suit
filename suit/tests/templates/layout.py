import re

from django.contrib import admin
from django.contrib.staticfiles import finders
from django.test import override_settings
from django.urls import reverse
from suit.templatetags.suit_tags import suit_collapsible, \
    suit_fieldset_classes, suit_line_visible
from suit.tests.mixins import ModelsTestCaseMixin, UserTestCaseMixin
from suit.tests.models import Book, test_app_label

app_label = test_app_label()


class CollapsedBookAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )


class LayoutTestCase(ModelsTestCaseMixin, UserTestCaseMixin):
    def setUp(self):
        self.login_superuser()

    def test_logout_is_post_form(self):
        self.get_response()
        self.assertContains(
            self.response,
            '<form id="logout-form" method="post" action="%s">' % reverse('admin:logout'))

    def test_static_files_exist(self):
        urls = (
            reverse('admin:index'),
            reverse('admin:%s_book_changelist' % app_label),
            reverse('admin:%s_book_add' % app_label),
        )
        for url in urls:
            self.get_response(url)
            content = self.response.content.decode()
            for path in re.findall(r'(?:href|src)="/static/([^"?]+)', content):
                self.assertTrue(finders.find(path), '%s not found' % path)

    def test_fieldset_classes_filter(self):
        self.assertEqual(suit_fieldset_classes('wide collapse suit-tab'),
                         'wide suit-tab')
        self.assertEqual(suit_fieldset_classes(None), '')

    def test_collapsible_fieldset(self):
        model_admin = admin.site._registry[Book]
        original = model_admin.fieldsets
        model_admin.fieldsets = (
            ('Main', {'fields': ('name',), 'classes': ('collapse', 'wide')}),
        )
        try:
            self.get_response(reverse('admin:%s_book_add' % app_label))
        finally:
            model_admin.fieldsets = original
        self.assertContains(self.response, '<details class="suit-collapse">')
        self.assertNotContains(self.response, ' collapse"')

    def test_collapsible_fieldset_open(self):
        model_admin = admin.site._registry[Book]
        original = model_admin.fieldsets
        model_admin.fieldsets = (
            ('Main', {'fields': ('name',), 'classes': ('collapse', 'open')}),
        )
        try:
            self.get_response(reverse('admin:%s_book_add' % app_label))
        finally:
            model_admin.fieldsets = original
        self.assertContains(self.response, '<details class="suit-collapse" open>')

    def test_collapsible_fallback(self):
        """Same result as Django 5.1+ is_collapsible on older Django"""
        from django import forms

        class Form(forms.Form):
            name = forms.CharField()
            hidden = forms.CharField(widget=forms.HiddenInput)

        class FakeFieldset:
            classes = 'collapse wide'
            fields = (('name', 'hidden'),)
            form = Form({})

        fieldset = FakeFieldset()
        if hasattr(fieldset, 'is_collapsible'):
            return
        self.assertFalse(suit_collapsible(fieldset))  # "name" has errors
        fieldset.form = Form({'name': 'x', 'hidden': 'y'})
        self.assertTrue(suit_collapsible(fieldset))
        fieldset.classes = 'wide'
        self.assertFalse(suit_collapsible(fieldset))

    def test_line_visible_fallback(self):
        from django import forms

        class Form(forms.Form):
            name = forms.CharField()
            hidden = forms.CharField(widget=forms.HiddenInput)

        class FakeLine:
            form = Form()

            def __init__(self, fields):
                self.fields = fields

        self.assertTrue(suit_line_visible(FakeLine(['name', 'hidden'])))
        self.assertFalse(suit_line_visible(FakeLine(['hidden'])))

    def test_fields_rendered_visible(self):
        self.get_response(reverse('admin:%s_book_add' % app_label))
        self.assertContains(self.response, 'field-name')
        self.assertNotContains(self.response, 'control-group hidden field-name')

    @override_settings(SUIT_CONFIG={'MENU_ICONS': {'auth': 'icon-lock'}})
    def test_legacy_icon_names_supported(self):
        self.get_response()
        self.assertContains(self.response, 'class="icon-lock"')
        self.assertContains(self.response, 'suit/css/glyphicons-compat.css')

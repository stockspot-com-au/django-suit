import itertools
from django import template
from django.contrib.admin.utils import lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from suit.config import get_config
from suit import utils

django_version = utils.django_major_version()

register = template.Library()


@register.filter(name='suit_conf')
def suit_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.tag
def suit_date(parser, token):
    return NowNode(get_config('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(get_config('HEADER_TIME_FORMAT'))


@register.filter
def field_contents_foreign_linked(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance

    # Django links readonly foreign keys itself when it can
    if fieldname not in getattr(admin_field.model_admin,
                                'linked_readonly_fields', ()) \
            or '<a ' in displayed:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj,
                                              admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None

    if isinstance(fieldtype, ForeignKey):
        try:
            url = admin_url(value)
        except NoReverseMatch:
            url = None
        if url:
            displayed = format_html('<a href="{}">{}</a>', url, displayed)
    return mark_safe(displayed)


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.model_name)
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def suit_bc(*args):
    return utils.value_by_version(args)


@register.simple_tag
def suit_bc_value(*args):
    return utils.value_by_version(args)


@register.simple_tag
def admin_extra_filters(cl):
    """ Return the dict of used filters which is not included
    in list_filters form """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys()
                                             for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.filter
def suit_fieldset_classes(classes):
    """
    Drop Django's "collapse" class: Bootstrap hides any element with it.
    Collapsible fieldsets are rendered with <details> instead.
    """
    return ' '.join(c for c in str(classes or '').split() if c != 'collapse')


@register.filter
def suit_collapsible(fieldset):
    """
    Fieldset / inline formset "is_collapsible" (Django 5.1+), with the same
    logic for older Django: has the "collapse" class and no errors.
    """
    if hasattr(fieldset, 'is_collapsible'):
        return fieldset.is_collapsible
    if 'collapse' not in str(getattr(fieldset, 'classes', '') or '').split():
        return False
    formset = getattr(fieldset, 'formset', None)
    if formset is not None and hasattr(fieldset, 'opts'):
        # InlineAdminFormSet
        return not any(formset.errors)
    fields = set()
    for field in fieldset.fields:
        fields.update(field if isinstance(field, (list, tuple)) else [field])
    return not any(field in fields for field in fieldset.form.errors)


@register.filter
def suit_has_class(classes, name):
    return name in str(classes or '').split()


@register.filter
def suit_line_visible(line):
    """
    Fieldline "has_visible_field" (Django 5.0+), with the same logic for
    older Django.
    """
    if hasattr(line, 'has_visible_field'):
        return line.has_visible_field
    return not all(
        field in line.form.fields and line.form.fields[field].widget.is_hidden
        for field in line.fields
    )


@register.simple_tag
def suit_django_version():
    return django_version


@register.filter
def django_version_lt(string):
    return django_version < str_to_version(string)


@register.filter
def django_version_lte(string):
    return django_version <= str_to_version(string)


@register.filter
def django_version_gt(string):
    return django_version > str_to_version(string)


@register.filter
def django_version_gte(string):
    return django_version >= str_to_version(string)


def str_to_version(string):
    return tuple([int(s) for s in string.split('.')])

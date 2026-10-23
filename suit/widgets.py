from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.forms import TextInput, Select, Textarea
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import gettext as _


class NumberInput(TextInput):
    """
    HTML5 Number input
    Left for backwards compatibility
    """
    input_type = 'number'


class HTML5Input(TextInput):
    """
    Supports any HTML5 input
    http://www.w3schools.com/html/html5_form_input_types.asp
    """

    def __init__(self, attrs=None, input_type=None):
        self.input_type = input_type
        super().__init__(attrs)


#
class LinkedSelect(Select):
    """
    Linked select - Adds link to foreign item, when used with foreign key field
    """

    def __init__(self, attrs=None, choices=()):
        attrs = _make_attrs(attrs, classes="linked-select")
        super().__init__(attrs, choices)


class EnclosedInput(TextInput):
    """
    Widget for Bootstrap input groups (prepended/appended add-ons)
    """

    def __init__(self, attrs=None, prepend=None, append=None):
        """
        For prepend, append parameters use string like %, $ or html.
        Icon class names (e.g. "bi bi-envelope" or legacy "icon-envelope")
        are rendered as icons.
        """
        self.prepend = prepend
        self.append = append
        super().__init__(attrs=attrs)

    def enclose_value(self, value):
        """
        If value doesn't starts with html open sign "<", enclose in add-on tag
        """
        if value.startswith("<"):
            return value
        if value.startswith(("icon-", "bi-", "bi ")):
            value = format_html('<i class="{}"></i>', _icon_class(value))
        # Developer supplied value, may contain entities like &euro;
        return mark_safe('<span class="input-group-text">%s</span>' % value)

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if self.prepend:
            output = self.enclose_value(self.prepend) + output
        if self.append:
            output = output + self.enclose_value(self.append)

        return mark_safe(
            '<div class="input-group suit-input-group">%s</div>' % output)


class AutosizedTextarea(Textarea):
    """
    Autosized Textarea - textarea height dynamically grows based on user input
    (handled by suit.js for every textarea.autosize)
    """

    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 2}, "autosize")
        super().__init__(new_attrs)


#
# Original date widgets with addition html
#
class SuitDateWidget(AdminDateWidget):
    template_name = 'suit/widgets/date.html'

    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Date:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vDateField")
        super().__init__(attrs=new_attrs, format=format)


class SuitTimeWidget(AdminTimeWidget):
    template_name = 'suit/widgets/time.html'

    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Time:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vTimeField")
        super().__init__(attrs=new_attrs, format=format)


class SuitSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    template_name = 'suit/widgets/split_datetime.html'

    def __init__(self, attrs=None):
        widgets = [SuitDateWidget, SuitTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)


def _icon_class(value):
    """
    "bi-x" -> "bi bi-x"; "bi bi-x" and legacy "icon-x" are returned as is
    (legacy names are mapped by suit/css/glyphicons-compat.css).
    """
    if value.startswith("bi-"):
        return "bi " + value
    return value


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result

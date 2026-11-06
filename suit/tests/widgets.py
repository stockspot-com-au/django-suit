import re

from django.test import TestCase
from suit.widgets import LinkedSelect, HTML5Input, EnclosedInput, \
    NumberInput, SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget, \
    AutosizedTextarea
from django.utils.translation import gettext as _


def strip_aria(html):
    """Django 6.0+ adds aria-describedby to admin date/time inputs"""
    return re.sub(r' aria-describedby="[^"]*"', '', html)


class WidgetsTestCase(TestCase):
    def test_NumberInput(self):
        inp = NumberInput()
        self.assertEqual('number', inp.input_type)

    def test_HTML5Input(self):
        input_type = 'calendar'
        inp = HTML5Input(input_type=input_type)
        self.assertEqual(input_type, inp.input_type)

    def test_LinkedSelect(self):
        ls = LinkedSelect()
        self.assertTrue('linked-select' in ls.attrs['class'])

    def test_LinkedSelect_with_existing_attr(self):
        ls = LinkedSelect(attrs={'class': 'custom-class', 'custom': 123})
        self.assertEqual('linked-select custom-class', ls.attrs['class'])
        self.assertEqual(ls.attrs['custom'], 123)

    def render_enclosed_widget(self, enclosed_widget):
        return enclosed_widget.render('enc', 123)

    def get_enclosed_widget_html(self, values):
        return '<div class="input-group suit-input-group">%s<input name="enc" ' \
               'type="text" value="123" />%s</div>' % values

    def test_EnclosedInput_as_text(self):
        inp = EnclosedInput(prepend='p', append='a')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="input-group-text">p</span>',
                  '<span class="input-group-text">a</span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_icon(self):
        inp = EnclosedInput(prepend='icon-fire', append='bi-tree')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="input-group-text"><i class="icon-fire"></i></span>',
                  '<span class="input-group-text"><i class="bi bi-tree"></i></span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_html(self):
        inp = EnclosedInput(prepend='<em>p</em>', append='<em>a</em>')
        output = self.render_enclosed_widget(inp)
        result = ('<em>p</em>', '<em>a</em>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_renders_twice(self):
        inp = EnclosedInput(prepend='p')
        self.assertHTMLEqual(self.render_enclosed_widget(inp),
                             self.render_enclosed_widget(inp))

    def test_SuitDateWidget(self):
        sdw = SuitDateWidget()
        self.assertTrue('vDateField' in sdw.attrs['class'])

    def test_SuitDateWidget_with_existing_class_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Date:')[:-1], sdw.attrs['placeholder'])

    def test_SuitDateWidget_with_existing_placeholder_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def get_SuitDateWidget_output(self):
        return '<div class="input-group suit-date"><input type="text" name="sdw" ' \
               'value="" class="vDateField " size="10" placeholder="Date" />' \
               '<span class="input-group-text"><i class="bi bi-calendar3"></i></span></div>'

    def test_SuitDateWidget_output(self):
        sdw = SuitDateWidget(attrs={'placeholder': 'Date'})
        output = strip_aria(sdw.render('sdw', ''))
        self.assertHTMLEqual(
            self.get_SuitDateWidget_output(), output)

    def test_SuitTimeWidget(self):
        sdw = SuitTimeWidget()
        self.assertTrue('vTimeField' in sdw.attrs['class'])

    def test_SuitTimeWidget_with_existing_class_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Time:')[:-1], sdw.attrs['placeholder'])

    def test_SuitTimeWidget_with_existing_placeholder_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def get_SuitTimeWidget_output(self):
        return '<div class="input-group suit-date suit-time"><input type="text" ' \
               'name="sdw" value="" class="vTimeField " size="8" placeholder="Time" />' \
               '<span class="input-group-text"><i class="bi bi-clock"></i></span></div>'

    def test_SuitTimeWidget_output(self):
        sdw = SuitTimeWidget(attrs={'placeholder': 'Time'})
        output = strip_aria(sdw.render('sdw', ''))
        self.assertHTMLEqual(
            self.get_SuitTimeWidget_output(),
            output)

    def get_SuitSplitDateTimeWidget_output(self):
        # Sub widgets of an empty MultiWidget have no value attribute
        dwo = self.get_SuitDateWidget_output().replace('sdw', 'sdw_0').replace(' value=""', '')
        two = self.get_SuitTimeWidget_output().replace('sdw', 'sdw_1').replace(' value=""', '')
        return '<div class="datetime">%s%s</div>' % (
            dwo.replace(' placeholder="Date"', ' placeholder="%s"' % _('Date:')[:-1]),
            two.replace(' placeholder="Time"', ' placeholder="%s"' % _('Time:')[:-1]))

    def test_SuitSplitDateTimeWidget(self):
        ssdtw = SuitSplitDateTimeWidget()
        output = strip_aria(ssdtw.render('sdw', ''))
        self.assertHTMLEqual(
            self.get_SuitSplitDateTimeWidget_output(),
            output)

    def test_AutosizedTextarea(self):
        txt = AutosizedTextarea()
        self.assertTrue('autosize' in txt.attrs['class'])
        self.assertEqual(2, txt.attrs['rows'])

    def test_AutosizedTextarea_with_existing_attrs(self):
        txt = AutosizedTextarea(attrs={'class': 'custom-class', 'rows': 3})
        self.assertTrue('autosize ' in txt.attrs['class'])
        self.assertTrue(' custom-class' in txt.attrs['class'])
        self.assertEqual(txt.attrs['rows'], 3)

    def test_AutosizedTextarea_output(self):
        txt = AutosizedTextarea()
        self.assertHTMLEqual(txt.render('txt', ''), (
            '<textarea class="autosize " cols="40" name="txt" '
            'rows="2">\r\n</textarea>'))

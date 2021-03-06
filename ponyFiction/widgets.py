#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import SelectMultiple, CheckboxSelectMultiple, Widget
from itertools import chain
from django.forms.widgets import CheckboxInput, Input, RadioFieldRenderer, RadioSelect, TextInput
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt


# Убрать при первой возможности
class NumberInput(TextInput):
    input_type = 'number'


class ButtonWidget(Widget):
    def render(self, name=None, value=None, attrs=None):
        attrs = self.attrs
        text = attrs.pop('text', '')
        return mark_safe('<button%s>%s</button>' % (flatatt(attrs), force_unicode(text)))


class ServiceButtonWidget(Input):
    input_type = 'submit'


class StoriesServiceInput(Widget):
    def render(self, name=None, value=None, attrs=None):
        return mark_safe('<input%s />' % flatatt(self.attrs))


class StoriesImgSelect(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        value = [int(x) for x in value]
        output = []
        attrs = self.attrs
        group_container_class = attrs['group_container_class']
        for group, option_sublist in chain(self.choices, choices):
            output.append('<span class="%s%s" title="%s">' % (group_container_class, group.id, group.name))
            for option in option_sublist:
                # *option == (int, string)
                output.append(self.render_option(attrs, name, value, *option))
            output.append('</span>')
        return mark_safe('\n'.join(output))

    def render_option(self, attrs, name, selected_choices, option_value, option_label):
        container_attrs = attrs['container_attrs']
        data_attrs = attrs['data_attrs']
        img_url = staticfiles_storage.url('images/characters/{}.png'.format(option_value))
        img_class = 'ui-selected' if option_value in selected_choices else ''
        item_image = '<img class="%s" src="%s" alt="%s" title="%s" />' % (img_class, img_url, option_label, option_label)
        cb = CheckboxInput(data_attrs, check_test=lambda x: x in selected_choices)
        rendered_cb = cb.render(name, option_value)
        return mark_safe('<span%s>%s%s</span>' % (flatatt(container_attrs), rendered_cb, item_image))

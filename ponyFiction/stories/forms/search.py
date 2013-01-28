# -*- coding: utf-8 -*-
from django.forms import Field, Form, ModelMultipleChoiceField, MultipleChoiceField, TextInput, ChoiceField
from ponyFiction.stories.fields import GroupedModelChoiceField
from ponyFiction.stories.models import Character, Category, Classifier, Rating, Size
from ponyFiction.stories.widgets import ButtonWidget, ServiceButtonWidget, StoriesImgSelect, StoriesCheckboxSelectMultiple, StoriesButtons, StoriesRadioButtons, StoriesServiceInput
from sanitizer.forms import SanitizedCharField

class SearchForm(Form):
    checkbox_attrs={
           'btn_attrs': {'type': 'button', 'class': 'btn'},
           'data_attrs': {'class': 'hidden'},
           'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-checkbox'},
           'data_container_attrs': {'class': 'buttons-data'},
           }
    radio_attrs={
           'btn_attrs': {'type': 'button', 'class': 'btn'},
           'data_attrs': {'class': 'hidden'},
           'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-radio'},
           'data_container_attrs': {'class': 'buttons-data'},
           }
    img_attrs = {
           'group_container_class': 'characters-group group-',
           'data_attrs': {'class': 'hidden'},
           'container_attrs': {'class': 'character-item'}
    }
    # Строка поиска
    search_query = SanitizedCharField(
        required=False,
        widget=TextInput(
            attrs={
               'size': 32,
               'placeholder': 'Пинки-поиск',
               'id': 'appendedInputButtons',
               'class': 'span3',
               'maxlength': 128,
            }
        ),
        max_length=128,
    )
    # Жанры
    categories_select = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=StoriesCheckboxSelectMultiple(
            attrs={
                   'label_attrs': ['checkbox', 'inline', 'gen'],
                   'label_id_related_attr': 'gen-',
                   },
        ),
    )
    # Персонажи
    characters_select = GroupedModelChoiceField(
        required=False,
        queryset=Character.objects.all(),
        group_by_field='group',
        widget=StoriesImgSelect(attrs=img_attrs),
    )
    # Оригинал/перевод
    originals_select = MultipleChoiceField(
        choices=[(0, 'Перевод'),(1, 'Оригинал')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Статус истории
    finished_select = MultipleChoiceField(
        choices=[(0, 'Не завершен'),(1, 'Завершен')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Активность истории
    freezed_select = MultipleChoiceField(
        choices=[(0, 'Активен'),(1, 'Заморожен')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Размеры
    sizes_select = ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Рейтинги
    ratings_select = ModelMultipleChoiceField(
        queryset=Rating.objects.all(),
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # События
    classifications_select = ModelMultipleChoiceField(
        queryset=Classifier.objects.all(),
        required=False,
        widget=StoriesCheckboxSelectMultiple(attrs={'label_attrs': ['checkbox', 'inline']}),
    )
    # Кнопка "Развернуть"
    button_advanced = Field(
        required=False,
        widget=ButtonWidget(
            attrs={
                   'type': 'button',
                   'class': 'btn btn-collapse btn-small',
                   'data-toggle': 'collapse',
                   'data-target': '#more-info',
                   'text': 'Еще более тонкий поиск'
                   }
        ),
    )
    button_submit = Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-primary'}),
        initial='Искать!',
    )
    button_reset = Field(
        required=False,
        widget=StoriesServiceInput(
            attrs={
                   'type': 'reset',
                   'class': 'btn',
                   'id': 'reset_search',
                   'value': 'Очистить',
                   }
        ),
    )
    # Тип поиска
    search_type = ChoiceField(
        choices=[(0, 'Быстрый'), (1, 'Полный')],
        required=True,
        widget=StoriesRadioButtons(attrs=radio_attrs),
    )
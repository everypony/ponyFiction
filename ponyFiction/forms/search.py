# -*- coding: utf-8 -*-
from django.forms import CheckboxSelectMultiple, Field, Form, ModelMultipleChoiceField, MultipleChoiceField, TextInput, ChoiceField, IntegerField, CharField, RadioSelect
from ponyFiction.forms.fields import GroupedModelChoiceField
from ponyFiction.models import Character, Category, Classifier, Rating
from ponyFiction.widgets import NumberInput, ButtonWidget, StoriesImgSelect, StoriesServiceInput


class SearchForm(Form):
    img_attrs = {
        'group_container_class': 'characters-group group-',
        'data_attrs': {'class': 'hidden'},
        'container_attrs': {'class': 'character-item'}
    }
    # Строка поиска
    q = CharField(
        required=False,
        widget=TextInput(
            attrs={
                'size': 32,
                'placeholder': 'Пинки-поиск',
                'id': 'appendedInputButtons',
                'class': 'col-md-3 form-control',
                'maxlength': 128,
            }
        ),
        max_length=128,
    )
    # Минимальный размер
    min_words = IntegerField(
        required=False,
        widget=NumberInput(
            attrs={
                'size': 8,
                'placeholder': 'От',
                'class': 'col-md-3 form-control',
                'maxlength': 8,
                'min': 0,
                'max': 99999000,
            }
        ),
    )
    # Максимальный размер
    max_words = IntegerField(
        required=False,
        widget=NumberInput(
            attrs={
                'size': 8,
                'placeholder': 'До',
                'class': 'col-md-3 form-control',
                'maxlength': 8,
                'min': 0,
                'max': 99999000,
            }
        ),
    )
    # Жанры
    genre = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # Персонажи
    char = GroupedModelChoiceField(
        required=False,
        queryset=Character.objects.all().prefetch_related('group'),
        group_by_field='group',
        widget=StoriesImgSelect(attrs=img_attrs),
    )
    # Оригинал/перевод
    original = MultipleChoiceField(
        choices=[(0, 'Перевод'), (1, 'Оригинал')],
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # Статус рассказа
    finished = MultipleChoiceField(
        choices=[(0, 'Не завершен'), (1, 'Завершен')],
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # Активность рассказа
    freezed = MultipleChoiceField(
        choices=[(0, 'Активен'), (1, 'Заморожен')],
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # Рейтинги
    rating = ModelMultipleChoiceField(
        queryset=Rating.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # События
    cls = ModelMultipleChoiceField(
        queryset=Classifier.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
    )
    # Кнопка "Развернуть тонкие настройки поиска"
    button_advanced = Field(
        required=False,
        widget=ButtonWidget(
            attrs={
                'type': 'button',
                'class': 'btn btn-collapse btn-default',
                'data-toggle': 'collapse',
                'data-target': '#more-info',
                'text': 'Еще более тонкий поиск'
            }
        ),
    )
    # Кнопка "Развернуть фильтры"
    button_filters = Field(
        required=False,
        widget=ButtonWidget(
            attrs={
                'type': 'button',
                'class': 'btn btn-collapse btn-default',
                'data-toggle': 'collapse',
                'data-target': '#more-filters',
                'text': 'Фильтры поиска'
            }
        ),
    )
    # Кнопка "Развернуть сортировку"
    button_sort = Field(
        required=False,
        widget=ButtonWidget(
            attrs={
                'type': 'button',
                'class': 'btn btn-collapse btn-default',
                'data-toggle': 'collapse',
                'data-target': '#more-sort',
                'text': 'Сортировка результатов'
            }
        ),
    )
    # Сортировка
    sort = ChoiceField(
        choices=[(0, 'По релевантности'), (1, 'По дате'), (2, 'По размеру'), (4, 'По комментам')],
        initial=0,
        required=True,
        widget=RadioSelect,
    )

    button_reset = Field(
        required=False,
        widget=StoriesServiceInput(
            attrs={
                'type': 'reset',
                'class': 'btn btn-default',
                'id': 'reset_search',
                'value': 'Очистить',
            }
        ),
    )
    # Тип поиска
    type = ChoiceField(
        choices=[(0, 'По описанию'), (1, 'По главам')],
        initial=0,
        required=True,
        widget=RadioSelect,
    )

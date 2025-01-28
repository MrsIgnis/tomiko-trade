from django import template

register = template.Library()

@register.filter(name='url_startswith')
def url_startswith_filter(value, prefix):
    """ Проверяет, начинается ли строка value с префикса prefix. Возвращает True, если начинается, иначе False."""
    return value.startswith(prefix)

@register.filter
def get_range(value):
    """Возвращает диапазон чисел от 1 до value для итерации в шаблоне."""
    return range(1, value + 1)

@register.filter
def get_empty_range(value):
    """Возвращает диапазон чисел от 1 до 5-value для пустых звезд."""
    return range(1, 6 - value)
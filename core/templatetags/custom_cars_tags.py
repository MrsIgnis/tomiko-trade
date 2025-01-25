from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def engine_format(value):
    """Форматирует объем двигателя из кубических сантиметров в литры"""
    try:
        return f"{float(value)/1000:.3f} л"
    except:
        return "н/д"

@register.filter
def intspace(value):
    """Форматирует число с пробелами вместо запятых (без изменения типа)"""
    try:
        return format(int(value), ',d').replace(",", " ")
    except (ValueError, TypeError):
        return "н/д"
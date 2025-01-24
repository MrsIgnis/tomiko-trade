from django import template

register = template.Library()

@register.filter
def engine_format(value):
    """Форматирует объем двигателя из кубических сантиметров в литры"""
    try:
        return f"{float(value)/1000:.1f} л"
    except:
        return "н/д"
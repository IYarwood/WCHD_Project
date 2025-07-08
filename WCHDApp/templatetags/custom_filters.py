from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr, '')

@register.filter
def money(value):
    return f"${float(value):,.2f}"
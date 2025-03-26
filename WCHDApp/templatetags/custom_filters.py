from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Custom filter to get dictionary value dynamically."""
    return dictionary.get(key, "")

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr, '')
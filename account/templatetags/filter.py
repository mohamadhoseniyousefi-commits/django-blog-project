from django import template



register=template.Library()

@register.filter
def cuter(value,arg):
    return value[:arg]
from django import template

register=template.Library()

@register.inclusion_tag('account/test.html')
def show_result(text):
    return {'text':text}
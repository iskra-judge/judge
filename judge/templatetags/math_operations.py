from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    print(value, arg)
    return value * arg


@register.filter
def divide(value, arg):
    return value / arg

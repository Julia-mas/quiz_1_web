from django import template

register = template.Library()


def negative_value(value):
    return -value


def multi(value, arg):
    return value * arg


def dived(value, arg):
    return value // arg


def expression(value, *args):
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
    return eval(value)

# {% expression '(%1 - 1) * 100 // %2' 45 89 %}
# '(45- 1) * 100 // 89'


register.filter('negative', negative_value)
register.filter('multi', multi)
register.filter('dived', dived)

register.simple_tag(func=expression, name='expression')
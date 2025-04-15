import os
from django import template

register = template.Library()

@register.filter
def basename(path):
    return os.path.basename(path)
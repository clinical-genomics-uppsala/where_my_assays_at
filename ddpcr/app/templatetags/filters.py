from django import template

import json

register = template.Library()

@register.filter
def get_value_from_dict(obj, key):
    return obj[key]

@register.filter
def mod_sequence(sequence):
    if sequence:
        return ' '.join([sequence[i:i+10] for i in range(0, len(sequence), 10)])

@register.filter
def jsonify(obj):
    return json.dumps(obj)

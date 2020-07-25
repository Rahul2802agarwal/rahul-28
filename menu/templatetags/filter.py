from django import template

register = template.Library()

@register.filter
def hash(h, key):
	print(key)
	print(h[key])
	return h[key]
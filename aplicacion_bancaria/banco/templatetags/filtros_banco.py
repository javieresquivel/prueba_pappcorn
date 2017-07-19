from django import template

register = template.Library()

@register.filter(name='get_clase')
def get_clase(transaccion, cliente):
	return transaccion.get_clase(cliente)

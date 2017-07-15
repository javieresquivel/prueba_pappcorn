from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, class_attr):
	if field:
		return field.as_widget(attrs={'class': class_attr})

@register.filter(name='addAttrs')
def addAttrs(field, attrs):
	attrs = attrs.split(";")
	dic = {}
	for a in attrs:
		llave =a.split(",")[0]
		valor =a.split(",")[1]
		dic[llave] = valor
	return field.as_widget(attrs=dic)
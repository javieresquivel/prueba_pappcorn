def datos_generales(request):
	if request.user.is_authenticated():
		return {"usuario_sistema":request.user}
	return {"usuario_sistema":None}
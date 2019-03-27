from django.http import HttpResponse


def secret(request):
	return HttpResponse("Congratulations, you have permission to see this!")
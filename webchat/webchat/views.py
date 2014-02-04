from django.http import HttpResponse
from django.shortcuts import render

def webchat(request):
	return render(request, 'prodromus.html')

def notfound(request):
	return HttpResponse("The page you requested is not found type ip/webchat or localhost/webchat if hosted locally")
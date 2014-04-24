from django.http import HttpResponse
from django.shortcuts import render, redirect


def stats(request):

    return render (request, 'stats.html')
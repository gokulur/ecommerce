from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("Accounts app is working!")
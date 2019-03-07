from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from old import DB_interface


def index(request):
    return render(request, "index.html")





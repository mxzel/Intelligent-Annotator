from django.test import TestCase
from django.http import JsonResponse


# Create your tests here.

def test_connect(request):
    return JsonResponse(data={"training_process": 50, "code": 200, "message": "annotate success"})

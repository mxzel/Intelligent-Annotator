"""IntelligentAnnotator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from annotator import views, affair, tests

urlpatterns = [
    path('', views.index),
    path('index', views.index),

    path('create_project', affair.create_project),
    path('upload_file', affair.upload_file),
    path('fetch_unlabeled_data', affair.fetch_unlabeled_data),
    path('commit_label_data', affair.commit_label_data),
    path('export_project', affair.export_project),

    path('test_connect', tests.test_connect),
]

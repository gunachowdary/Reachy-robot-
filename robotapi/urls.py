from django.urls import path
from .views import parse_command

urlpatterns = [
    path('parse-command/', parse_command, name='parse_command'),
]

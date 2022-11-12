from django.urls import path

from scrapper.views import *

urlpatterns = [
    path('testing', Testing.as_view()),
    path('listOfAllProfiles', ListOfAllProfiles.as_view())
]

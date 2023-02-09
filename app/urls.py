from django.urls import path
from .views import main, treatment_complete,add_wifi
urlpatterns = [
    path('', main, name='main'),
    path('treatment_complete/', treatment_complete, name='treatment_complete'),
    path('add_wifi/', add_wifi, name='add_wifi'),
]

from django.urls import path
from .views import main, treatment_complete,add_wifi, treatment_going_on_A, treatment_going_on_B
urlpatterns = [
    path('', main, name='main'),
    path('treatment_complete/', treatment_complete, name='treatment_complete'),
    path('add_wifi/', add_wifi, name='add_wifi'),
    path('treatment_going_on_A/', treatment_going_on_A, name='treatment_going_on'),
    path('treatment_going_on_B/', treatment_going_on_B, name='treatment_going_on'),
]

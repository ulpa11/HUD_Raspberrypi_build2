from django.urls import path
from .views import main, treatment_page, treatment_complete, add_wifi

urlpatterns = [
    path('', main, name='main'),
    path('treatment/', treatment_page, name='treatment'),
    path('treatment_complete/', treatment_complete, name='treatment_complete'),
    path('add_wifi/', add_wifi, name='add_wifi'),
    
]
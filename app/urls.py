from django.urls import path
from .views import main, treatment_page

urlpatterns = [
    path('', main, name='main'),
    path('treatment/', treatment_page, name='treatment'),

]
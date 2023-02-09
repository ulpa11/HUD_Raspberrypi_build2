from django.shortcuts import render,redirect
#import subprocess for connecting wifi and wifi names
import subprocess
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import requests
import json
#from .tubeA import process_tubeA
#from .tubeB import process_tubeB
import subprocess
from django.urls import reverse

# Create your views here.
def main(request):
    return render(request,'main.html')

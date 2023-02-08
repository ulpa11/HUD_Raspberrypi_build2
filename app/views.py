from django.shortcuts import render,redirect
#import subprocess for connecting wifi and wifi names
import subprocess
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import requests
import json
from .tubeA import tubeA
from .tubeB import tubeB

def main(request):
    # Make a GET request to the API
    url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube&user_id=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    }
    data = requests.get(url, headers=headers)
    data = json.loads(data.text)
    data = {
        'patient_name': str(data['Patient Name']),
        'tube_name': str(data['Tube Name']), 
        'treatment_dose': str(data['Treatment Dose (in Joule)']),
    }
    if request.method=="POST":
        if request.POST.get("refresh-button")=="refresh-button":
            print("refresh")
            return redirect("/")
        elif request.POST.get("start-button")=="start-button":
            print("start")
            #redirect to treatment page
            return redirect("/treatment/")
    return render(request, 'main.html', data)

def treatment_page(request):
        # Make a GET request to the API
    url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube&user_id=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    }
    data = requests.get(url, headers=headers)
    data = json.loads(data.text)
    tube_name = str(data['Tube Name'])
    treatment_dose = str(data['Treatment Dose (in Joule)'])
    data = {
        'patient_name': str(data['Patient Name']),
        'tube_name': str(data['Tube Name']), 
        'treatment_dose': str(data['Treatment Dose (in Joule)']),
    }
    if tube_name=="A":
        #call tubeA function
        try:
            tubeA()
            return redirect ("/treatment_complete/")
        except:
            print("error")
            #redirect to main page
            return redirect ("/")

        
    elif tube_name=="B":
        #call tubeB function
        #tubeB()
        print("tubeB")
    else:
        print("0")
        #redirect to main page
        return redirect("/")
    return render(request, 'treatment.html',data)

def treatment_complete(request):
    return render(request, 'treatment_complete.html')












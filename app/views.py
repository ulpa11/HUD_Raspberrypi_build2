from django.shortcuts import render,redirect
#import subprocess for connecting wifi and wifi names
import subprocess
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import requests
import json
from .tubeA import process_tubeA
from .tubeB import process_tubeB
import subprocess




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
        elif request.POST.get("add-wifi-button")=="add-wifi-button":
            #redirect to add wifi page
            return redirect("/add_wifi/")
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
            process_tubeA()
            return redirect("/treatment_complete/")
        except:
            print("error")
            #redirect to main page
            return redirect ("/")

        
    elif tube_name=="B":
        #call tubeB function
        try:
            process_tubeB()
            return redirect("/treatment_complete/")
        except:
            print("error")
            #redirect to main page
            return redirect ("/")
    else:
        print("0")
        #redirect to main page
        return redirect("/")
    return render(request, 'treatment.html',data)


def treatment_complete(request):
    if request.method=="GET":
        return redirect("/")
    return render(request, 'treatment_complete.html')


def add_wifi(request):
    if request.method=="POST":
        #call wifi name 
        ssid= request.POST.get("wifi_name")
        #call wifi password
        password = request.POST.get("password")
        wpa_supplicant_conf = f"""
                country=US
                ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
                update_config=1
                network={{
                ssid="{ssid}"
                psk="{password}"
                key_mgmt=WPA-PSK
                }}
        """
        try:
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
                f.write(wpa_supplicant_conf)
            subprocess.call(["wpa_cli", "-i", "wlan0", "reconfigure"])
            subprocess.call(["dhclient", "wlan0"])
            return redirect("/")
        except:
            #add message warning that failed to connect to wifi
            messages.warning(request, "Failed to connect to wifi")
            return redirect("/")


    return render(request, 'login.html')






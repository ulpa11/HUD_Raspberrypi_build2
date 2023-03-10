from django.shortcuts import render,redirect
import subprocess
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
import requests
import json
from .tubeA import process_tubeA
from .tubeB import process_tubeB
import subprocess

# Create your views here.
def main(request):
    # Make a GET request to the API
    url = 'https://cyberimpulses.com/MVRC_Phototherapy_Booth/process.php?action=patient_tube&user_id=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    }
    try:
        data = requests.get(url, headers=headers)
        data = json.loads(data.text)
        data = {
            'patient_name': str(data['Patient Name']),
            'tube_name': str(data['Tube Name']), 
            'treatment_dose': str(data['Treatment Dose (in Joule)']),
        }
    except:
        return render(request, 'main.html', {'error_message': 'Internet connection not available. Please check your connection and try again.'})
    
    if request.method == "POST":
        if request.POST.get("refresh-button") == "refresh-button":
            # redirect to main page
            return redirect("/")
        elif request.POST.get("start-button") == "start-button":
            # redirect to treatment page
            # send a message that treatment has started
            try:
                data['overlay_message'] = "Treatment in progress, please wait..."
                data['treatment_ongoing'] = True
                if data['tube_name'] == 'A':
                    return redirect("/treatment_going_on_A/")
                elif data['tube_name'] == 'B':
                    return redirect("/treatment_going_on_B/")
            except:
                return render(request, 'main.html', {'error_message': 'Internet connection not available. Please check your connection and try again.'})
        elif request.POST.get("add-wifi-button") == "add-wifi-button":
            # redirect to add wifi page
            return redirect("/add_wifi/")
    else:
        data['treatment_ongoing'] = False
    return render(request, 'main.html', data)


def treatment_going_on_A(request):
    process_tubeA()
    redirect("/treatment_complete/")

def treatment_going_on_B(request):
    process_tubeB()
    redirect("/treatment_complete/")




def treatment_complete(request):
    if request.method=="POST":
        if request.POST.get("refresh")=="refresh":
            return redirect("/")
    return render(request, 'treatment_complete_page.html')


def add_wifi(request):
    if request.method=="POST":
        if request.POST.get("Connect")=="Connect":
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
        elif request.POST.get("Reload")=="Reload":
            return redirect("/")
    return render(request, 'login.html')
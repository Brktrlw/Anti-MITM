
import os
import time
from pygame import mixer
from datetime import datetime

import scapy.all as scapy

kayit = 0



target_ip = None
ip_address=list()
mac_address=list()
original_modem_mac=None
original_modemIP=None
time.sleep(2)
with os.popen('arp -a') as f:
    data2 = f.read()
sayac=0
macAddressList=list()
for lines in data2.splitlines():
    sayac+=1
    if sayac==4:
        original_modem_mac=lines.split()[1]
        original_modemIP=lines.split()[0]
while True:
    time.sleep(2)
    with os.popen('arp -a') as f:
        data = f.read()

    sayac=0
    macAddressList=list()
    for line in data.splitlines():
        sayac+=1
        if sayac==4:
            modemMac=line.split()[1]
            modemIP=line.split()[0]
        else:
            if line.split()==[]:
                pass
            else:
                if "Internet" in line.split() or "192.168.21.48" in line.split():
                    pass
                else:
                    macAddressList.append(line.split()[1])

    #macAddressList.append(modemMac)
    if modemMac in macAddressList or original_modem_mac!=modemMac:
        mixer.init()
        mixer.music.load('dangerSound.mp3')
        mixer.music.play()
        if kayit == 0:
            with open("logs.txt","a") as file:
                file.write(data)
                file.write("TARİH= "+str(datetime.now()))
                kayit=1

        gateway_ip = modemIP

        for dataline in data.splitlines():
            if dataline.split()==[]:
                pass
            else:
                if "Interface:" in dataline.split() or "Internet" in dataline.split():
                    pass
                else:
                    ip_address.append(dataline.split()[0])
                    mac_address.append(dataline.split()[1])
        arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=original_modem_mac, psrc="192.168.20.1")
        #while True:
        #    scapy.send(arp_response,verbose=0)


    else:
        pass # sakin

    yeniliste=dict(zip(ip_address,mac_address))
    try:
        yeniliste.pop("192.168.20.1")
    except:
        pass
    dict_items = yeniliste.items()
    for key, value in dict_items:
        if value == modemMac:
            target_ip=key
            break











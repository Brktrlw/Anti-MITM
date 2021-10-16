
import os
import time
from pygame import mixer
from datetime import datetime
import scapy.all as scapy
class AntiMITM():
    def __init__(self):
        self.REAL_GATEWAY_MAC=None
        self.REAL_GATEWAY_IP=None
        self.MAC_ADDRESS_LIST=list()
        self.MAC_ADDRESS_LIST_FOR_DETECT_ATTACKER=list()
        self.IP_ADDRESS_LIST=list()
        self.TARGET_MAC_ADDRESS=None
        self.TARGET_IP_ADDRESS=None
        self.ZIP_IP_AND_MAC=None

    def setRealGatewayMac(self):                             # tek bir sefer calısır ve orijinal modem mac adresini ayarlar
        with os.popen('arp -a') as f:
            arpTable = f.read()
        for lines in arpTable.splitlines():
            if lines.split()==[] or "Interface:" in lines.split() or "Internet" in lines.split():
                pass
            else:
                self.REAL_GATEWAY_MAC=lines.split()[1]
                self.REAL_GATEWAY_IP=lines.split()[0]
                break

    def updateMacAddressList(self):
        with os.popen('arp -a') as f:                                      # Mac adreslerin bulunduğu listeyi günceller
            self.arpTable = f.read()
        for lines in self.arpTable.splitlines():
            if lines.split() == [] or "Interface:" in lines.split() or "Internet" in lines.split():
                pass
            else:
                self.MAC_ADDRESS_LIST.append(lines.split()[1])
    def SAVE_LOG(self):      # Log kayıt eder
        with open("logs.txt", "a") as file:
            file.write(self.arpTable)
            file.write("TARİH= " + str(datetime.now())+"\n")
            file.write("SALDIRGAN IP: "+str(self.TARGET_IP_ADDRESS)+"\n")
            file.write("SALDIRGAN MAC:"+str(self.TARGET_MAC_ADDRESS)+"\n")

    def checkArpTable(self):
        while True:
            time.sleep(2)
            if self.REAL_GATEWAY_MAC not in self.MAC_ADDRESS_LIST:                  ######----- SALDIRI YAPILDIĞINDA CALISAN YER -----#####
                self.SAVE_LOG()
                mixer.init()
                mixer.music.load('dangerSound.mp3')
                mixer.music.play()
                os.system("netsh wlan disconnect")
                self.zipIPandMAC()
                self.setTargetMacAddress()
                self.setAttackerIpAddress()
                while True:
                    time.sleep(1)
                #self.ATTACK()
            else:
                self.MAC_ADDRESS_LIST.clear()
                self.updateMacAddressList()

    def setTargetMacAddress(self):
        for lines in self.arpTable.splitlines():
            if lines.split() == [] or "Interface:" in lines.split() or "Internet" in lines.split():
                pass
            else:
                self.TARGET_MAC_ADDRESS=lines.split()[1]
                break

    def zipIPandMAC(self):
        for lines in self.arpTable.splitlines():
            if lines.split() == [] or "Interface:" in lines.split() or "Internet" in lines.split() or self.REAL_GATEWAY_MAC in lines.split():
                pass
            else:
                self.IP_ADDRESS_LIST.append(lines.split()[0])
                self.MAC_ADDRESS_LIST_FOR_DETECT_ATTACKER.append(lines.split()[1])
        self.ZIP_IP_AND_MAC=dict(zip(self.MAC_ADDRESS_LIST_FOR_DETECT_ATTACKER,self.IP_ADDRESS_LIST))

    def setAttackerIpAddress(self):
        self.TARGET_IP_ADDRESS=self.ZIP_IP_AND_MAC.get(self.TARGET_MAC_ADDRESS)


    #def ATTACK(self):
    #    arp_response = scapy.ARP(op=2, pdst=self.TARGET_IP_ADDRESS, hwdst=self.TARGET_MAC_ADDRESS, psrc=self.REAL_GATEWAY_IP)
    #    while True:
    #        time.sleep(1)
    #        scapy.send(arp_response, verbose=0)
    #        print("**********PAKET GÖNERİLDİ**********")

obje=AntiMITM()
obje.setRealGatewayMac()
obje.updateMacAddressList()
obje.checkArpTable()



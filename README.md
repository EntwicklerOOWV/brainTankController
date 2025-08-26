# OOWV b:rainTank Controller

Willkommen in der Dokumentation für das OOWV b:rainTank Controller Repository. Hier erfährst du alles, was du über den Controller zur Steuerung des intelligenten Wassertanks wissen musst. Bisherige Erfahrungsberichte zum Aufbau des b:rainTanks findest du auf der Wiki-Seite des brainTank-Repositorys: https://github.com/EntwicklerOOWV/brainTank/wiki.

## Hardware
#### Controller

Folgende Hardware-Komponenten werden für den Controller benötigt:

- Raspberry Pi Zero W: Ein leistungsstarker Einplatinencomputer.  
https://www.amazon.de/dp/B06XFZC3BX

- SanDisk Ultra Android microSDHC: Zum Speichern des Betriebssystems und der Daten.  
https://www.amazon.de/dp/B08GY9NYRM

- AZDelivery 2-Relais Modul 5V: Für die Schaltung von Geräten.  
https://www.amazon.de/dp/B078Q326KT

- Aufwärtswandler XL6009(3V-32V zu 5V-35V): Zur Spannungsanpassung.  
https://www.amazon.de/dp/B00HV59922

- Füllstandssensor (TL-136): Misst den Wasserstand im Tank.  
https://www.amazon.de/dp/B08YWQJM1T

- Analog-zu-Digital-Wandlermodul ADS1115: Konvertiert analoge Signale in digitale Werte.  
https://www.amazon.de/dp/B09135KBLT

- Strom zu Spannungsmodul (4-20Ma Bis 0-3.3V 5V 10V): Wandelt Strom in Spannungsbereich um.  
https://www.amazon.de/dp/B07TWLG37N

- Verteilerdose zum Verstauen der Hardware-Komponenten (zb OBO Abzweigkasten Aufputz 150mm x 116mm grau IP 66)  
https://www.amazon.de/dp/B001JMRTTS

- Micro USB Netzteil (Raspberry Pi 5V 3A Netzteil)  
https://www.amazon.de/dp/B07TZ89BT7

- Micro-USB Kabel (falls nicht am Netzteil fest verbaut)   
[https://www.amazon.de/Micro-USB-Kabel](https://www.amazon.de/SIZUKA-Android-Ladekabel-Samsung-Motorola/dp/B0C8FZZB83/ref=sr_1_2_sspa?crid=18JZDVGTAZ84I&dib=eyJ2IjoiMSJ9.tgUxGIZXu7CT_CqNh4L2RK1r1yl5I0rOkRfafcormg9KoHfjh2jO4Wib_hQbTjumhHH237coBzgvvZXOLYstX28CrSNaS4T_O7NoVWbbCI5wcycZI28uM3ZritixZmINQAOWxBOTZl4UbobRky2dh08ozOaK-uQ3TYDmjiFI_eL3eJwcoxr2h2yrchai7S-vWwm-9SL5Qm2rudbFnznjCTjHOsiZERagDVsXfweXnYrZLDu--Qqnqy8KkASS55P0tunAt5FbRshVFHzxF_5gcXd1VtymJ22Owm9JmBNGyPM.8mpHCAX_ZXfaOZCFckNmbZelnXsBb9fAWRbrSEOsL5o&dib_tag=se&keywords=micro+usb+kabel&qid=1753949779&s=ce-de&sprefix=micro+usb%2Celectronics%2C104&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)

- Jumperkabel und lose Kabel für längere Verbindungen  
https://www.amazon.de/dp/B01EV70C78/

- Aderendhülsen und Crimpzange  
https://www.amazon.de/dp/B0BMWSN4D3/

- Lüsterklemmen  
https://www.amazon.de/dp/B007CWCQ74

- Pins bzw. Pinleisten für ADS1115 Spannungswandler (normalerweise im Lieferumfang enthalten)   
[https://www.amazon.de/Lötleisten](https://www.amazon.de/ANGEEK-stiftleisten-l%C3%B6tleisten-Raspberry-Elektronik/dp/B07XM71CHT/ref=sr_1_6?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1NIZKREKBD7GD&dib=eyJ2IjoiMSJ9.9S4dcSq_QjxNncwZaJt6LTGATB6HTyCHZNlH-K3U1MKjFSG5gDPKuxwj0o_a8K7fWh_sl9a8gbCQpPdcils92tCTMhIzeudcdyJCuJ6ThsjvLUwPb1DUbYokasb9846YlbER7k7yX7wyWHofW2oDyqUr_6-QpjUh4uwdPd1xTChZUAcjmbo7tIkAGHSSSiv3b7JGeC_HVsf3eonbxGrutag1UxjajZcoM-LCoJ0aX9fuNQCrbff2BSirmBFQPgk63oz1sHBWKoBHG5C-kT1MyDR4wruT6BXMKE7fGVRZOOWCyiV35cn4yT0ONeYiu0NsRWTeex7SiESJyaY2z_AIYT8iwzsbDOb299MBeOrODzwQabKv0-5vV_b98eI1P4Oa87B5ES8PkZceVST_t0vUIKoWVgZR8HH0b2uVDXzdvHVrLYijlKk8ysqwMHN_Crg4.kLCXiDF3kkZJHjMRCtYEKmcrmO6StLA3hZ7uoG_QCQU&dib_tag=se&keywords=pinleiste&qid=1742462745&sprefix=pinleiste%2Caps%2C97&sr=8-6)

- Schrauben/Heißkleber zur Befestigung der Komponenten

- Lötkolben   
[https://www.amazon.de/Lötkolben](https://www.amazon.de/Elektronik-Temperatur-Einstellbar-Entl%C3%B6tpumpe-L%C3%B6tkolbenst%C3%A4nder/dp/B09B3GRVTM/ref=sr_1_3?crid=3EXPYM1LJGQYR&dib=eyJ2IjoiMSJ9.abVn_XEgvMuBFGfbU5uaixAkAtnBBpki96VHzfbOMw_-0BM8_a84_T5tZ_0daC6tBkkgpbhJEc2cBZoBAFSQKlCxSotNv9Yqgd_9HFXx3u_5FZyBHiNGX4UmSGGp2UFuETklwzbtFc3VwYTTenneDQywUtyQSuqGjAlNFUQrg6ZwUEndnT03QezLOiYQ5d-0SnqpiyqXxPZ_-M42gNPY-P14BEA_h_1UpddzhviPKNA.r-qHzufBw55KadKprDmLHdEaIZMhvzJJcyZSzIBiTbo&dib_tag=se&keywords=l%C3%B6tkolben&qid=1742463362&sprefix=l%C3%B6%2Caps%2C154&sr=8-3)

- Digitalmultimeter   
https://www.amazon.de/Crenova-Automatisch-Pr%C3%BCfvorrichtung-LCD-Anzeige-Hintergrundlicht/dp/B01825GBK2

#### Wassertank

- 1000L IBC Container  
https://www.rekubik.de/ibc-container/neue-ibc/1000l-ibc-container-rebottled-food-auf-stahlpalette-neuwertig?number=RK50122

- IBC Adapter S60x6 - 2-fach 1" Kugelhahn mit 3/4" Tülle  
https://www.rekubik.de/ibc-zubehoer/adapter/s60x6-grobgewinde/ibc-adapter-s60x6-2-fach-1-kugelhahn-mit-3/4-tuelle-geka-kompatibel

- Motorkugelhahnventil  
https://www.amazon.de/dp/B07V2VX76C

<br>

---

## Installation

#### Installation des Raspberry Pi Zero

Um das Raspberry Pi OS auf dem Raspberry zu installieren empfiehlt sich der [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

Als Betriebssystem sollte das Raspberry Pi OS (32-bit) ausgewählt werden und als Speichermedium die jeweilige mit dem PC verbundene SD-Karte.
![Erweiterte Optionen im Rasperry Pi Imager](./docs/pi-os-overview.png)
Unter den Erweiterten Optionen (Zahnrad im oberen Bild unten rechts) müssen anschließend ein Hostname gesetzt werden sowie die SSH Option aktiviert werden und dafür Benutzername und Passwort für die Anmeldung des SSH Clients erstellt und notiert werden.
Für die Verbindung mit einem Netzwerk müssen noch die benötigten Daten eingetragen werden.
Abschließend muss unter den Spracheinstellungen noch die Zeitzone Europe/Berlin gewählt werden.
![Erweiterte Optionen im Rasperry Pi Imager](./docs/pi-os-install-1.png)


Anschließend kann die Installation gestartet werden.

<br>

---

#### Zugriff auf den Raspberry Pi mittels SSH Terminal
Nach Abschluss der Installation des OS auf der SD Karte, kann diese anschließend in den Kartenslot des Raspberry gesteckt und der Raspberry mittels USB mit einem Computer oder einer anderen 5V Stromquelle verbunden werden.
Nachdem der Raspberry erfolgreich hochgefahren ist, kann über auf den Pi mittels SSH Verbindung zugegriffen werden. Dafür müssen sich der Pi und Computer im selben WLAN befinden.


#### Powershell
```
ssh <benutzername>@<raspberrypi-netzwerk-ip>
<benutzername>@<raspberrypi-netzwerk-ip>'s password:<passwort>
```

#### Termius
Um mit dem Raspberry PI zu kommunizieren kann ein Service wie Termius verwendet werden. Dieser bietet eine SHH- sowie eine SFTP-Funktion um Dateien einfach auf den Raspberry Pi zu laden.
Dazu muss zunächst über die Benutzeroberfläche ein entsprechender Host erstellt werden. Diesem müssen die IP des Kontrollers sowie Benutzername und ein geeigneter SSH Key hinterlegt werden.
Anschließend kann das Verzeichnis des Raspberry direkt ausgewählt werden.
![Erweiterte Optionen im Rasperry Pi Imager](./docs/oowv-termius.png)
Dort können die Dateien geöffnet werden und nach abschließendem speichern auch wieder hochgeladen werden (siehe unten).  
![Erweiterte Optionen im Rasperry Pi Imager](./docs/oowv-termius-update.png)
<br>

---

#### Ändern des Netzwerks
Falls sich nach der Installation das Netzwerk ändert, muss die SD Karte aus dem Pi entfernt und mit dem Computer verbunden werden. Im Grundverzeichnis muss anschließend eine Datei namens ***wpa_supplicant.conf*** mit folgendem Inhalt hinterlegt werden:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE
network={
   ssid="WLAN-SSID"
   psk="WLAN-PASSWORT"
}
```
Anschließend kann der Pi mit eingelegter SD-Karte neugestartet werden.

<br>

---

#### Aktualisierung des Raspberry Pi

Um die auf dem Gerät installierten möglicherweise veralteten Pakete zu aktualisieren, muss zu nächst mittels SSH wie oben beschrieben auf den Raspberry Pi zugegriffen werden.
Anschließend können die Pakete mit folgenden Befehlen aktualisiert werden. Dies kann einige Zeit in Anspruch nehmen. Gelegentlich muss der Forgang zb. mit der Eingabe von "y" bestätigt werden.
```
sudo apt update
sudo apt full-upgrade
sudo apt-get install libopenblas-dev
```
Da der Analog-zu-Digitalwandler über den seriellen Kommunikationsbus I2C mit dem Raspberry kommuniziert,
muss dieser auf dem Pi noch eingeschaltet werden.
```
sudo raspi-config
```
Im Konfigurationsmenü navigiere zu "Interfacing Options" (Schnittstellenoptionen) und wähle "I2C".
Bestätige die Aktivierung des I2C-Interfaces.

![Raspberry Pi I2C aktivieren](./docs/raspi-interface-config.png)

Starte den Raspberry Pi anschließend neu, damit die Änderungen wirksam werden:
```
sudo reboot
```

<br>

---

#### Installation des Quellcodes auf dem Raspberry Pi

Um den Quellcode auf dem Raspberry Pi zu installieren muss folgender Befehl im Verzeichnis **/home/user** (user steht für den gewählten Benutzernamen) ausgeführt werden:

```
git clone https://github.com/EntwicklerOOWV/brainTankController.git
```


Anschließend dürfte das Verzeichnis brainTankController unter **/home/user/brainTankController** zu finden sein. Ist dies der Fall wechselst du anschließend mit folgenden Befehlen aus **/home/user** in das Verzeichnis wechseln und dort die Installation starten. Diese kann einige Minuten in Anspruch nehmen.

```
cd brainTankController
sudo chmod +x setup.sh
sudo ./setup.sh
```

<h5>Hinweis:</h5>
Um zu überprüfen in welchem Verzeichnis du dich aktuell befindest oder um ein Verzeichnis zurück oder in ein spezifisches Verzeichnis zu wechseln, kannst du folgende befehle verwenden

```
dir
cd ..
cd Verzeichnisname
```

<br>

---


#### Speicheraddresse des ADS1115 Moduls
Damit der Analog-zu-Digitalwandler über den I2C Bus angesprochen werden kann, muss die Speicheraddresse des Moduls bekannt sein.
Diese kann mittels folgendem Befehl ausgelesen werden. Dafür muss der Kontroller vollständig zusammengebaut und verkabelt sein damit alle Komponenten korrekt erkannt werden.
```
sudo i2cdetect -y 1
```
Der dort ausgegebene Wert ist die sogenannte Speicheradresse des ADS1115 Moduls. Diese muss anschließend in die Datei *brainTankController/modules/hardware.py* in Zeile 31 eingetragen werden. 
Überlicherweise ist der Wert 0x48 oder 0x49.
```
ADS1115_ADDRESS = 0x48
```

Um die Datei auf direkt dem Rasperry Pi zu bearbeiten kann der Nano oder Vim Editor verwendet werden. 
```
sudo nano hardware.py
```
Alternativ kann die Datei kann mittels des SFTP-Clients Termius in einem beliebigen Editor auf dem Computer bearbeitet und anschließend wieder auf den Raspberry Pi geladen werden.
Falls in der Ausgabe keine Addresse angezeigt wird, muss das Modul nochmal überprüft werden da es nicht korrekt erkannt wurde.

<br>

---

#### Testen des Programms
Um das Programm auch für den Zusammenbau der Hardware zu testen und die Konsolenausgaben direkt zu sehen, 
kann es im Verzeichnis *venv/brainTankController* wie folgt ausgeführt werden. Dafür muss die virtuelle Umgebung aktiviert sein.
```
python oowvcontroller.py
```
Das Programm kann mit der Tastenkombination *Strg + C* beendet werden.
<br>

---

#### Installation des Services
Damit die Controller-Software automatisch ausgeführt wird sobald der Controller gestartet wird, wurde während der Installation ein Linux Service eingerichtet. Dieser läuft im Hintergrund und startet sich bei einem Neustart des Raspberry Pi ebenfalls neu.

Falls es im Verlauf zu Problemen kommt, kann entweder der Raspberry neugestartet werden oder der Service mit folgenden Befehlen neugestartet oder Informationen über den Status des Service ausgegeben werden.
```
sudo systemctl restart oowv-controller.service
sudo systemctl status oowv-controller.service
```

Mit folgenden Befehlen lässt sich der Service entweder stoppen oder die letzten Logeinträge ausgeben.
```
sudo system ctl stop oowv-controller.service
sudo journalctl -f -u oowv-controller.service
```

<br>

---

### Aufbau der Hardware

Für die Konstruktion des Controllers werden neben den Komponenten noch weiteres Werkzeug und Bauteile benötigt:
- Lötkolben und Lötzinn
- Kabel und Lüsterklemmen
- Aderendhülsen und Crimpzange
- Multimeter

#### Controller

Zu Beginn empfiehlt es sich die Komponenten lose in der Dose anzuordnen und anschließend zB. mit einer Heißklebe Pistole zu befestigen.
Alternativ können die Komponenten auch auf einem Perfboard verlötet und dieses anschließend in der Dose befestigt werden.
Einige Komponenten müssen bevor Kabel an die Pins angeschlossen werden können noch mit der jeweils mitgelieferten Stifleiste verlötet werden.
Anschließend können die Öffnungskappen der Dose für den Stecker des Netzteils sowie Kabel des Ventils und Wassersensors entfernt und die Kabel bzw. Stecker in den Öffnungen befestigt werden.

Danach können die Kompononenten nach dem Schaltplan miteinander verkabelt werden.

![Schaltplan 1 mit Stromzufuhr über USB](./docs/schaltplan.png)
Schaltplan mit Stromversorgung über Netzteil

![Die verkabelten Komponenten](./docs/wired.png)
Die verkabelten Komponenten.

![Die verkabelten Komponenten in der Verteilerdose](./docs/box-wired.png)
Die verkabelten Komponenten in der Verteilerdose

![Der vollständige Controller mit Sensor und Ventil](./docs/closed-controller.png)
Der vollständige Controller mit Sensor und Ventil

<br>

---

#### Stromversorgung
Wie im Schaltplan zu sehen, wird der Raspbery Pi über ein Micro USB Kabel mit Strom versorgt. 
Dieses Kabel kann für die Entwicklung zwar an einen Laptop angeschlossen werden, 
sobald der Controller allerdings im Freien steht, sollte der Pi entweder über ein Batteriepack 
oder ein 5V/3A Netzteil mit Strom versorgt werden.

<br>

---

#### Aufwärtswandler
Um das Ventil sowie den Sensor mit 24V zu versorgen muss der Aufwärtswandler auf 5V Eingangsspannung und 24V Ausgangsspannung eingestellt werden.
Dies geschieht durch Drehen des kleinen Rädchens auf dem Modul.
Zur Überprüfung des Spannungsverhältnisses misst man mittels Multimeter den Spannungsabfall zwischen Eingangs- und Ausgangsspannung.

<br>

---

#### Strom-zu-Spannungswandler
Mittels des Spannungswandlers wird der Strom des Wassersensors in eine Spannung umgewandelt. Desweiteren kann über den Wandler ein Spannungsmaximum für den gefüllten Tank und ein Spannungsminimum für den leeren Tank eingestellt werden.
Beim Spannungswandler geschieht dies ebenfalls über die Drehrädchen auf dem Modul. Während sich das Spannungsminimum sehr leicht simulieren lässt indem der Wassersensor nicht eingetaucht ist und somit über das ZERO Rädchen auf ein Spannungsminimum von 0V eingestellt werden kann, muss für das Spannungsmaximum der Wassersensor 1 Meter tief in Wasser eingetaucht werden. Dafür legt man den Wassersensor in ein Kunststoffrohr (HT-Rohr) und befüllt dieses auf 1 Meter mit Wasser. Anschließend kann über das SPAN Rädchen das Spannungsmaximum auf 3,3V eingestellt werden. 
Zur Überprüfung der Spannungen empfiehlt sich hier die Verwendung eines Multimeters indem man den Spannungsabfall auf dem Spannungswandler zwischen GND und VOUT misst.

<br>

---

#### Pumpe und ShellyPlug

Um die Entleerung des Wassertanks zu beschleunigen wird eine zusätzliche Pumpe verwendet. 
Da das Betreiben einer Pumpe mit einer hohen Spannung in der Nähe einer Wasserquelle gefährlich ist, kann ein ShellyPlug verwendet werden. 
Die Installation des ShellyPlugs setzt sich aus folgenden Schritten zusammen:

1. Installation der Shelly App auf dem Smartphone
2. Verbindung via Bluetooth und aktivieren der statischen IP über WIFI "Set static IP address"
2. Einfügen des folgenden Programms in das Verzeichnis *venv/brainTankController/modules* mittels "nano smartplug.py". Die IP muss durch die jeweilige IP ersetzt werden.
```python
import requests

#IP-Adresse der Steckdose ersetzen
shelly_ip = "192.168.178.62"

#Funktion zum Einschalten der Steckdose
def schalte_steckdose_ein():
    url = f"http://{shelly_ip}/relay/0?turn=on"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return

#Funktion zum Ausschalten der Steckdose
def schalte_steckdose_aus():
    url = f"http://{shelly_ip}/relay/0?turn=off"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    
    
while True:
command = input("command: ")
if command== "1":
    schalte_steckdose_ein()
if command == "2":
    schalte_steckdose_aus()
```

3. Öffnen der Datei "hardware.py" im Pfad *venv/brainTankController/modules* und Einfügen von:
```python
#Einfügen in Zeile 1  
import smartplug

#Einfügen unter Zeile 42 relay_open()
smartplug.schalte_steckdose_ein()

#Einfügen unter Zeile 45 relay_close()
smartplug.schalte_steckdose_aus()
```
Beim Einfügen der Funktionen ist auf die korrekte Einrückung mit vier Leerzeichen zu achten.

---
#### Wassertank

Nach dem Zusammenbau des Controllers kann dieser am eigentlichen Wassertank installiert werden. Dabei sollte darauf geachtet werden, dass der Controller sowie das Netzteil vor Regen geschützt und die Kabelverbindungen gut isoliert sind.

![Das Motor-Ventil am Wassertank.](./docs/ventil-horizontal.png)  
Das Motor-Ventil am Wassertank.

![Der Wassertank mit Motor-Ventil und Controller](./docs/tank-front.png)  
Der Wassertank mit Motor-Ventil und Controller

---

## Acknowledgements

* [The Raspberry Pi Platform](https://www.raspberrypi.com)

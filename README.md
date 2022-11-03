# OCR-AIC-06
OCR-AIC-06 - "Participez à la vie de la communauté Open Source"

### Généralités ###
Le script Debian-LAMP-DHCP-DNS.py est rédigé en Python.
Il est fonctionnel sur une version récente de Debian (testé sur versions 10 et 11) et exécutable tant pas le compte root que par un "compte sudo".

### Objectif principal ###
Sur la machine sur laquelle il est lancé, ce script a pour objectif d'installer et de configurer :
- un serveur DHCP
- un serveur DNS lié au DHCP (Dynamic DNS) 

Les configurations dépendent des choix renseignés par l'utilisateur lors d'un questionnaire initial :
- nom de la machine
- nom du domaine
- adresses IP de la machine et de sa passerelle, masque de sous-réseau
- étendue du "pool" DHCP

### Option (L)AMP ###
Le script donne également le choix à l'utilisateur d'installer :
- Apache
- MariaDB
- PHP (version proposée par les dépôts de debian.org)

# OCR-AIC-06
OCR-AIC-06 - "Participez à la vie de la communauté Open Source" - Version du 27 octobre 2022

### Environnement d'exécution ###
Le script Debian-LAMP-DHCP-DNS.py est :
- rédigé pour être lancé par Python3 
- fonctionnel sur une version récente de Debian (testé sur versions 10 et 11)
- exécutable tant par le compte "root" que par un "compte sudo"


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
- PHP (version des dépôts standards de Debian)


### Méthode d'exécution du script ###
1. Charger le script sur la machine cible
2. Au choix :
    1. Rendre le script exécutable, puis le lancer :<br>
          chmod +x Debian-LAMP-DHCP-DNS.py<br>
          ./Debian-LAMP-DHCP-DNS.py<br>
    2. Le faire exécuter par python3 :<br>
          python3 Debian-LAMP-DHCP-DNS.py

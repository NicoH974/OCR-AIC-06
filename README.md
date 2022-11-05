# OCR-AIC-06
OCR-AIC-06 - "Participez à la vie de la communauté Open Source" - Version du 5 novembre 2022
> Projet sous [**GNU General Public License v.3.0**](LICENSE.md)

### Environnement d'exécution ###
Le script Debian-LAMP-DHCP-DNS.py est :
- destiné à être traité par Python3 
- fonctionnel sur une version récente de Debian (testé sur versions 10 - Buster et 11 - Bullseye)
- exécutable tant par le compte "root" que par un "compte sudo"


### Objectif principal ###
Sur la machine sur laquelle il est lancé, ce script a pour objectif d'installer et de configurer :
- un serveur DHCP, avec un pool
- un serveur DNS lié au DHCP (Dynamic DNS) 

Les configurations dépendent des choix renseignés par l'utilisateur dans un questionnaire initial (il est nécessaire de respecter le modèle de réponse proposé entre crochets, sous peine de dysfonctionnement) :
- nom de la machine
- nom du domaine
- adresses IP de la machine et de sa passerelle, la première étant notée avec son masque de sous-réseau au format CIDR
- étendue du "pool" DHCP


### Option (L)AMP ###
Le script donne également le choix à l'utilisateur d'installer :
- Apache
- MariaDB
- PHP (version des dépôts standards de Debian)


### Méthode d'exécution du script ###
1. Charger le script sur la machine cible
2. Au choix :
    1. Rendre le script exécutable, puis le lancer :
        ```
        chmod +x Debian-LAMP-DHCP-DNS.py
        ./Debian-LAMP-DHCP-DNS.py
        ```
    2. Le faire exécuter par python3 :
        ```
        python3 Debian-LAMP-DHCP-DNS.py
        ```

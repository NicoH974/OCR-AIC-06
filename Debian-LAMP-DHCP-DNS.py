#!/usr/bin/python3

###########
# Modules #
###########

from fileinput import close
import os, re, shutil
from subprocess import check_call, STDOUT

#################
### Fonctions ###
#################

# Exécute la commande Linux saisie en paramètre, sans sortie écran
def deb_cmd(cmd):
  check_call(cmd.split(' '), stdout=open(os.devnull,'wb'), stderr=STDOUT)

# Installe le 'package' saisi en paramètre
def deb_inst(pkg):
  deb_cmd("apt-get install -y " + pkg)

# Formate la proposition d'install. des éléments (L)AMP et teste la réponse 
def tst_rep(nom):
  rep = 0
  while rep not in oui+non:
    rep = input (' - ' + nom + ' [O|n] : ').lower()
    if rep in oui:
      return 'o'

# Affiche une ligne séparatrice
def print_ligne(txt = '#', nb = 49):
  print ('\n' + txt * nb + '\n')

# Formate l'affichage de l'avancée des tâches
def txt_justif(txt):
  print ('### ' + txt + (42 - len(txt)) * ' ' + '###')

#############
# Variables #
#############

print_ligne()
print("> Choix de la configuration système et réseau :")

# Noms
srv_name = input ("Nom du serveur ['DebServer'] : ") or "DebServer"
dom_name = input ("Nom du domaine ['nico.lan']  : ") or "nico.lan"

# Configuration IP
net_cidr = int(input ("Masque au format CIDR [24]   : ") or 24)
net_part = input ("IP - NetID ['192.168.40']    : ") or "192.168.40"

srv_addr = input ("IP - HostID de cet hôte [3]  : ") or 3
gw_addr  = 2

# Carte réseau
nic_list = os.listdir('/sys/class/net/')
if nic_list[0] == "lo":
  nic_name = nic_list[1]
else:
  nic_name = nic_list[0]

# Serveur DHCP
dhcp_deb = input ("Plage DHCP - Début [51]      : ") or 21
dhcp_fin = input ("Plage DHCP - Fin   [70]      : ") or 70

# Listes
oui = ['oui', 'o', 'yes', 'y', '']
non = ['non', 'n', 'no']
files2bak = ['network/interfaces', 'resolv.conf', 'default/isc-dhcp-server', 'dhcp/dhcpd.conf', 'bind/named.conf', 'bind/named.conf.local', 'bind/named.conf.options']

###########################
### Variables calculées ###
###########################

# Masque décimal
msk_bin = net_cidr * '1' + (32 - net_cidr) * '0'
t       = re.findall('.{1,8}', msk_bin)

for i in range(4):
  t[i] = int(t[i], 2)

net_mask = "{0}.{1}.{2}.{3}".format(t[0], t[1], t[2], t[3])

# Masque ARPA
t        = net_part.split('.')
net_arpa = "{2}.{1}.{0}".format(t[0], t[1], t[2])

###########################
### Installation LAMP ? ###
###########################

print_ligne()
print('> Choix des éléments à installer :')
inst_lAmp = tst_rep('Apache2')
inst_laMp = tst_rep('MariaDB')
inst_lamP = tst_rep('PHP    ')
print_ligne()

###################################
# Install. paquets et sauvegardes #
###################################

# Mises à jour apt-get
txt_justif("apt update")
deb_cmd("apt-get update")

txt_justif("apt full-upgrade")
deb_cmd("apt-get -y full-upgrade")

# Installations DHCP, DNS, (L)AMP
txt_justif("Installation DHCP (isc) et DNS (bind)")
deb_inst('isc-dhcp-server')
deb_inst('bind9')

if inst_lAmp == 'o':
  txt_justif("Installation d'Apache2")
  deb_inst('apache2')

if inst_laMp == 'o':
  txt_justif("Installation de MariaDB")
  deb_inst('mariadb-server')

if inst_lamP == 'o':
  txt_justif("Installation de PHP")
  deb_inst('php')
  deb_inst('libapache2-mod-php')
  os.system('service apache2 restart')
  if inst_laMp == 'o':
    deb_inst('php-mysql')

# Sauvegarde des fichiers de conf. qui seront modifiés, duplication clé RNDC
txt_justif("Sauvegarde des fichiers conf originels")
for f in files2bak:
  shutil.copy('/etc/' + f, '/etc/' + f + '.bak')

shutil.copy('/etc/bind/rndc.key', '/etc/dhcp/rndc.key')

###############################
# Configuration de la machine #
###############################

print_ligne()
txt_justif("Configuration machine")

### Nom, domaine
os.system("hostnamectl set-hostname {0}".format(srv_name))

file=open('/etc/hosts', 'w')
str=["""
127.0.0.1       localhost
127.0.1.1       {0}.{1}      {0}
""".format(srv_name, dom_name)]
file.writelines(str)
file.close()

### Interfaces réseau
file=open("/etc/network/interfaces",'w')
str=["""# Extensions
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto {0}
allow-hotplug {0}
iface {0} inet static
        address {1}.{2}/{3}
        gateway {1}.{4}
""".format(nic_name, net_part, srv_addr, net_cidr, gw_addr)]
file.writelines(str)
file.close()

### DNS
file=open("/etc/resolv.conf",'w')
str=["""source {0}
search {0}

nameserver {1}.{2}
nameserver 8.8.8.8
""".format(dom_name, net_part, srv_addr)]
file.writelines(str)
file.close()

#################################
# Configuration du service DHCP #
#################################

txt_justif("Configuration serveur DHCP")

### Fichier principal
file=open("/etc/dhcp/dhcpd.conf", 'w')
str=["""option domain-name "{0}";
option domain-name-servers {1}.{2}, 8.8.8.8;

default-lease-time 600;
max-lease-time 7200;

ddns-updates on;
ddns-update-style interim;

subnet {1}.0 netmask {3} {{
  range {1}.{5} {1}.{6};
  option routers {1}.{4};

  include "/etc/dhcp/rndc.key";

  zone {0}.{{
    primary {1}.{2};
    key rndc-key;
  }}

  zone {7}.in-addr.arpa.{{
    primary {1}.{2};
    key rndc-key;
  }}
}}""".format(dom_name, net_part, srv_addr, net_mask, gw_addr, dhcp_deb, dhcp_fin, net_arpa)]
file.writelines(str)
file.close()

### Interface(s) à l'écoute
file=open("/etc/default/isc-dhcp-server", 'w')
file.writelines('INTERFACESv4="{0}"'.format(nic_name))
file.close()

os.system('service isc-dhcp-server restart 2> /dev/null')

################################
# Configuration du service DNS #
################################

txt_justif("Configuration serveur DNS")

### Prise en charge de la clé RNDC
file=open("/etc/bind/named.conf", 'a')
file.writelines('include "/etc/bind/rndc.key";')
file.close()

### Déclaration des zones
file=open("/etc/bind/named.conf.local", 'w')
str=["""zone "{0}" IN {{
        type master;
        file "/var/lib/bind/db.{0}";
        allow-update {{key "rndc-key";}};
}};
zone "{2}.in-addr.arpa" {{
        type master;
        file "/var/lib/bind/db.{1}";
        allow-update {{key "rndc-key";}};
}};
""".format(dom_name, net_part, net_arpa)]
file.writelines(str)
file.close()

### Redirecteurs
file=open("/etc/bind/named.conf.options", 'w')
str=["""options {
        directory "/var/cache/bind";

        forwarders {
		8.8.8.8;
		8.8.4.4;
        };

        dnssec-validation auto;
};"""]
file.writelines(str)
file.close()

### Zone de recherche directe
file=open("/var/lib/bind/db."+dom_name, 'w')
str=["""$ORIGIN {0}.
$TTL    604800
@       IN      SOA     {1}. root.{1}. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@     IN  NS  {1}.
{1}     IN  A {2}.{3}
dns     IN  A {2}.{3}
gw      IN  A {2}.{4}
""".format(dom_name, srv_name, net_part, srv_addr, gw_addr)]
file.writelines(str)
file.close()

### Zone de recherche inversée
file=open("/var/lib/bind/db."+net_part, 'w')
str=["""$ORIGIN {4}.in-addr.arpa.
$TTL    604800
@       IN      SOA     {0}.{1}. root.{0}.{1}. (
                              1         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@     IN  NS  {0}.{1}.
{2}     IN  PTR  {0}.{1}.
{2}     IN  PTR  dns.{1}.
{3}     IN  PTR  gw.{1}.
""".format(srv_name, dom_name, srv_addr, gw_addr, net_arpa)]
file.writelines(str)
file.close()

os.system("""chown -R bind:bind /var/lib/bind
service bind9 restart""")

################
# Finalisation #
################

print_ligne()
txt_justif('Création index.php pour test PHP')
file=open("/var/www/html/index.php", 'w')
file.writelines("""<?php
        phpinfo();
?>
""")
file.close()

print_ligne()
print("Fini ! Je redémarre avec l'@IP {0}.{1}".format(net_part, srv_addr))
print_ligne()

os.system('reboot')

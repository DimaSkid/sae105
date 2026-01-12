Voici une proposition de README.md sobre et structurée pour votre dépôt GitHub, conçue pour être utilisée par les équipes techniques en Inde.

Présentation
Cet outil automatise l'analyse des fichiers de capture réseau issus de tcpdump. Il transforme des logs textuels bruts en rapports structurés (HTML et CSV) pour faciliter le diagnostic réseau et la surveillance du trafic.

Fonctionnalités
Extraction par Regex : Identification automatique de l'horodatage, des adresses IP (source et destination), des services, des drapeaux TCP et de la taille des paquets.

-Tableau de bord HTML : Visualisation des statistiques clés (sources les plus actives, ports sollicités, répartition des flags).
-Export CSV : Archivage des données extraites dans un format compatible avec les outils d'analyse de données et tableurs.

Interface Graphique : Fenêtre de sélection de fichier pour une utilisation simplifiée sans ligne de commande.
Requirements (prérequis) : 
  -Python 3.8 ou version supérieure.
  -Bibliothèques standards utilisées : os, re, csv, tkinter, webbrowser, collections.

Installation
Cloner le dépôt : git clone https://github.com/DimaSkid/sae105.git

Accéder au répertoire : cd sae15

Instructions d'utilisation
Exécuter le script : python test.py

Dans l'interface, cliquer sur le bouton Choisir le fichier dump.

Sélectionner le fichier de log au format .txt.

Une fois l'analyse terminée :

Le Tableau de bord réseau s'ouvre automatiquement dans votre navigateur par défaut.

Un fichier nommé donnees_extraites.csv est généré dans le dossier contenant le log d'origine.

Interprétation des résultats
Analyse de sécurité : Un volume élevé de flags [S] (SYN) provenant d'une source unique peut indiquer une tentative de scan ou une attaque par déni de service.

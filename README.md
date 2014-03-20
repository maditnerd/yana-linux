yana-linux
==========

Yana client for Linux

##Installation

### Copie de yana-linux (dans le répertoire courant)

```` 
sudo apt-get install git-core
git clone http://github.com/maditnerd/yana-linux
````

### Dépendances
```` 
cd yana-linux
sudo ./install.sh 
````

### Réglages du micro / volume

```` alsamixer ````

#### Volume Baffes
Augmenter le volume (flèche vers le haut)

#### Volume Micro
* Tapez F6
* Choissisez votre micro/webcam
* Monter le volume

## Configuration

### Connexion à yana-server

Toute la configuration se fait dans le fichier *yana.cfg*
Adresse IP de votre Raspberry Pi (127.0.0.1 si vous utilise yana-linux sur le même raspberry pi que yana-server)
* ip=127.0.0.1

URL de yana server, par exemple si vous avez votre yana-server sur http://192.168.0.10/yana-server 
* url=yana-server

Le token d'identification fourni sur yana-server
* token=1234

http ou https ? (1 pour https, 0 pour http)
* ssl=1

### Paramètres de la reconnaissance vocale
Yana for linux peut se réveler être moins précis que YANA for windows (surtout qu'il n'utilise pas le même systeme pour gérer la détection, cette variable vous permet de réduire le paramètre *confidence* de toutes les commandes
* tolerance=0.4

Durée où Yana for Linux va enregistrer des extraits audio en secondes
* duration=3

Cette valeur correspond à la différence de volume avant que la reconnaissance vocale s'enclenchent.
Même si cette méthode n'est pas la plus pertinente (le moindre brut soudain va la déclencher) c'est le seul moyen que j'ai trouvé pour limiter l'envoi de requête à google.
* maxlevel=3


### Avancé
Change la langue de la reconnaissance vocale / synthèse vocale
* lang=fr

Un son est émis lorsque la reconnaissance est prête (au premier lancement) et puis à chaque fois qu'une élévation de volume a été detecté. Ce son n'est là que pour les tests, et il est conseillé de le déactiver pour votre santé mentale.
*beep=1

Active/Déactive la synthèse vocale
*voice=1



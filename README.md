Ce client ne marche plus :-( Désolé , je laisse ça là si quelqu'un veut réutiliser une partie du code. (yana-linux)
==========



Alternative:
* https://www.openjarvis.com/
* https://github.com/kitt-ai/snowboy


Bon je vais pas vous laissez sur la faim, j'ai regardé un peu ce qu'on pouvait faire avec snowboy, si ça dit quelqu'un de creuser la dessus. Par contre c'est pas sensé être utiliser comme ça mais je pense que ça peut être intéressant à tester plus en profondeur.

# Contrôler un websocket avec snowboy (reconnaissance vocale hors ligne)
Snowboy est utilisé comme détecteur de mot clé, mais il peut aussi marcher avec des phrases complètes.    
Vous devez enregistrer les phrases sur le siteweb de snowboy (vous pouvez utiliser votre login github) et les télécharger.    
Une fois que vous avez le modèle, vous pouvez utiliser snowboy sans connexion à internet.

## Installer snowboy (Aller voir la doc officiel en cas de problème)

```
#!/bin/bash
mkdir /opt/snowboy
cd /opt/snowboy

wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.1.1.tar.bz2
tar -xvf rpi-arm-raspbian-8.0-1.2.0.tar.bz2
apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev
pip install pyaudio

# Generate alsa configuration for root

cat > ~/.asoundrc << EOF
pcm.!default {
  type asym
   playback.pcm {
     type plug
     slave.pcm "hw:0,0"
   }
   capture.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
}
EOF

rec test.wav
```

## Code Python (Le premier modèle allume une led, le second en éteint une)
```
import snowboydecoder
import sys
import signal
import websocket
# Demo code for listening two hotwords at the same time

interrupted = False

ws = websocket.WebSocket()
ws.connect("ws://localhost:42000");

def signal_handler(signal, frame):
    global interrupted
    interrupted = True
def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

def turn_on():
    print("ON")
    ws.send("ON")

def turn_off():
    print("OFF")
    ws.send("OFF")

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: turn_on(),
             lambda: turn_off()]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
```

|
|
|
|
|

Yana client for Linux [Obsolète]



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
* beep=1

Active/Déactive la synthèse vocale
* voice=1



Yana-Linux
----------
Vous pouvez trouver des bouts de code ici, si vous voulez créer un client en python pour yana.    
Il y a un exemple de reco hors ligne et un code pour récupérer les commandes sur yana.    

* yana-linux.py, récupère les commandes de yana et les affiche.  
* test_vocal.py, est un exemple de reconnaissance vocale hors ligne, il écrit ON quand on dit allumer et OFF quand on dit éteindre.   
J'ai mis les modèles vocales que j'ai enregistré dans pmdl (allumer.pmdl, eteindre.pmdl) mais je vous conseille de générer les votre sur    
le site de snowboy c'est très facile et ça contribue à améliorer son fonctionnement.

Ceci ne marchera qu'avec des phrases préenregistrés, et je garantis pas la fiabilité mais si ça vous dit de tester 
D'origine c'est utilisé pour reconnaitre **uniquement** un mot clé avant de switcher sur de la reconnaissance avec Google/Amazon, mais   
ça marche pas si mal de lui-même.   

Vous pouvez voir mon code qui marche plus ici : https://github.com/maditnerd/yana-linux/tree/deprec

# Prérequis

* Un micro (ou une webcam)

# Installation
Snowboy ne nécessite pas d'être installer, il nous faut juste des bibliothèque python pour gérer l'enregistrement vocal.    
J'ai inclus snowboy dans le repo pour ceux qui voudraient tester ça, mais je vous conseille de le télécharger par vous même en suivant 
la documentation
http://docs.kitt.ai/snowboy/

* Cloner ce repo sur votre Raspberry Pi
```
git clone https://github.com/maditnerd/yana-linux 
```

* Lancer install.sh ou tapez ceci
```
sudo apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev python-pip
sudo pip install pyaudio

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
```

* Test micro
Un petit test du micro, les barres devraient bouger, il va aussi créer un fichier test.wav.
```
rec test.wav
```

# Enregistrer allumer/éteindre
* Aller sur https://snowboy.kitt.ai/dashboard
* Créer un compte (si vous avez un compte github c'est rapide)

Voici les modèles que j'ai crée pour allumer et éteindre, vous pouvez les télécharger ici uniquement après avoir   
enregistrer votre voix (c'est de toute façon conseiller si vous voulez que ça marche avec votre voix)   

**utiliser le même micro que sur le raspberry pi si possible**
* allumer.pmdl
https://snowboy.kitt.ai/hotword/1638
* eteindre.pmdl
https://snowboy.kitt.ai/hotword/3477

# Tester
Copier vos modèles dans le dossier pmdl et tapez:
```
./test.sh
```
Ou
```
python test_vocal.py pmdl/allumer.pmdl pmdl/eteindre.pmdl
```

# Aller plus loin
A partir de là, aller jeter un oeil sur test_vocal.py, le code est très simple.     
Dans detector, on injecte les modèles préenregistrés et on leur assigne une fonction.   
La fonction est exécuté à chaque fois qu'un modèle est reconnu.

J'ai fait des tests avec des phrases plutôt que des mots, et ça marche, après il faudrait faire plus de tests pour la fiabilité.   
Malheuresement j'ai pas trop le temps de m'en occuper mais je me suis dit que ça pourrait être utile à d'autres gens.   
Hésitez pas à écrire un message dans issues (ou sur celui de yana-server), si vous testez ça, j'essayerais d'y répondre.
* https://github.com/maditnerd/yana-linux/issues
* https://github.com/ldleman/yana-server/issues/285


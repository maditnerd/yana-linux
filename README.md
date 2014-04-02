yana-linux
==========

Yana client for Linux/Raspberry Pi

##Installation

### Copy yana-linux (inside current directory)

```` 
sudo apt-get install git-core
git clone http://github.com/maditnerd/yana-linux -b en
````

### Dépendencies
```` 
cd yana-linux
sudo ./install.sh 
````

### Set up microphone and speakers

```` alsamixer ````

#### Speaker Volume
Augmenter le volume (flèche vers le haut)

#### Microphone Volume
* Type F6
* Choose your microphone/webcam
* Turn up the volume

## Configuration

### Connect it to Yana Server

All the configuration is made in *yana.cfg*

Raspberry Pi IP Address (127.0.0.1 if you use yana-linux on the same Raspberry Pi than yana-server)
* ip=127.0.0.1

Yana-server's URL, for example if you have yana-server on http://192.168.0.10/yana 
* url=yana

Identification token founded on yana-server
* token=1234

http ou https ? (1 for https, 0 for http)
* ssl=1

### Settings the vocal recognition
Yana for linux can be less precise then Yana for Windows (especially has it doesn't use the same system to handle detection, this variable reduce the confidence parameters of all commands
* tolerance=0.4

Duration of audio recording in seconds
* duration=3

Audio level difference before vocal recognition is activated
(This method is not the best to trigger detection but limit the number of request to google)
* maxlevel=3


### Avancé
Modify the vocal recognition/ vocal synthesis language
* lang=en

Enable a beep sound when the recognition is ready (at launch) and then every time recognition is ready
It should be only used to debug.
* beep=1

Enable/Disable vocal recognition
* voice=1



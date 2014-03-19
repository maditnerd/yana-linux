#!/bin/bash
#TTS convert speech to text with Google API
#Original from StevenHickson
#Modified by Sarrailh Remi

string=$@
lang="fr"
if [ "$1" == "-l" ] ; then
    lang="$2"
    string=`echo "$string" | sed -r 's/^.{6}//'`
fi

#empty the original file
echo "" > "/dev/shm/speak.mp3"

len=${#string}
while [ $len -ge 100 ] ;
do
    #lets split this up so that its a maximum of 99 characters
    tmp=${string:0:100}
    string=${string:100}
    
    #now we need to make sure there aren't split words, let's find the last space and the string after it
    lastspace=${tmp##*"%20"}
    tmplen=${#lastspace}

    #here we are shortening the tmp string
    tmplen=`expr 100 - $tmplen` 
    tmp=${tmp:0:tmplen}
    
    #now we concatenate and the string is reconstructed
    string="$lastspace$string"
    len=${#string}

    #get the first 100 characters
    wget -q -U Mozilla -O "/dev/shm/tmp.mp3" "http://translate.google.com/translate_tts?ie=utf8&tl=${lang}&q=$tmp"
    cat "/dev/shm/tmp.mp3" >> "/dev/shm/speak.mp3"
done
#this will get the last remnants
wget -q -U Mozilla -O "/dev/shm/tmp.mp3" "http://translate.google.com/translate_tts?ie=utf8&tl=${lang}&q=$string"
cat "/dev/shm/tmp.mp3" >> "/dev/shm/speak.mp3"
#now we finally say the whole thing
cat "/dev/shm/speak.mp3" | mpg123 - 1>>/dev/shm/voice.log 2>>/dev/shm/voice.log

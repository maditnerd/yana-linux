#!/bin/sh
#DaveConroy.com
#10/29/13
#Text 2 Speech with Google API
#stt.sh
#Modified by Sarrailh Remi 03/18/2014

sample_rate=16000
lang=$1
duration="3"
hardware="plughw:1,0"

flac /dev/shm/noise.wav -f --best --sample-rate 16000 -o /dev/shm/out.flac 1>/dev/shm/voice.log 2>/dev/shm/voice.log; curl -X POST --data-binary @/dev/shm/out.flac --user-agent 'Mozilla/5.0' --header 'Content-Type: audio/x-flac; rate=16000;' "https://www.google.com/speech-api/v2/recognize?output=json&lang=$lang&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&client=Mozilla/5.0" | sed -e 's/[{}]/''/g' | awk -F":" '{print $4}' | awk -F"," '{print $1}' | tr -d '\n'
rm /dev/shm/out.flac
echo " "

#DaveConroy.com
#10/29/13
#Text 2 Speech with Google API
#stt.sh
#Modified by Sarrailh Remi 03/18/2014

#hardware="plughw:1,0"
#duration="3"
#lang="fr"
sample_rate=16000
lang=$1
#duration=$2
flac /dev/shm/noise.wav -f -0 --sample-rate $sample_rate -o /dev/shm/out.flac 1>/dev/shm/voice.log 2>/dev/shm/voice.log; wget -O - -o /dev/null --post-file /dev/shm/out.flac --header="Content-Type: audio/x-flac; rate=16000" http://www.google.com/speech-api/v1/recognize?lang="$lang" | sed -e 's/[{}]/''/g'| awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]; exit }' | awk -F: 'NR==3 { print $3; exit }'
echo " "

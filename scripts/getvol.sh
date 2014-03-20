#!/bin/sh
#Get volume level of a audio file
#Inspired by StevenHickson voice command code
#Made by Sarrailh Remi

hardware="plughw:1,0"
sample_rate=16000
duration=$1

arecord -q -D $hardware -f cd -t wav -d $duration -r $sample_rate /dev/shm/noise.wav
vol=$(sox /dev/shm/noise.wav -n stats -s 16 2>&1  | grep "Max level"|awk {'print $3'})
echo $vol

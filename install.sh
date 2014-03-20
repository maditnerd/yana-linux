echo "---------------------"
echo "Dependencies"
echo "---------------------"
sudo apt-get install python-levenshtein sox flac mpg123 git-core

echo "---------------------"
echo "Settings Mic/Speakers"
echo "---------------------"
alsamixer
scripts/tts.sh -l en "Installation finished"

echo "---------------------"
echo "Test Mic"
echo "---------------------"
echo "Press Enter when you are ready to test the mic"
read

arecord -D plughw:1,0 -d 3 -r 16000 -t wav /tmp/test.wav
aplay /tmp/test.wav


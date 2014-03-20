echo "---------------------"
echo "Dependencies"
echo "---------------------"
sudo apt-get install python-levenshtein sox flac mpg123 git-core

echo "---------------------"
echo "Settings Mic/Speakers"
echo "---------------------"
alsamixer
scripts/tts.sh -l en "Installation finished"

apt-get install python-pyaudio python3-pyaudio sox libatlas-base-dev python-pip
pip install pyaudio

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
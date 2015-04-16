#!/usr/bin/python
"""
This script manages vocal recognition for YANA
This heavily uses Google API so you need a internet connection

You should be advice that you are sending short portion of audio recording to Google
This programs is also not support by Google.

By Sarrailh Remi Gplv3
https://github.com/maditnerd/yanapi
"""
import ConfigParser
import urllib2
import json
import os
import sys
import Levenshtein
import unicodedata

global ding
global voice
global path
global lang

""" 
Constants 
"""
command="GET_SPEECH_COMMAND"
config_file = "yana.cfg"

"""
Functions
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#Verify if a file exists
def file_exists( filename ):
	if (os.path.isfile(filename)):
		print filename + " founded"
	else:
		fatalerror(filename + " not founded")
	return 

#Verify dependencies
def verify_files():
	file_exists(path + "yana.cfg")
	file_exists(path + "scripts/sst.sh")
	file_exists(path + "scripts/getvol.sh")
	file_exists(path + "scripts/tts.sh")
	file_exists("/usr/bin/sox")
	file_exists("/usr/bin/flac")
	file_exists("/usr/bin/play")
	file_exists("/usr/bin/mpg123")
	file_exists("/usr/bin/arecord")

#Convert a string to a boolean
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

#Convert accentuated characters to unicode non accentuated string
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def banner(text):
	print bcolors.OKBLUE + "\n----------------------" + bcolors.ENDC
	print bcolors.OKBLUE + text + bcolors.ENDC
	print bcolors.OKBLUE + "---------------------" + bcolors.ENDC

def banner_green(text):
	print bcolors.OKGREEN + "\n----------------------" + bcolors.ENDC
	print bcolors.OKGREEN + text + bcolors.ENDC
	print bcolors.OKGREEN + "---------------------" + bcolors.ENDC

def banner_yellow(text):
	print bcolors.WARNING + "\n----------------------" + bcolors.ENDC
	print bcolors.WARNING + text + bcolors.ENDC
	print bcolors.WARNING + "---------------------" + bcolors.ENDC

def fatalerror(text):
	print bcolors.FAIL + "ERROR: " + text + bcolors.ENDC
	exit(1)
#External Commands (TODO: Theses functions should be python native)

#Play a MP3
def playsound(name):
	if (ding):
		os.system("play " + path + "sounds/" + name + " > /dev/null 2>&1 &")

#Record sound for duration and output volume
def getvol():
	volume = os.popen(path + "scripts/getvol.sh "+ duration).readlines()
	try:
		volume = float(volume[0])
	except ValueError:
		os.system("arecord -l")
		fatalerror("No Microphone detected / Bad Microphone Configuration")
	return volume

#Convert speech 2 text with Google API
def speech2text():
	output = os.popen(path + "scripts/sst.sh " + lang).readlines()
	output = unicode(output[0],'utf8')
	return output

#Convert text2speech with Google API
def text2speech( text ):
	if (voice):
		os.system(path + "scripts/tts.sh -l " + lang + " " + text.encode("utf-8"))


"""
Verify dependencies
"""
banner("Verify Files")
#Get Path of yanavoice
path = os.path.dirname(sys.argv[0])+"/"
#Verify that all scripts/configuration are there
verify_files()


"""
Read Configuration File
"""
#Read the configuration files
settings = ConfigParser.ConfigParser()
settings.read(path + config_file)

banner("Reading Configuration File")

try:
	ip = settings.get("yana","ip") #IP Address of the Raspberry Pi
	ssl = str2bool(settings.get("yana","ssl")) #HTTP/HTTPS ?
	url = settings.get("yana","url") #URL of Yana
	token = settings.get("yana","token") #YANA Token
	tolerance = float(settings.get("recognition","tolerance")) #Tolerance (Lower confidence of YANA)
	duration = settings.get("recognition","duration") #Duration of recording (by default:3)
	maxlevel = settings.get("recognition","maxlevel") #Sound level difference before recognition
	ding = str2bool(settings.get("advanced","beep")) #Beep when a volume elevation is detected
	voice = str2bool(settings.get("advanced","voice")) #Voice response when a command is done
	lang = settings.get("advanced","lang") #Language used
	print "Configuration readed successfully"
except ConfigParser.NoOptionError, e:
	fatalerror("yana.cfg is corrupted")

""" Get Commands from YANA """
if (ssl):
	url_begin = "https://"
else:
	url_begin = "http://"

banner("Connecting to " + url_begin + ip + "/" +url)

#Building URL to query commands
command_list_commands = url_begin+ip+"/"+url+"/action.php?action="+command+"&token="+token
try:
	json_commands = urllib2.urlopen(command_list_commands).read() #Put all the command in an list
#Handle invalid IP
except IOError, e:
	fatalerror("Invalid IP in yana.cfg")

#If response is not json data we assume the URL is incorrect
try:
	commands = json.loads(json_commands)
except ValueError,e:
	fatalerror("Invalid URL in yana.cfg")

#If we have json data with Error, display error
if("error" in commands):
		fatalerror(commands["error"])
else:
	print "Connection established"

""" Convert JSON commands to Lists """

banner("Converting Commands Lists from Yana")

i=0
for command in commands["commands"]:
	print command["command"]
	#Commands are converted in unicode (so we can compare them)
	commands["commands"][i]["command"] = strip_accents(command["command"])
	if(ssl):
		commands["commands"][i]["url"] = command["url"].replace("http","https")
	#Confidence level are converted in float (so we can compare them)
	commands["commands"][i]["confidence"] = float(command["confidence"])
	i = i + 1
	
#At first launch we record silence to have a basic level
banner("Recording Silence")
output_volume_low = getvol()
silence_volume = output_volume_low
print "Volume:" + str(output_volume_low)

playsound("ding.wav")
#Handle general error
#try:
while 1:
	confidence = 0

	banner("Waiting for Audio Elevation")

	#Get Volume of audio
	output_volume_high = getvol()
	#Compare Volume Audio from last recording
	output_volume_variation = output_volume_high - output_volume_low
	print "Volume Differential:" + str(output_volume_variation)
	#Reset last audio volume
	output_volume_low = output_volume_high
	#If volume is higher than usual we assume someone spoke
	if (output_volume_variation >  int(maxlevel)):
			
		banner_green("Searching for commands")
		playsound("ding.wav")
			
		new_result = False
		best_result_confidence = 0
		output = speech2text()
		print "I heard :" + output
			
		#Compare speak with the lists of commands
		for command in commands["commands"]:
				
			#Use Levenshtein algorithm to see which commands look like what have been said
			confidence = Levenshtein.ratio(output,command["command"])
			
			#If a command look like what have been said (confidence - tolerance) then elect it has the right command
			if (confidence > float(command["confidence"] - tolerance)):
				#If a command look like a better result than the first elected replace it
				if(new_result):
					if (confidence > best_result_confidence):
						best_result = command
						best_result_confidence = confidence
				#First time a command look like a good command we save it
				else:
					best_result = command
					best_result_confidence = confidence
					new_result = True;
		#If a command is found
		if (new_result):
			#Display the command
			print "I understood : " + best_result["command"]
			#Prepare the command with token
			action = best_result["url"]+"&token="+token
			#print action
			#Send command to the YANA
			json_response = urllib2.urlopen(action).read()
			try:
				response = json.loads(json_response)
				if ("talk" in response["responses"][0]["type"]):
					speak = response["responses"][0]["sentence"].encode("utf8","ignore")
					banner_yellow("Response")
					print speak
					speak = urllib2.quote(speak)
					text2speech(speak)
				elif ("sound" in response["responses"][0]["type"]):
					print response["responses"][0]["file"]
					playsound(response["responses"][0]["file"])
				elif ("command" in response["responses"][0]["type"]):
					os.system(response["responses"][0]["program"] + " &")
				else:
					banner_yellow("Unsupported Response")
					print response
			except ValueError, e:
				banner_yellow("No Json Answer")
		else:
			banner_yellow("No Command Detected")

		#Resetting volume to original silence volume
		output_volume_low = silence_volume
#except KeyError, e:
#	fatalerror("Unknown Error")

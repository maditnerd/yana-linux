#!/usr/bin/python
"""
Recup des commandes dans yana
"""
import urllib2
import json
import sys

if len(sys.argv) != 3:
    print("Utilisation: python yana-linux.py url token")
    print("Exemple: python yana-linux http://127.0.0.1/yana-server/ bb4ddb24a32172eed1")
    sys.exit(-1)

url = sys.argv[1]
token = sys.argv[2]

""" 
Constants 
"""
command="GET_SPEECH_COMMAND"

# Building URL to query commands
command_list_commands = url + "/action.php?action="+command+"&token="+token
json_commands = urllib2.urlopen(command_list_commands).read() #Put all the command in an list

#If response is not json data we assume the URL is incorrect
commands = json.loads(json_commands)

""" Convert JSON commands to Lists """
for command in commands["commands"]:
	print command

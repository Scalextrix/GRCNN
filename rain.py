#!/usr/bin/env python

"""Gather list of Whitelisted projects from Gridcoin NN, call each project for team member CPIDs,
allow user to send a multi transaction to rain GRC on team members"""

import getpass
import subprocess
from urllib2 import urlopen
import sqlite3
import gc
import xml.etree.ElementTree as ET

gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")

rosetta_url = ("https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&account_key=Y&xml=1")

root = ET.parse(urllib.urlopen(rosetta_url)).getroot()

items = root.findall('users/user')
for user in root: 
     user.find('cpid').text 

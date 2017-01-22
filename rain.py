#!/usr/bin/env python

"""Gather list of Whitelisted projects from Gridcoin NN, call each project for team member CPIDs,
allow user to send a multi transaction to rain GRC on team members"""

__author__ = "Steven Campbell AKA Scalextrix"
__copyright__ = "Copyright 2017, Steven Campbell"
__license__ = "The Unlicense"
__version__ = "0.1"

import csv
import gc
import getpass
import itertools
import os.path
import sqlite3
import subprocess
import sys
from urllib2 import urlopen
import xml.etree.ElementTree as ET

user_account = getpass.getuser()	
filename = "C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\DailyNeuralMagnitudeReport.csv" % user_account

if os.path.isfile("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account):
	print "File path to DailyNeuralMagnitudeReport.csv found"	
else:
	conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS USERPREFS (filename TEXT)''') 
	c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?);", filename)
	conn.commit()		
	conn.close()

rosetta_url = ("https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&account_key=Y&xml=1")

rain_team = raw_input("Which BOINC project to RAIN on: ").lower()
if rain_team == "rosetta" or rain_team == "rosetta@home":
	project_url = rosetta_url
else:
	sys.exit("Sorry: BOINC Team not recognised")

grc_amount = raw_input("How much GRC to rain on BOINC project: ")
grc_amount = float(grc_amount)
account_label = raw_input("Choose Wallet Account Label from which the GRC should be taken: ")
message = raw_input("Enter if you wish to send a message to recipients: ")
message = str('"'+message+'"')
gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")
        
root = ET.parse(urlopen(project_url)).getroot()
team_cpids = [el.text for el in root.findall('.//user/cpid')]
team_cpids = zip(*[iter(team_cpids)]*1)
print "BOINC project team XML Parsed"

conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS GRIDCOINTEAM (cpids TEXT)''') 
c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?);", team_cpids)
conn.commit()		
conn.close()
print "TEAM DB created"

conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS NNDATA (cpid TEXT, LocalMagnitude TEXT, NeuralMagnitude TEXT, TotalRAC TEXT, Synced Til TEXT, Address TEXT, CPID_Valid TEXT, Witnesses TEXT)''')
filename.encode('utf-8')
with open(filename, 'rb') as NN:
    reader = csv.DictReader(NN)
    field = [(i['CPID'], i['LocalMagnitude'], i['NeuralMagnitude'], i['TotalRAC'], i['Synced Til'], i['Address'], i['CPID_Valid'], i['Witnesses']) for i in reader]
    c.executemany("INSERT INTO NNDATA VALUES (?,?,?,?,?,?,?,?);", field)
conn.commit()		
conn.close()
print "CSV DB created"
            
conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
conn.text_factory = float
nn_mag = c.execute('select NeuralMagnitude from NNDATA where cpid in (select cpids from GRIDCOINTEAM)').fetchall() 
conn.text_factory = str
address = c.execute('select Address from NNDATA where cpid in (select cpids from GRIDCOINTEAM)').fetchall()
conn.close()
print "DB values exported"

address = list(itertools.chain(*address))
nn_mag = list(itertools.chain(*nn_mag))
address = filter(lambda x: x is not None,address)
nn_mag = filter(lambda x: x is not None,nn_mag)
call_amount = [x * (grc_amount / (sum(nn_mag))) for x in nn_mag]
call_amount = [str(i) for i in call_amount]
counter1 = len(nn_mag)
quotes = '"' * counter1
colon = ":" * counter1
comma = "," * counter1
call_insert = [val for pair in zip(quotes, address, quotes, colon, call_amount, comma) for val in pair]
call_insert = ''.join(call_insert)
call_insert = str("'{"+call_insert+"}'")

print("Gridcoin TXID:")   
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=False)
subprocess.call(['gridcoinresearchd', 'sendmany', account_label, call_insert, message], shell=False)
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=False)

conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''')
c.execute('''DROP TABLE IF EXISTS NNDATA''')
conn.commit()		
conn.close()
            
gc.collect()

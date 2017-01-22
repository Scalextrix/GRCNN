#!/usr/bin/env python

"""Gather list of Whitelisted projects from Gridcoin NN, call each project for team member CPIDs,
allow user to send a multi transaction to rain GRC on team members"""

__author__ = "Steven Campbell AKA Scalextrix"
__copyright__ = "Copyright 2017, Steven Campbell"
__license__ = "The Unlicense"
__version__ = "0.1"

import getpass
from urllib2 import urlopen
import gc
import xml.etree.ElementTree as ET
import subprocess
import sys
import csv
import os.path

if os.path.isfile("Rain.db"):
	print "File path to DailyNeuralMagnitudeReport.csv found"	
else:
	user_account = raw_input("What is your PC User Account (case sensitive): ")
	filename = "C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\DailyNeuralMagnitudeReport.csv" % user_account
	conn = sqlite3.connect("Rain.db")
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
message = raw_input("Enter if you wish to send a message to recipients: ")
message = str('"'+message+'"')
gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")
        
root = ET.parse(urlopen(project_url)).getroot()
team_cpids = [el.text for el in root.findall('.//user/cpid')]
team_cpids = zip(*[iter(team_cpids)]*1)
print "BOINC project team XML Parsed"

conn = sqlite3.connect("Rain.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS GRIDCOINTEAM (cpids TEXT)''') 
c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?);", team_cpids)
conn.commit()		
conn.close()
print "TEAM DB created"

conn = sqlite3.connect("Rain.db")
c = conn.cursor()
filename = c.execute('select filename from USERPREFS').fetchall()
filename = [0][0]
c.execute('''CREATE TABLE IF NOT EXISTS NNDATA (cpid TEXT, LocalMagnitude TEXT, NeuralMagnitude TEXT, TotalRAC TEXT, Synced Til TEXT, Address TEXT, CPID_Valid TEXT, Witnesses TEXT)''')
filename.encode('utf-8')
with open(filename, 'rb') as NN:
    reader = csv.DictReader(NN)
    field = [(i['CPID'], i['LocalMagnitude'], i['NeuralMagnitude'], i['TotalRAC'], i['Synced Til'], i['Address'], i['CPID_Valid'], i['Witnesses']) for i in reader]
    c.executemany("INSERT INTO NNDATA VALUES (?,?,?,?,?,?,?,?);", field)
conn.commit()		
conn.close()
print "CSV DB created"
            
conn = sqlite3.connect("Rain.db")
c = conn.cursor()
conn.text_factory = str
nn_mag = c.execute('select NeuralMagnitude from NNDATA where cpid in (select cpids from GRIDCOINTEAM)').fetchall() 
conn.text_factory = float
address = c.execute('select distinct Address from NNDATA where cpid in (select cpids from GRIDCOINTEAM)').fetchall()
conn.close()
print "DB values exported"

address = list(itertools.chain(*address))
nn_mag = list(itertools.chain(*nn_mag))
address = filter(lambda x: x is not None,address)
nn_mag = filter(lambda x: x is not None,nn_mag)
call_amount = [x * (grc_amount / (sum(nn_mag))) for x in nn_mag]
call_amount = [str(i) for i in call_amount]
counter1 = len(nn_mag)
colon = ":" * counter1
comma = "," * counter1
call_insert = [val for pair in zip(address, colon, call_amount, comma) for val in pair]
call_insert = ''.join(call_insert)
call_insert = str("'{"+call_insert+"}'")

print("Gridcoin TXID:")   
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=False)
subprocess.call(['gridcoinresearchd', 'sendmany', '', call_insert, '', '', message], shell=False)
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=False)

conn = sqlite3.connect("Rain.db")
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''')
c.execute('''DROP TABLE IF EXISTS NNDATA''')
conn.commit()		
conn.close()
            
gc.collect()

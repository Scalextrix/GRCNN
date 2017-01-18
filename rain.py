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

gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")
grc_amount = raw_input("How much GRC to rain on BOINC project: ")

rosetta_url = ("https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&account_key=Y&xml=1")


rain_team = raw_input("Which BOINC project to RAIN on: ").lower()
if rain_team == "rosetta" or rain_team == "rosetta@home":
    project_url = rosetta_url
else:
    sys.exit("Sorry: BOINC Team not recognised")
        
root = ET.parse(urlopen(project_url)).getroot()
team_cpids = [el.text for el in root.findall('.//user/cpid')]
team_cpids = zip(*[iter(team_cpids)]*1)
print "XML Parsed"

conn = sqlite3.connect("Rain.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS GRIDCOINTEAM (cpids TEXT)''') 
c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?);", team_cpids)
conn.commit()		
conn.close()
print "TEAM DB created"

user_account = raw_input("What is your PC User Account: ")
filename = "C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\DailyNeuralMagnitudeReport.csv" % user_account

conn = sqlite3.connect("Rain.db")
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
            
conn = sqlite3.connect("Rain.db")
c = conn.cursor()
nn_mag = c.execute('select distinct NeuralMagnitude from NNDATA where cpid from NNDATA in select distinct cpids from GRIDCOINTEAM').fetchall() 
address = c.execute('select distinct Address from NNDATA where cpid in NNDATA in select distinct cpids from GRIDCOINTEAM').fetchall()
conn.close()
print "DB values exported"

print("Gridcoin TXID:")   
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=False)
subprocess.call(['gridcoinresearchd', 'sendmany', address, grc_amount, '', '', 'Its raining GRC'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=False)

conn = sqlite3.connect("Rain.db")
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''')
c.execute('''DROP TABLE IF EXISTS NNDATA''')
conn.commit()		
conn.close()
            
gc.collect()

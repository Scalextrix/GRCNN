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

asteroids_url = ("http://asteroidsathome.net/boinc/team_email_list.php?teamid=2218&xml=1")
atlas_url = ("http://atlasathome.cern.ch/team_email_list.php?teamid=1869&account_key=Y&xml=1")
collatz_url = ("http://boinc.thesonntags.com/collatz/team_email_list.php?teamid=3029&xml=1")
csgrid_url = ("http://csgrid.org/csg/team_email_list.php?teamid=154&xml=1")
ddm_url = ("http://www.distributeddatamining.org/DistributedDataMining/team_email_list.php?teamid=2176&xml=1")
gpugrid_url = ("https://www.gpugrid.net/team_email_list.php?teamid=3493&xml=1")
gridcoin_finance_url = ("finance.gridcoin.us/finance/team_email_list.php?teamid=5&xml=1")
einstein_url = ("https://einsteinathome.org/team_email_list.php?teamid=13630&account_key=Y&xml=1")
lhc_url = ("http://lhcathomeclassic.cern.ch/sixtrack/team_email_list.php?teamid=8128&xml=1")
milkyway_url = ("http://milkyway.cs.rpi.edu/milkyway/team_email_list.php?teamid=6566&xml=1")
poem_url = ("http://boinc.fzk.de/poem/team_email_list.php?teamid=3147&xml=1")
primegrid_url = ("https://www.primegrid.com/team_email_list.php?teamid=4469&xml=1")
rosetta_url = ("https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&account_key=Y&xml=1")
seti_url = ("https://setiathome.berkeley.edu/team_email_list.php?teamid=145340&xml=1")
wcg_url = ("https://www.worldcommunitygrid.org/boinc/team_email_list.php?teamid=30513&xml=1")
yafu_url = ("http://yafu.myfirewall.org/yafu/team_email_list.php?teamid=260&account_key=Y&xml=1")


rain_team = raw_input("Which BOINC project to RAIN on: ").lower()
if rain_team == "asteroids" or rain_team == "asteroids@home":
	project_url = asteroids_url
elif rain_team == "atlas" or rain_team == "atlas@home":
	project_url = atlas_url
elif rain_team == "collatz" or rain_team == "collatz conjecture":
	project_url = collatz_url
elif rain_team == "csg" or rain_team == "csgrid" or rain_team == "citizen science grid":
	project_url = csgrid_url
elif rain_team == "ddm" or rain_team == "distributed data mining":
	project_url = ddm_url
elif rain_team == "gpugrid" or rain_team == "gpugrid.net":
	project_url = gpugrid_url
elif rain_team == "gridcoin finance":
	project_url = gridcoin_finance_url
elif rain_team == "einstein" or rain_team == "einstein@home":
	project_url = einstein_url
elif rain_team == "lhc" or rain_team == "lhc@home":
	project_url = lhc_url
elif rain_team == "milkyway" or rain_team == "milky way" or rain_team == "milkyway@home":
	project_url = milkyway_url
elif rain_team == "poem" or rain_team == "poem@home":
	project_url = poem_url
elif rain_team == "primegrid" or rain_team == "primegrid@home":
	project_url = primegrid_url
elif rain_team == "rosetta" or rain_team == "rosetta@home":
	project_url = rosetta_url
elif rain_team == "seti" or rain_team == "seti@home":
	project_url = seti_url
elif rain_team == "wcg" or rain_team == "world community grid":
	project_url = wcg_url
elif rain_team == "yafu" or rain_team == "yafu@home":
	project_url = yafu_url
else:
	sys.exit("Sorry: BOINC Team not recognised")

grc_amount = float(raw_input("How much GRC to rain on BOINC project: "))
account_label = raw_input("Choose Wallet Account Label from which the GRC should be taken: ")
message = str('"'+(raw_input("Enter if you wish to send a message to recipients: "))+'"')
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
nn_mag = c.execute('select NeuralMagnitude from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM)').fetchall() 
conn.text_factory = str
address = c.execute('select Address from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM)').fetchall()
conn.close()
print "DB values exported"

conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''')
c.execute('''DROP TABLE IF EXISTS NNDATA''')
conn.commit()		
conn.close()

address = list(itertools.chain(*address))
nn_mag = list(itertools.chain(*nn_mag))
call_amount = [x * (grc_amount / (sum(nn_mag))) for x in nn_mag]
call_amount = [str("{:.8f}".format(i)) for i in call_amount]
quotes = '"' * len(nn_mag)
colon = ":" * len(nn_mag)
comma = "," * len(nn_mag)
call_insert = [val for pair in zip(quotes, address, quotes, colon, call_amount, comma) for val in pair]
call_insert = str('{'+(''.join(call_insert))+'}')
call_insert = call_insert[:-2] + call_insert[-1:]

print("Gridcoin TXID:")   
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=True)
subprocess.call(['gridcoinresearchd', 'sendmany', account_label, call_insert, "2", message], shell=True)
subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=True)
            
gc.collect()

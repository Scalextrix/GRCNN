#!/usr/bin/env python

"""Gather list of Whitelisted projects from Gridcoin NN, call each project for team member CPIDs,
allow user to send a multi transaction to rain GRC on team members"""

import getpass
from urllib2 import urlopen
import gc
import xml.etree.ElementTree as ET
import subprocess
import sys

gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")
grc_amount = raw_input("How much GRC to rain on each project CPID: ")


rosetta_url = ("https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&account_key=Y&xml=1")

def xml_to_db():
    rain_team = raw_input("Which BOINC project to RAIN on: ").lower()
    if rain_team == "rosetta" or rain_team == "rosetta@home":
        project_url = rosetta_url
    else:
        sys.exit("Sorry: BOINC Team not recognised")
        
    root = ET.parse(urlopen(project_url)).getroot()
    cpids = [el.text for el in root.findall('.//user/cpid')]
    rac = [el.text for el in root.findall('.//user/expavg_credit')]
    cpids = zip(*[iter(cpids), iter(rac)]*1)

    conn = sqlite3.connect("GridcoinTeam.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS GRIDCOINTEAM (cpid TEXT, rac TEXT)''') 
    c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?,?);", cpids)
    conn.commit()		
    conn.close()

    conn = sqlite3.connect("GridcoinTeam.db")
    c = conn.cursor()
    cpids = c.execute('select cpid from GRIDCOINTEAM').fetchall()
    rac = c.execute('select rac from GRIDCOINTEAM').fetchall()
    conn.close()

def db_clean():
    conn = sqlite3.connect("GridcoinTeam.db")
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''') 
    conn.commit()		
    conn.close()

def execute_send():     
     subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
     subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=False)
     subprocess.call(['gridcoinresearchd', 'sendmany', addresses, grc_amount, '', '', 'Its raining GRC'], shell=False)
     subprocess.call(['gridcoinresearchd', 'walletlock'], shell=False)
     subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=False)

xml_to_db()
execute_send()
db_clean()
gc.collect()

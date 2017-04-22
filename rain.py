#!/usr/bin/env python

"""Gather list of Whitelisted projects from Gridcoin NN, call each project for team member CPIDs,
allow user to send a multi transaction to rain GRC on team members"""

__author__ = "Steven Campbell AKA Scalextrix"
__copyright__ = "Copyright 2017, Steven Campbell"
__license__ = "The Unlicense"
__version__ = "1.1"

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

amicable_url = "https://sech.me/boinc/Amicable/team_email_list.php?teamid=1806&xml=1"
asteroids_url = "http://asteroidsathome.net/boinc/team_email_list.php?teamid=2218&xml=1"
atlas_url = "http://atlasathome.cern.ch/team_email_list.php?teamid=1869&account_key=Y&xml=1"
burp_url = "https://burp.renderfarming.net/team_email_list.php?teamid=1285&xml=1"
collatz_url = "http://boinc.thesonntags.com/collatz/team_email_list.php?teamid=3029&xml=1"
cosmology_url = "http://www.cosmologyathome.org/team_email_list.php?teamid=3637&xml=1"
csgrid_url = "http://csgrid.org/csg/team_email_list.php?teamid=154&xml=1"
ddm_url = "http://www.distributeddatamining.org/DistributedDataMining/team_email_list.php?teamid=2176&xml=1"
einstein_url = "https://einsteinathome.org/team_email_list.php?teamid=13630&xml=1"
enigma_url = "http://www.enigmaathome.net/team_email_list.php?teamid=2937&xml=1"
find_url = "http://findah.ucd.ie/team_email_list.php?teamid=2198&xml=1"
gpugrid_url = "https://www.gpugrid.net/team_email_list.php?teamid=3493&xml=1"
gridcoin_finance_url = "finance.gridcoin.us/finance/team_email_list.php?teamid=5&xml=1"
leiden_url = "http://boinc.gorlaeus.net/team_email_list.php?teamid=1629&xml=1"
lhc_url = "http://lhcathomeclassic.cern.ch/sixtrack/team_email_list.php?teamid=8128&xml=1"
malaria_url = "http://www.malariacontrol.net/team_email_list.php?teamid=4059&xml=1"
milkyway_url = "http://milkyway.cs.rpi.edu/milkyway/team_email_list.php?teamid=6566&xml=1"
mindmodel_url = "https://mindmodeling.org/team_email_list.php?teamid=2415&xml=1"
moo_url = "http://moowrap.net/team_email_list.php?teamid=2190&xml=1"
nfs_url = "https://escatter11.fullerton.edu/nfs/team_email_list.php?teamid=2353&xml=1"
numberfields_url = "https://numberfields.asu.edu/NumberFields/team_email_list.php?teamid=2069&xml=1"
poem_url = "http://boinc.fzk.de/poem/team_email_list.php?teamid=3147&xml=1"
pogs_url = "http://pogs.theskynet.org/pogs/team_email_list.php?teamid=2020&xml=1"
primegrid_url = "https://www.primegrid.com/team_email_list.php?teamid=4469&xml=1"
rosetta_url = "https://boinc.bakerlab.org/rosetta/team_email_list.php?teamid=12575&xml=1"
sat_url = "http://sat.isa.ru/pdsat/team_email_list.php?teamid=2059&xml=1"
seti_url = "https://setiathome.berkeley.edu/team_email_list.php?teamid=145340&xml=1"
stzaki_url = "http://szdg.lpds.sztaki.hu/szdg/team_email_list.php?teamid=3502&xml=1"
tngrid_url = "https://gene.disi.unitn.it/test/team_email_list.php?teamid=61&xml=1"
vlhc_url = "http://lhcathome2.cern.ch/vLHCathome/team_email_list.php?teamid=2429&xml=1"
wcg_url = "https://www.worldcommunitygrid.org/boinc/team_email_list.php?teamid=30513&xml=1"
wuprop_url = "http://wuprop.boinc-af.org/team_email_list.php?teamid=2243&xml=1"
yafu_url = "http://yafu.myfirewall.org/yafu/team_email_list.php?teamid=260&xml=1"
yoyo_url = "http://www.rechenkraft.net/yoyo/team_email_list.php?teamid=1475&xml=1"


rain_team = raw_input("Which BOINC project to RAIN on: ").lower()
if rain_team == "amicable" or rain_team == "amicable numbers":
	    project_url = amicable_url
elif rain_team == "asteroids" or rain_team == "asteroids@home":
	    project_url = asteroids_url
elif rain_team == "atlas" or rain_team == "atlas@home":
	    project_url = atlas_url
elif rain_team == "burp":
	    project_url = burp_url
elif rain_team == "collatz" or rain_team == "collatz conjecture":
	    project_url = collatz_url
elif rain_team == "cosmology" or rain_team == "cosmology@home":
	    project_url = cosmology_url
elif rain_team == "csg" or rain_team == "csgrid" or rain_team == "citizen science grid":
	    project_url = csgrid_url
elif rain_team == "ddm" or rain_team == "distributed data mining":
	    project_url = ddm_url
elif rain_team == "einstein" or rain_team == "einstein@home":
	    project_url = einstein_url
elif rain_team == "enigma" or rain_team == "enigma@home":
	    project_url = enigma_url
elif rain_team == "find" or rain_team == "find@home":
	    project_url = find_url
elif rain_team == "gpugrid" or rain_team == "gpugrid.net":
	    project_url = gpugrid_url
elif rain_team == "gridcoin finance":
	    project_url = gridcoin_finance_url
elif rain_team == "leiden" or rain_team == "leiden@home":
	    project_url = leiden_url
elif rain_team == "lhc" or rain_team == "lhc@home":
	    project_url = lhc_url
elif rain_team == "malariacontrol" or rain_team == "malaria control":
	    project_url = malaria_url
elif rain_team == "milkyway" or rain_team == "milky way" or rain_team == "milkyway@home":
	    project_url = milkyway_url
elif rain_team == "mindmodeling" or rain_team == "mind modeling" or rain_team == "mindmodeling@home":
	    project_url = mindmodel_url
elif rain_team == "moo" or rain_team == "moowrap":
	    project_url = moo_url
elif rain_team == "nfs" or rain_team == "nfs@home":
	    project_url = nfs_url
elif rain_team == "numberfields" or rain_team == "number fields" or rain_team == "numberfields@home":
	    project_url = numberfields_url
elif rain_team == "poem" or rain_team == "poem@home":
	    project_url = poem_url
elif rain_team == "pogs" or rain_team == "skynet" or rain_team == "theskynet pogs":
	    project_url = pogs_url
elif rain_team == "primegrid" or rain_team == "primegrid@home":
	    project_url = primegrid_url
elif rain_team == "rosetta" or rain_team == "rosetta@home":
	    project_url = rosetta_url
elif rain_team == "sat" or rain_team == "sat@home":
	    project_url = sat_url
elif rain_team == "seti" or rain_team == "seti@home":
	    project_url = seti_url
elif rain_team == "stzaki":
	    project_url = stzaki_url
elif rain_team == "tngrid" or rain_team == "tn-grid":
	    project_url = tngrid_url
elif rain_team == "vlhc" or rain_team == "lhc@home2" or rain_team == "vlhc@home":
	    project_url = vlhc_url
elif rain_team == "wcg" or rain_team == "world community grid":
	    project_url = wcg_url
elif rain_team == "wuprop" or rain_team == "wuprop@home":
	    project_url = wuprop_url
elif rain_team == "yafu" or rain_team == "yafu@home":
	    project_url = yafu_url
elif rain_team == "yoyo" or rain_team == "yoyo@home":
	    project_url = yoyo_url
else:
	    sys.exit("Sorry: BOINC Team not recognised")

mag_or_rac_rain = raw_input("Would you prefer to rain by RAC or Magnitude :").lower()
grc_amount = float(raw_input("How much GRC to rain on BOINC project: "))
account_label = raw_input("Choose Wallet Account Label from which the GRC should be taken: ")
message = str('"'+(raw_input("Enter if you wish to send a message to recipients: "))+'"')
gridcoin_passphrase = getpass.getpass(prompt="What is your Gridcoin Wallet Passphrase: ")
try:
        subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
        subprocess.check_output(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=True)
except subprocess.CalledProcessError:
        sys.exit("Exiting: GRIDCOIN WALLET HAS BEEN LOCKED")
        
root = ET.parse(urlopen(project_url)).getroot()
team_cpids = [el.text for el in root.findall('.//user/cpid')]
team_racs = [el.text for el in root.findall('.//user/expavg_credit')]
team_stats = zip(*[iter(team_cpids),(team_racs)]*1)
print "BOINC project team XML Parsed"

conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS GRIDCOINTEAM''')
c.execute('''DROP TABLE IF EXISTS NNDATA''')
conn.commit()		
conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS GRIDCOINTEAM (cpids TEXT, rac TEXT)''') 
c.executemany("INSERT INTO GRIDCOINTEAM VALUES (?,?);", team_stats)
conn.commit()
print "TEAM DB created"
c.execute('''CREATE TABLE IF NOT EXISTS NNDATA (cpid TEXT, LocalMagnitude TEXT, NeuralMagnitude TEXT, TotalRAC TEXT, Synced Til TEXT, Address TEXT, CPID_Valid TEXT, Witnesses TEXT)''')
filename.encode('utf-8')
with open(filename, 'rb') as NN:
	reader = csv.DictReader(NN)
	field = [(i['CPID'], i['LocalMagnitude'], i['NeuralMagnitude'], i['TotalRAC'], i['Synced Til'], i['Address'], i['CPID_Valid'], i['Witnesses']) for i in reader]
	c.executemany("INSERT INTO NNDATA VALUES (?,?,?,?,?,?,?,?);", field)
conn.commit()		
print "CSV DB created"
conn.text_factory = float
mag_pull = c.execute('select NeuralMagnitude from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM)').fetchall()
conn.text_factory = float
rac_pull = c.execute('select rac from GRIDCOINTEAM where rac != 0 and rac is not null').fetchall()
conn.close()
mag_pull = list(itertools.chain(*mag_pull))
mag_contrib = grc_amount / (sum(mag_pull))
rac_pull = list(itertools.chain(*rac_pull))
rac_contrib = grc_amount / (sum(rac_pull))
tx_counter = int(8192/(len(message) + 50))

if mag_or_rac_rain == "magnitude" or mag_or_rac_rain == "mag":
	conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
	c = conn.cursor()
        subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
        subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=True)
    	position = 0
	print "Gridcoin TXIDs:" 
    	while True:
        	conn.text_factory = str
        	address_db = c.execute('select Address from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM) limit {}, {}'.format(position, tx_counter)).fetchall()
        	conn.text_factory = float
        	magnitude_db = c.execute('select NeuralMagnitude from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM) limit {}, {}'.format(position, tx_counter)).fetchall()
        	if not address_db:
            		conn.close()
            		subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
            		subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=True)
            		del gridcoin_passphrase	
			gc.collect()
			sys.exit("Completed Raining")
        	else:
            		position += tx_counter
            		address_list = list(itertools.chain(*address_db))
            		magnitude_list = list(itertools.chain(*magnitude_db))
            		call_amount = [x * mag_contrib for x in magnitude_list]
            		call_amount = [str("{:.8f}".format(i)) for i in call_amount]
			call_amount = ["0.00000001" if x=="0.00000000" else x for x in call_amount]
            		quotes = '"' * len(magnitude_list)
            		colon = ':' * len(magnitude_list)
            		comma = ',' * len(magnitude_list)
            		call_insert = [val for pair in zip(quotes, address_list, quotes, colon, call_amount, comma) for val in pair]
            		call_insert = str('{'+(''.join(call_insert))+'}')
            		call_insert = call_insert[:-2] + call_insert[-1:]   
            		subprocess.call(['gridcoinresearchd', 'sendmany', account_label, call_insert, "2", message], shell=True)
elif mag_or_rac_rain == "rac":
	conn = sqlite3.connect("C:\\Users\\%s\\AppData\\Roaming\\GridcoinResearch\\reports\\Rain.db" % user_account)
    	c = conn.cursor()
        subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
        subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999'], shell=True)
    	position = 0
	print "Gridcoin TXIDs"
    	while True:
        	conn.text_factory = str
        	address_db = c.execute('select Address from NNDATA where NeuralMagnitude != 0 and NeuralMagnitude is not null and CPID in (select cpids from GRIDCOINTEAM) limit {}, {}'.format(position, tx_counter)).fetchall()
        	conn.text_factory = float
        	rac_db = c.execute('select rac from GRIDCOINTEAM where rac != 0 and rac is not null limit {}, {}'.format(position, tx_counter)).fetchall()
        	if not address_db:
            		conn.close()
            		subprocess.call(['gridcoinresearchd', 'walletlock'], shell=True)
            		subprocess.call(['gridcoinresearchd', 'walletpassphrase', gridcoin_passphrase, '9999999', 'true'], shell=True)
            		del gridcoin_passphrase	
			gc.collect()
			sys.exit("Completed Raining")
        	else:
            		position += tx_counter
            		address_list = list(itertools.chain(*address_db))
            		rac_list = list(itertools.chain(*rac_db))
            		call_amount = [x * rac_contrib for x in rac_list]
            		call_amount = [str("{:.8f}".format(i)) for i in call_amount]
			call_amount = ["0.00000001" if x=="0.00000000" else x for x in call_amount]
            		quotes = '"' * len(rac_list)
            		colon = ':' * len(rac_list)
            		comma = ',' * len(rac_list)
            		call_insert = [val for pair in zip(quotes, address_list, quotes, colon, call_amount, comma) for val in pair]
            		call_insert = str('{'+(''.join(call_insert))+'}')
            		call_insert = call_insert[:-2] + call_insert[-1:]
            		subprocess.call(['gridcoinresearchd', 'sendmany', account_label, call_insert, "2", message], shell=True)


else:
	sys.exit("Sorry: You must choose 'mag'/'magnitude' OR 'RAC'")
del gridcoin_passphrase	
gc.collect()

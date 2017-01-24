# GRCNN

IN DEVELOPMENT

The purpose of this repository is to create a method for users of the Gridcoin crypto-currency (www.gridcoin.us)
to re-distribute the GRC currency to other members who are active on specific BOINC projects, this methodology is
called 'rain' or 'raining'.

This allows for example a project administrator to rain additional GRC funds onto their project if they need a
short term boost in processing power, or between community members as a thankyou, or to bring resources to bear
in preparation for BOINC contests, such as the BOINC Pentathlon (https://www.seti-germany.de/boinc_pentathlon/start.php?&lang=en)

*** PREREQUISITES

This Python script is for Windows only, Linux Gridcoin wallets have no Neural Network.  To operate this Python script you need to install Python 2.7, the Gridcoin Qt wallet must be started with the -server argument to allow GridcoinResearch to accept RPC commands, the gridcoinresearch.conf file must contain 'exportmagnitude=true', 'rpcuser=' and 'rpcpassword=' must be set with a username and password, the NeuralNetwork must also be synchronized.  This Python script must be copied to 'C:\Program Files (x86)\GridcoinResearch' for it to work.

*** INSTRUCTIONS

Open the command prompt:

  > cd C:\Program Files (x86)\GridcoinResearch
  
  > gridcoinresearch -server

Once the GridcoinResearch wallet is fully loaded:

Option A, from the command prompt type:

  > gridcoinresearchd execute syncdpor2
  
Option B, go to the RPC console in the GUI wallet and type:

  > execute syncdpor2

wait for the Neural Network to finish syncing.  *** Note; the NN must sync before proceeding to ensure latest Gridcoin Magnitudes are loaded ***

From the command prompt:

  > rain.py
  
You will need to:

Enter the name of the project on which you wish to rain funds

If you prefer to distribute based on Project RAC or use Gridcoin Magnitude

Enter the total amount of GRC you wish to send to the rainees

Choose the Gridcoin Wallet Account Label from which the GRC should be taken (in GUI wallet see Receive Coins)

Enter an optional message to send in the transaction

Enter your Gridcoin Wallet Passphrase *** Note; the passphrase is not stored in the database or Python script and the entry will be invisible, the wallet will be locked, unlocked, the transaction sent, re-locked and then unlocked for staking only ***

Once all the data is loaded and the transaction completed, you will receive a TXID which can be queried on the block explorer.

A database file 'Rain.db' will be added to the 'C:\Users\User\AppData\Roaming\GridcoinResearch\reports' folder, in case of problems it is safe to delete this file.

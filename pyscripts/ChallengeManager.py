from brownie import *
import json
from brownie import Contract
from web3 import Web3
from brownie.network.gas.strategies import GasNowStrategy
import sys

'''
    Usage (from command line):

    *** LAUNCH 1 VS 1 CHALLENGE ***
    $ python ChallengeManager.py launch_1v1 target1

    *** LAUNCH 1 VS 2 CHALLENGE ***
    $ python ChallengeManager.py launch_1v2 target1 target2
    
    *** ACCEPT CHALLENGE ***    
    $ python ChallengeManager.py accept 
    (accept idealmente non lo lanceremo da qua)
    
    *** FORCE CLOSURE CHALLENGE ***    
    $ python ChallengeManager.py forcedClosure 

    *** TIME LEFT ***
    $ python ChallengeManager.py timeLeft

    *** TIME 1v2 ***
    $ python ChallengeManager.py left1v1 NomeUtente

    *** LEFT 1v1***
    $ python ChallengeManager.py left1v1 NomeUtente
    
    *** BALANCE OF USER ***
    $ python ChallengeManager.py balanceOf NomeUtente
    
    
'''

#*********************************** OCCHIO AL PATH CORRETTO *****************************
p = project.load('/home/cristiano/cartella_test', name = "TokenProject") 
#*****************************************************************************************

p.load_config()

from brownie.project.TokenProject import TokenZ, Challenge

Players = { 'Pacho': '0xc89304bE60b1184281cDacF8e9ADD215B960Fcb8',
            'Citte': '0xebf84b5aa7a66412863F8F66655B5876EF92d91F', 
            'Fra'  : '0x66F26b71404A133F4e478Fb5f52a8105fB324F6e',
            'Becca': '0x4f6374606526BC5892D5C3037cE68da5712B4Efe',
            'Diana': '0x0B3DE044dC8b2902e6B668Cc43bfedB39dfA8fcD'}

playersList =['Pacho','Citte','Fra' ,'Becca','Diana']
#alternativamente facciamo un load da un json, la sintassi sara comunque la stessa di qui sopra, tipo:
#f = open('NomeFile.json')
#Players = json.load(f)
#f.close()

network.connect('ropsten')
#network.connect('development')

print('Connesso a ropsten')

#*********************************** OCCHIO AL PATH CORRETTO *****************************
PrivateData=json.loads(open('/home/cristiano/cartella_test/scripts/private_dict.json').read())
myAccount=accounts.from_mnemonic(PrivateData['personal_account']['mnemonic'], count=1)

print('Caricato account personale di utente')

challenge_address = '0x31806A506a6BDf08ad03022CdD215d25629B37f6'
paytoken_address = '0x44262BE38008972D52400a5AEe77F3240d27C6b4'

challenge = Contract.from_abi('Challenge', challenge_address, Challenge.abi)
paytoken = Contract.from_abi('Paytoken', paytoken_address, TokenZ.abi)

print ('Caricati indirizzi di challenge e paytoken')

if (len(sys.argv) == 3 and sys.argv[1] == 'launch_1v1'):
    print("++++++++++ LAUNCHING 1 VS 1 CHALLENGE +++++++++++")    
    target1 = Players[sys.argv[2]]
    challenge.launch_1v1(target1, {'from':myAccount})


if (len(sys.argv) == 4 and sys.argv[1] == 'launch_1v2'):
    print("++++++++++ LAUNCHING 1 VS 2 CHALLENGE +++++++++++")    
    target1 = Players[sys.argv[2]]
    target2 = Players[sys.argv[3]]
    challenge.launch_1v2(target1, target2, {'from':myAccount})


if (len(sys.argv) == 2 and sys.argv[1] == 'accept'):
    print("++++++++++ ACCEPTING +++++++++++")    
    challenge.accept({'from':myAccount})

if (len(sys.argv) == 1 and sys.argv[1] == 'forcedClosure'):
    print("++++++++++ forcing closure +++++++++++")    
    challenge.forcedClosure({'from':myAccount})

if (len(sys.argv) == 2 and sys.argv[1] == 'timeLeft'):
    print("++++++++++ checking time left +++++++++++")    
    print(challenge.timeLeft({'from':myAccount}))

if (len(sys.argv) == 3 and sys.argv[1] == 'left1v1'):
    print("++++++++++ remaining 1v1: +++++++++++")    
    print(challenge.left1v1(Players[sys.argv[2]], {'from':myAccount}))

if (len(sys.argv) == 3 and sys.argv[1] == 'left1v2'):
    print("++++++++++ remaining 1v2: +++++++++++")    
    print(challenge.left1v2(Players[sys.argv[2]], {'from':myAccount}))

if (len(sys.argv) == 3 and sys.argv[1] == 'balanceOf' and sys.argv[2] in playersList):
    print(f"++++++++++ {sys.argv[2]} +++++++++++")    
    print(paytoken.balanceOf(Players[sys.argv[2]], {'from':myAccount}))


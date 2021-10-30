from mnemonic import Mnemonic
import requests
import genwords
from datetime import datetime
import threading
i=0
import platform,socket,re,uuid,json,psutil,logging
from getsisteminfo import *
now = datetime.now()
date_time = now.strftime("%H:%M:%S")
global date
date=now.strftime('%d-%m-%Y-%H')


def start(i):
    print (i)
    while True:
        try:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            global date
            date=now.strftime('%d-%m-%Y-%H')
            mnemo = Mnemonic("english")
            words = mnemo.generate(strength=256)
            addres=genwords.bip39(words)
            global htmlfile
            htmlfile=requests.get(f"https://blockchain.info/address/{addres}?format=json")
            print(htmlfile.status_code)
            if htmlfile.status_code == 200:    
                try:
                    htmltext = htmlfile.json()
                    balance=htmltext["final_balance"]
                except Exception as e:
                    open(f'Logfile{date}.txt','a+').write(f"""{e}\n{words}\n""")
            if balance > 0:
                open('есть битки{date}.txt','a+').write(f""" 
Addr: {addres} 
Balance: {balance} 
Words: {words} \n""")
            elif balance <= 0:
                open(f'Logfile{date}.txt','a+').write(f"""{date_time} : {words} \n""")
            i+=1
        except Exception as e:
            open(f'Logfile{date}.txt','a+').write(f"""{date_time} : {e}\n{words}\n""")
while True:
    
    try:
        for i in range(16):
            t = threading.Thread(target=start, args=(i,))
            t.start()
        main(status='online', message='')
    except Exception as e:
        open(f'Logfile{date}.txt','a+').write(f"""{e}\n""")
    continue


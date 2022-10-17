import os
import re
import requests
import threading
import pandas as pd
        

class CheckAddress(object):
    
    def checkIPV4(self, ip, **kwargs):
        ipv4Addr = f"{ip}"
        response = os.system("ping -c 1 %s" % ipv4Addr)
        if response == 0:
            x = ipv4Addr
            return x
        else:
            print(f" \n {ipv4Addr} IS NOT ACTIVE \n")

    def threadedCheck(self, df):
        # Will not output to csv
        threads = []
        
        for ip in df["IP Address"]:
            t = threading.Thread(target=self.checkIPV4, args=[ip, ])
            t.start()
            
        for thread in threads:
            thread.join()

    def iterCheck(self, df, path):
        valid_ip = []
            
        for ip in df["IP Address"]:
            ipw = self.checkIPV4(ip)
            valid_ip.append(ipw)
            print(ipw)
            
        df = pd.DataFrame()
        df["Valid IPV4"] = valid_ip
        df.to_csv(f"{path}valid.csv")


def choices():
    print(f"1: Check IPV4 and output to csv (slower) \n"
          f"2: Threaded Check IPV4 (faster) \n")

    choice = int(input("--> "))
    return choice


def main(choice):
    USER = CheckAddress()
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    DATA_PATH = os.path.join(ROOT_PATH, "v4/")
    server_df = pd.read_csv("Servers.csv", index_col=0)

    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
        print("Directory '%s' created \n" % DATA_PATH)
    else:
        pass

    if choice == 1:
        USER.iterCheck(server_df, DATA_PATH)

    elif choice == 2:
        USER.threadedCheck(server_df)

    else:
        print("Incorrect argument. Enter a number from one of the valid choices. \n")


while True:
    main(choices())
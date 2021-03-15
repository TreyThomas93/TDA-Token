# OBJECTIVE: AUTHENTICATE USER AND ONCE DONE, SAVE TOKEN DATA TO MONGODB FOR MAIN PROGRAM TO USE.

# imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from termcolor import colored
import colorama
colorama.init()
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=f"{os.getcwd()}/.env")
import urllib.parse as up
import requests
import time
from pprint import pprint
from datetime import datetime, timedelta
import bcrypt

class AuthenticateTDA():

    def __init__(self, name, username, password, account_id, asset_type, account_type, existing):

        self.username = username

        self.password = password

        self.account_id = account_id

        self.asset_type = asset_type

        self.account_type = account_type

        self.existing = existing

        # CONNECT MONGO
        self.connectMongo()

        time.sleep(2)

        # GET USER
        found = self.getUser(name)

        time.sleep(2)

        if found:

            self.authenticate()
        
    def connectMongo(self):

        print(colored("\nCONNECTING TO MONGO...", "blue"))

        self.client = MongoClient(os.getenv("MONGO_URI"))

        self.db = self.client["Live_Trader"]

        self.users = self.db["users"]

        print(colored("CONNECTED TO MONGO!\n", "green"))

    def getUser(self, name):

        user = self.users.find_one({"Name": name})
        
        if user:

            self.user = user

            return True

        else:

            print("NAME NOT FOUND")

        ask = input("WOULD YOU LIKE TO CREATE NEW USER? (Y/N): ")

        if ask.upper() != "Y":

            return False

        deviceID = input("ENTER DEVICE ID FOR PUSH NOTIFICATIONS (PUSHSAFER): ")

        client_id = input("ENTER CLIENT ID (From TDA Developers Site): ")

        if deviceID != "" and client_id != "":

            obj = {
                "Name": name.strip(),
                "deviceID": int(deviceID),
                "Active": False,
                "ClientID": client_id.strip(),
                "Accounts": {}
            }

            pprint(obj)

            ask = input("IS THE ABOVE INFO CORRECT? (Y/N): ")

            if ask.upper() != "Y":

                return False

            # ADD USER TO USERS COLLECTION
            self.users.insert_one(obj)

            self.user = obj

            return True
            
        print("MISSING FIELDS....TERMINATING")
        
        return False

    def authenticate(self):

        self.client_id = self.user["ClientID"]

        self.redirect_uri = "http://localhost:8080"

        self.username = self.username

        self.password = self.password

        # driver = webdriver.Chrome(
        #     executable_path=f"{os.getcwd()}/chromedriver.exe")

        driver = webdriver.Chrome(ChromeDriverManager().install())

        client_id = self.client_id + '@AMER.OAUTHAP'

        url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + \
            up.quote(self.redirect_uri) + \
            '&client_id=' + up.quote(client_id)

        driver.get(url)

        driver.implicitly_wait(5)

        ubox = driver.find_element_by_id('username0')

        pbox = driver.find_element_by_id('password1')

        ubox.send_keys(self.username)

        pbox.send_keys(self.password)

        driver.find_element_by_id('accept').click()

        driver.find_element_by_id('accept').click()

        while True:

            try:

                code = up.unquote(driver.current_url.split('code=')[1])

                if code != '':

                    break

                else:

                    time.sleep(2)

            except:

                pass

        driver.close()

        resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                                headers={
                                    'Content-Type': 'application/x-www-form-urlencoded'},
                                data={'grant_type': 'authorization_code',
                                    'refresh_token': '',
                                    'access_type': 'offline',
                                    'code': code,
                                    'client_id': self.client_id,
                                    'redirect_uri': self.redirect_uri})

        if resp.status_code != 200:

            raise Exception('COULD NOT AUTHENTICATE!')

        tokens = resp.json()

        if not self.existing:

            tokens["created_at"] = time.time()

            tokens["refresh_exp_date"] = (datetime.now().replace(microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d")

            tokens["AccountID"] = self.account_id

            tokens["Account_Balance"] = 0

            tokens["Available_For_Trading"] = 0

            tokens["Asset_Type"] = self.asset_type

            tokens["Price_Range"] = {"Min": 8, "Max": 30}
            
            tokens["Strategies"] = {}

            tokens["Account_Type"] = self.account_type

            tokens["Limit_Offset"] = 0.005

            tokens["Trailing_Stop_Active"] = False

            # ONCE TOKENS RECEIVED, SAVE TO DATABASE
            self.users.update_one({"Name": self.user["Name"]}, {"$set": {f"Accounts.{account_id}": tokens}})

            print("ACCOUNT AND TOKENS ADDED")
            
        else:

            self.users.update_many({"Name": self.user["Name"]}, {"$set": {
                f"Accounts.{account_id}.created_at": time.time(),
                f"Accounts.{account_id}.refresh_exp_date" : (datetime.now().replace(microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d"),
                f"Accounts.{account_id}.access_token" : tokens["access_token"],
                f"Accounts.{account_id}.refresh_token" : tokens["refresh_token"],
                f"Accounts.{account_id}.expires_in" : tokens["expires_in"],
                }})
        
            print("TOKENS UPDATED!")

if __name__ == "__main__":

    # THIS WILL BE USED TO MARK ALL OF YOUR DATA IN YOUR MONGODB
    name = "John Doe"

    # THIS IS YOUR USERNAME FOR YOUR TDAMERITRADE ACCOUNT
    username = "JohnDoe123"
    
    # THIS IS YOUR PASSWORD FOR YOUR TDAMERITRADE ACCOUNT
    password = "JDoe987"

    # THIS WILL BE USED TO MARK ALL OF YOUR DATA IN YOUR MONGODB
    account_id = 123455678

    # THIS IS THE ASSET TYPE FOR THE SPECIFIED ACCOUNT, I.E EQUITY, OPTIONS, ECT.
    asset_type = "EQUITY"
    
    # THIS IS TO TELL THE PROGRAM IF THIS IS THE PRIMARY ACCOUNT, SECONDARY ACCOUNT, AND SO ON.
    account_type = "PRIMARY"

    # IF USER EXISTS IN MONGO USERS COLLECTION, THEN THIS NEEDS TO BE TRUE.
    existing = False
    
    authenticate = AuthenticateTDA(name, username, password, account_id, asset_type, account_type, existing)



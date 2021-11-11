from datetime import datetime, timedelta
import urllib.parse as up
import colorama
from termcolor import colored
from pymongo import MongoClient
import time
from pprint import pprint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import requests
load_dotenv(dotenv_path=f"{os.getcwd()}/.env")
colorama.init()


class TDAuth:

    def __init__(self):

        self.name = None

        self.username = None

        self.password = None

        self.account_id = None

        self.client_id = None

        self.device_id = None

        self.asset_type = None

        self.account_type = None

        self.redirect_uri = "http://localhost:8080"

    def getTokens(self, user_type):

        self.displayText("Starting Browser....\n")

        driver = webdriver.Chrome(ChromeDriverManager().install())

        client_id = self.client_id + '@AMER.OAUTHAP'

        url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + \
            up.quote(self.redirect_uri) + \
            '&client_id=' + up.quote(client_id)

        self.displayText(f"Redirecting to {url}....\n")

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

        self.displayText("Closing Browser....\n", "success")

        self.displayText("Sending POST request to OAuth!\n", "success")

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

            self.displayText(
                "COULD NOT AUTHENTICATE! - STATUS CODE: {resp.status_code}\n", "error")

            raise Exception('COULD NOT AUTHENTICATE!')

        tokens = resp.json()

        self.displayText("Tokens Received Successfully!\n", "success")

        if user_type == "new":

            tokens["created_at"] = time.time()

            tokens["refresh_exp_date"] = (datetime.now().replace(
                microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d")

            tokens["Account_Balance"] = 0

            tokens["Active"] = True

            # SAVE NEW USER AND TOKENS TO DATABASE
            self.users.insert({
                "Name": self.name,
                "deviceID": self.device_id,
                "ClientID": self.client_id,
                "Accounts": {
                    str(self.account_id): tokens
                },
                "Username": "",
                "Password": ""
            })

            self.displayText(
                "New User And Tokens Added To Database!\n", "success")

            self.displayText(tokens, "success")

        elif user_type == "existing":

            self.users.update_many({"Name": self.name}, {"$set": {
                f"Accounts.{self.account_id}.created_at": time.time(),
                f"Accounts.{self.account_id}.refresh_exp_date": (datetime.now().replace(microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d"),
                f"Accounts.{self.account_id}.access_token": tokens["access_token"],
                f"Accounts.{self.account_id}.refresh_token": tokens["refresh_token"],
                f"Accounts.{self.account_id}.expires_in": tokens["expires_in"],
            }})

            self.displayText(
                "Existing Users Tokens Updated In Database!\n", "success")

            self.displayText(tokens, "success")

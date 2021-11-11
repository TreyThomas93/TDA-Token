import urllib.parse as up
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import requests


class TDAmeritrade:

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

    def fetchTokens(self):

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

        

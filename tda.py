import urllib.parse as up
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import requests
import traceback


class TDAmeritrade:

    def fetchTokenData(self, form_data):

        try:

            driver = webdriver.Chrome(ChromeDriverManager().install())

            client_id = form_data["Client_ID"] + '@AMER.OAUTHAP'

            url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + \
                up.quote("http://localhost:8080") + \
                '&client_id=' + up.quote(client_id)

            driver.get(url)

            driver.implicitly_wait(5)

            ubox = driver.find_element_by_id('username0')

            pbox = driver.find_element_by_id('password1')

            ubox.send_keys(form_data["Username"])

            pbox.send_keys(form_data["Password"])

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
                                       'client_id': form_data["Client_ID"],
                                       'redirect_uri': "http://localhost:8080"})

            if resp.status_code != 200:

                return {"error": "unable to authenticate"}

            return resp.json()

        except Exception:
            
            return {"error": traceback.format_exc()}

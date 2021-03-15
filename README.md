# TDA Tokens Generator

### DESCRIPTION
- This program allows you to obtain access and refresh tokens via OAuth through the TDAmeritrade API. 

### DEPENDENCIES
>[dev-packages]

>[packages]
- selenium
- termcolor
- colorama
- pymongo
- dnspython
- python-dotenv
- requests
- webdriver-manager
- bcrypt

>[venv]
- pipenv

>[requires]
- python_version = "3.8"

### SETUP
- Insert your information at the bottom of the script as stated, and the program will do the rest. 
- You will need your MongoDB uri to connect to Mongo via pymongo. This allows you to save your tokens.
- If user not found in database, you will be prompted to create user.
- There are pre-set fields that will be saved to the database in conjunction with the tokens. These fields are used by the program. 
- If you have any questions, email me and I can assist.
- The deviceID field is the id you receive when you setup a device with the PushSafer web app and mobile app. https://www.pushsafer.com/
- The ClientID is achieved through the TDA developers site. https://developer.tdameritrade.com/apis
- You will need to register as a developer, which is free.
- Once created, go to the My Apps section and create an app. Name it whatever you want.
- You will need the callback url to be set as http://localhost:8080
- Once created, you will need the Consumer Key, which is your client id. This will be saved to your database.

### HOW IT WORKS
- You input your information at the bottom of the script. 
- Create user if need be.
- Selenium and web browser will open browser, automatically insert username/password, click login button, and if successful, redirects you to a verification page. 
- This page will have you either receive a phone call or text message to your phone containing a pin number.
- Phone number is which ever one is saved in your TDA account.
- You can answer a security question aswell.
- Once you do all that and are successful, your tokens will be created and saved to your Mongo database.
- For more info on the TDA authentication process, see this link: https://developer.tdameritrade.com/content/authentication-faq
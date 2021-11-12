# TDA Tokens Generator

### **DESCRIPTION**

- This program allows you to obtain access and refresh tokens via OAuth through the TDAmeritrade API. This uses the Eel library for the GUI.

### **DEPENDENCIES**

---

> [dev-packages]

- autopep8 = "\*"

> [packages]

- selenium = "\_"
- pymongo = "\_"
- dnspython = "\_"
- python-dotenv = "\_"
- requests = "\_"
- webdriver-manager = "\_"
- eel = "\_"
- certifi = "\_"
- bcrypt = "\*"

> [requires]

- python_version = "3.8"

### **HOW IT WORKS**

---

- The purpose of this program is to obtain access and refresh tokens from TDAmeritrade for a specific account, and store that information in your MongoDB database.

- This program uses the Eel library to generate a GUI to make it easier to insert user info.

- You are going to need to connect to the MongoDB Live_Trader database that you created in your cluster. You will need to store your URI in a config.env file stored in the root folder of the program.

- When you start the program, you will see a page with two buttons at the top right. If you currently have any accounts already created, they will populate on the page as well.

#### **Add/Update Account**

- If you clicked the Add/Update Account button, you will see a popup with the following fields below:

- **Name** - This is the users name (First and Last)

- **Username** - This is the username for the TDAmeritrade account you are using.

- **Password** - This is the password for the TDAmeritrade account you are using.

- **Account ID** - This is the account id for the TDAmeritrade account you are using.

#### **Add User**

- If you clicked Add User button, you will see a popup with the following fields below:

- **Name** - This is the users name (First and Last)

- **Username** - This is the username for the TDAmeritrade account you are using.

- **Password** - This is the password for the TDAmeritrade account you are using.

- **Account ID** - This is the account id for the TDAmeritrade account you are using.

- **Device ID** - This is the device id for the Pushsafer API. This id is what allows you to push notifications from the program to your phone or any other device. https://www.pushsafer.com/

- **Client ID** - This is the client id created when you create an app in the TDA Developers site here: https://developer.tdameritrade.com/apis. This is different than your TDAmeritrade account, and you will have to register (Registration is free). Once registered, login and you will see a tab that says My Apps. Click the tab, and click on the tab that says Add A New App. Once clicked, a page will load and will ask you for an App Name, Callback URL, and "What is the purpose of this application". Name it whatever you want, the Callback url needs to be http://localhost:8080, and describe a purpose for the app. Then click the Create App button. Once you do that, go to where you can view all of your apps. Click on the app you just created, and click on the Keys tab. Look for the Consumer Key. That is your **Client ID**.

#### **After Submission**

- After you submit the form, another browser will display and auto input your username and password and then login. If successful, you will be redirected to another page.
- Continue following the directions on the pages. It will ask you to input a code that gets sent to your phone. You can also answer a security question.
- Once you do all that and are successful, you will be redirected to a page that asks you to allow trading, Click the allow button.
- Your tokens will be generated and automatically inserted in your MongoDB Live_Trader database.
- Also, your TDA username and password (which is encrypted using bcrypt) will be inserted into your user object in Mongo as well. This can be used for credentials if you decide to use the web app.
- For more info on the TDA authentication process, see this link: https://developer.tdameritrade.com/content/authentication-faq

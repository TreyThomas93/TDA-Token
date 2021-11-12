import eel
from tda import TDAmeritrade
from mongo import MongoDB
import time
from datetime import datetime, timedelta
from encrypt_password import encrypt_password
import traceback
from pprint import pprint

eel.init("web")

tda = TDAmeritrade()

mongo = MongoDB()

mongo.connectMongo()


@eel.expose
def fetchFormData(form_data):

    try:

        user = mongo.users.find_one({"Name": form_data["Name"]})

        if user:

            form_data["Client_ID"] = user["ClientID"]

        # SEND DATA TO TDA OBJECT TO GET TOKENS AND RETURN IT THE FORM DATA WITH INCLUDED TOKEN DATA
        token_data = tda.fetchTokenData(form_data)

        if "error" in token_data:

            # IF ERROR, THEN RETURN ERROR TO JS AND DISPLAY TO USER
            eel.response({"error": token_data["error"]})

            return

        # SAVE TO MONGO.
        account_id = form_data["Account_ID"]

        token_data["Active"] = True

        token_data["refresh_exp_date"] = (datetime.now().replace(
            microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d")

        token_data["created_at"] = time.time()

        token_data["Account_Position"] = "Paper"

        action = None

        # IF EXISTING USER, THEN ADD ACCOUNT OR UPDATE ACCOUNT
        if user:

            action = "Account Added or Updated!"

            mongo.users.update_one({"Name": form_data["Name"]}, {"$set": {
                f"Accounts.{account_id}": token_data
            }})

        # IF USER DOES NOT EXIST, THEN CREATE NEW USER OBJECT.
        else:

            action = "User Added!"

            mongo.users.insert_one({
                "Name": form_data["Name"],
                "deviceID": form_data["Device_ID"],
                "ClientID": form_data["Client_ID"],
                "Accounts": {
                    str(account_id): token_data
                },
                "Username": form_data["Username"],
                "Password": encrypt_password(form_data["Password"])
            })

        eel.response({"success": action})

        return

    except Exception:
        # IF ERROR, THEN RETURN ERROR TO JS AND DISPLAY TO USER
        eel.response({"error": traceback.format_exc()})

        return


@eel.expose
def callAccounts():
    # FETCH ALL ACCOUNTS AND SEND TO JS TO BE DISPLAYED
    accounts = [user["Accounts"] for user in mongo.users.find()]

    eel.fetchAccounts(accounts[0])


if __name__ == '__main__':

    eel.start("index.html", size=(1024, 768), position=(0, 0))

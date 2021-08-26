from functools import partial
from tkinter import *
from tdauth import TDAuth
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=f"{os.getcwd()}/.env")
from pprint import pprint
import threading


class GUI(TDAuth):

    def __init__(self):

        self.window = Tk()

        super().__init__()

        # SET MAIN WINDOW POSITION TO CENTER OF SCREEN
        app_width = 700

        app_height = 500

        screen_width = self.window.winfo_screenwidth()

        screen_height = self.window.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)

        y = (screen_height / 2) - (app_height / 2)

        self.window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

        #############################################

        # CUSTOM COLORS
        self.bg = "#002B36"

        self.font_color = "white"

        self.window.config(bg=self.bg)

        # SET WINDOW TITLE
        self.window.title("TDA Tokens Generator")

        # CONNECT MONGO
        super().connectMongo()

        self.decisionScreen()

        self.error_label = None

    def saveInfo(self, frame, data, user_type):

        if self.error_label != None:

            self.error_label.destroy()

        if data["Name"] != "" and data["Username"] != "" and data["Password"] != "" and data["Account_ID"] != "":

            self.name = data["Name"]

            self.username = data["Username"]

            self.password = data["Password"]

            try:

                self.account_id = int(data["Account_ID"])

            except:

                self.error_label = Label(
                    frame, text="Account ID Must Be Integer!", fg="red", bg=self.bg)

                self.error_label.grid(
                    columnspan=2, sticky="w", padx=10, pady=5)

                return

            if user_type == "New":

                try:

                    self.device_id = int(data["Device_ID"])
                    
                except:

                    self.error_label = Label(
                        frame, text="Device ID Must Be Integer!", fg="red", bg=self.bg)

                    self.error_label.grid(
                        columnspan=2, sticky="w", padx=10, pady=5)

                    return

                frame.destroy()

                self.client_id = data["Client_ID"]

                self.text = Text(
                    self.window, bg=self.bg, fg=self.font_color, wrap="word", borderwidth=0, highlightthickness=0, spacing1=3)

                self.text.pack(padx=10, pady=10, fill=BOTH, expand=True)

                threading.Thread(target=self.getTokens, args=("new",)).start()

                return

            # CHECK IF USER EXISTS WITH NAME
            user_exists = self.users.find_one(
                {"Name": self.name})

            if user_exists != None:

                frame.destroy()

                self.device_id = user_exists["deviceID"]

                self.client_id = user_exists["ClientID"]

                self.text = Text(
                    self.window, bg=self.bg, fg=self.font_color, wrap="word", borderwidth=0, highlightthickness=0, spacing1=3)

                self.text.pack(padx=10, pady=10, fill=BOTH, expand=True)

                threading.Thread(target=self.getTokens, args=("existing",)).start()

            else:

                self.error_label = Label(
                    frame, text="User Not Found!", fg="red", bg=self.bg)

                self.error_label.grid(
                    columnspan=2, sticky="w", padx=10, pady=5)

        else:

            self.error_label = Label(
                frame, text="An Error Occured. Please Check All Fields.", fg="red", bg=self.bg)

            self.error_label.grid(
                columnspan=2, sticky="w", padx=10, pady=5)

    def existingUser(self):
        """ SETUP ENTRY'S FOR NAME, USERNAME, PASSWORD, ACCOUNT ID, ASSET TYPE, ACCOUNT TYPE
        """
        frame = Frame(self.window, bg=self.bg)

        frame.pack()

        frame.place(anchor="c", relx=.5, rely=.5)

        # SECTION LABEL
        section_label = Label(frame, text="Existing User",
                              font=20, bg=self.bg, fg=self.font_color)

        section_label.grid(column=0, row=0, sticky="w", padx=10, pady=10)

        # NAME ENTRY
        name_label = Label(frame, text="Enter Name:",
                           bg=self.bg, fg=self.font_color)

        name_label.grid(column=0, row=1, sticky="w", padx=10, pady=10)

        name_entry = Entry(frame, width=30)

        name_entry.grid(column=1, row=1)

        # USERNAME ENTRY
        username_label = Label(frame, text="Enter Username:",
                               bg=self.bg, fg=self.font_color)

        username_label.grid(column=0, row=2, sticky="w", padx=10, pady=10)

        username_entry = Entry(frame, width=30)

        username_entry.grid(column=1, row=2)

        # PASSWORD ENTRY
        password_label = Label(frame, text="Enter Password:",
                               bg=self.bg, fg=self.font_color)

        password_label.grid(column=0, row=3, sticky="w", padx=10, pady=10)

        password_entry = Entry(frame, width=30)

        password_entry.grid(column=1, row=3)

        # ACCOUNT ID ENTRY
        account_id_label = Label(
            frame, text="Enter Account ID:", bg=self.bg, fg=self.font_color)

        account_id_label.grid(column=0, row=4, sticky="w", padx=10, pady=10)

        account_id_entry = Entry(frame, width=30)

        account_id_entry.grid(column=1, row=4)

        def saveInfo():

            data = {
                "Name": name_entry.get().strip().title(),
                "Username": username_entry.get().strip(),
                "Password": password_entry.get().strip(),
                "Account_ID": account_id_entry.get().strip()
            }

            self.saveInfo(frame=frame, data=data, user_type="Existing")

        btn = Button(frame, text="Submit", bg="slate gray",
                     fg="white", command=saveInfo)

        btn.grid(column=0, row=5, sticky="w", padx=10)

    def newUser(self):
        """ SETUP ENTRY'S FOR NAME, USERNAME, PASSWORD, ACCOUNT ID, ASSET TYPE, ACCOUNT TYPE, DEVICE ID, CLIENT ID
        """

        frame = Frame(self.window, bg=self.bg)

        frame.pack()

        frame.place(anchor="c", relx=.5, rely=.5)

        # SECTION LABEL
        section_label = Label(frame, text="New User",
                              font=20, bg=self.bg, fg=self.font_color)

        section_label.grid(column=0, row=0, sticky="w", padx=10, pady=10)

        # NAME ENTRY
        name_label = Label(frame, text="Enter Name:",
                           bg=self.bg, fg=self.font_color)

        name_label.grid(column=0, row=1, sticky="w", padx=10, pady=10)

        name_entry = Entry(frame, width=30)

        name_entry.grid(column=1, row=1)

        # USERNAME ENTRY
        username_label = Label(frame, text="Enter Username:",
                               bg=self.bg, fg=self.font_color)

        username_label.grid(column=0, row=2, sticky="w", padx=10, pady=10)

        username_entry = Entry(frame, width=30)

        username_entry.grid(column=1, row=2)

        # PASSWORD ENTRY
        password_label = Label(frame, text="Enter Password:",
                               bg=self.bg, fg=self.font_color)

        password_label.grid(column=0, row=3, sticky="w", padx=10, pady=10)

        password_entry = Entry(frame, width=30)

        password_entry.grid(column=1, row=3)

        # ACCOUNT ID ENTRY
        account_id_label = Label(
            frame, text="Enter Account ID:", bg=self.bg, fg=self.font_color)

        account_id_label.grid(column=0, row=4, sticky="w", padx=10, pady=10)

        account_id_entry = Entry(frame, width=30)

        account_id_entry.grid(column=1, row=4)

        # DEVICE ID ENTRY
        device_id_label = Label(
            frame, text="Enter Device ID:", bg=self.bg, fg=self.font_color)

        device_id_label.grid(column=0, row=5, sticky="w", padx=10, pady=10)

        device_id_entry = Entry(frame, width=30)

        device_id_entry.grid(column=1, row=5)

        # CLIENT ID ENTRY
        client_id_label = Label(
            frame, text="Enter Client ID:", bg=self.bg, fg=self.font_color)

        client_id_label.grid(column=0, row=6, sticky="w", padx=10, pady=10)

        client_id_entry = Entry(frame, width=30)

        client_id_entry.grid(column=1, row=6)

        def saveInfo():

            data = {
                "Name": name_entry.get().strip().title(),
                "Username": username_entry.get().strip(),
                "Password": password_entry.get().strip(),
                "Account_ID": account_id_entry.get().strip(),
                "Client_ID": client_id_entry.get().strip(),
                "Device_ID": device_id_entry.get().strip(),
            }

            self.saveInfo(frame=frame, data=data, user_type="New")

        btn = Button(frame, text="Submit", bg="slate gray",
                     fg="white", command=saveInfo)

        btn.grid(column=0, row=9, sticky="w", padx=10)

    def decisionScreen(self):
        """ ASK THE USER IF THEY ARE EXISTING OR NEW

        [extended_summary]
        """

        frame = Frame(self.window, bg=self.bg)

        frame.pack()

        frame.place(anchor="c", relx=.5, rely=.5)

        def existing_user():

            self.existingUser()

            frame.destroy()

        def new_user():

            self.newUser()

            frame.destroy()

        existing_btn = Button(frame, text="Existing User",
                              padx=5, pady=5, width=10, command=existing_user, bg="slate gray", fg="white")

        existing_btn.grid(row=0, column=0, padx=5, pady=5)

        new_btn = Button(frame, text="New User", padx=5,
                         pady=5, width=10, command=new_user, bg="slate gray", fg="white")

        new_btn.grid(row=0, column=1, padx=5, pady=5)

    def displayText(self, text, type="info"):

        if type == "info":

            self.text.insert(INSERT, text)

        elif type == "success":

            self.text.tag_config('success', foreground="green")

            self.text.insert(INSERT, text, "success")

        elif type == "error":

            self.text.tag_config('error', foreground="red")

            self.text.insert(INSERT, text, "error")

if __name__ == "__main__":

    gui = GUI()

    gui.window.mainloop()

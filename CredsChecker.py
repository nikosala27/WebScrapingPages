import gspread
from tkinter.messagebox import showerror
from google.oauth2.service_account import Credentials


class CredsChecker():
    def __init__(self) -> None:
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file("PATH/TO/GOOGLE/CREDS/JSON", scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        self.sheet_id = 'SHEET ID'
    

    def get_users(self):
        sheet = self.client.open_by_key(self.sheet_id)
        sheet_values = sheet.sheet1.get_all_values()
        users_dict = {}

        for value in sheet_values[1:]:
            if value[0] not in users_dict.keys():
                users_dict[value[0]] = value[1]

        return users_dict
    
    def check_username(self, username, users:dict):
        if username not in users.keys():
            showerror("ERROR", "NIE ZNALEZIIONO TAKIEGO UŻYTKOWNIKA W BAZIE")
            return False
        return True
    
    def check_password(self, username, password, users:dict):
        if users[username] != password:
            showerror("ERROR", "PODANO ZŁE HASŁO UŻYTKOWNIKA")
            return False
        return True

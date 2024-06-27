from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showinfo
from CredsChecker import CredsChecker
from LegaItaly import LegaItaly
from HoneyExtractors import HoneyExtractors
from QuartiItaly import QarItaly
from LatienDade import LatienDae
from LaTienda import LaTienda
from Koningin import Koningin
from PasiekaBarc import PasiekaBarc
from Burnat import Burnat
from Techtron import Techtron
from Apitec import Apitec
from ArtykulyPszczelarskie import ArtykulyPszczelarskie
from Apiart import Apiart
from Adamek import Adamek
from UleWyrobek import UleWyrobek
from Apikoz import Apikoz
from ApikozSklep import ApikozSklep
from PhBarc import phBarc
from Lukasiewicz import Lukasiewicz
import datetime
import os


class GUI():
    def __init__(self) -> None:
        self.root = self.initialization()
        self.root.mainloop()

    def initialization(self):
        root = Tk()
        root.geometry("800x500")
        root.title("WEB SCRAPER")
        root.resizable(False, False)

        # background
        self.background = PhotoImage(file='./images/background.png')
        background_label = Label(root, image=self.background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # left frame
        left_frame = Frame(root, width=400, height=500, bg='#3a7ff6')
        left_frame.place(x=0, y=0)

        # text
        text_box = Text(left_frame, wrap=WORD, bg='#3a7ff6', fg='#ffffff', font=("Segoe UI Semibold", 12, "bold"), bd=0, highlightthickness=0)
        text_box.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.9, relheight=0.8)
        text_box.insert(1.0, "Scraper to program służący do wykonywania całościowych zrzutów wybranych stron internetowych dla celów analitycznych.\n\n1. Wybrać stronę zrzutu\n2.Wybrać ścieżkę gdzie zapisać plik XML\n3.Wpisać swój token użytkownika\n\n\n\n\n\n\n\n\nWłaścicielem programu jest Nikodem Sala, pytania i informacje o błędach kierować na mail: nikodemsala@lyson.com.pl")
        text_box.config(state=DISABLED)

        # Right frame
        right_frame = Frame(root, width=400, height=500, bg='#ffffff')
        right_frame.place(x=400, y=0)

        # Styling for input fields
        style = ttk.Style()
        style.configure("TEntry", padding=10, relief="flat", background="#BFC6D3")
        style.map("TEntry",
                  fieldbackground=[('active', '#BFC6D3')],
                  background=[('readonly', '#BFC6D3')])

        # Center frame for login and password entries
        center_frame = Frame(right_frame, bg='#ffffff')
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Login label
        login_label = ttk.Label(center_frame, text="Login:", font=("Segoe UI Semibold", 12), background="#ffffff")
        login_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        # Login entry
        self.login_entry = ttk.Entry(center_frame, width=40, font=("Segoe UI Semibold", 8, "bold"), foreground="#000000")
        self.login_entry.grid(row=0, column=1, padx=10, pady=10)
        self.login_entry.insert(0, "Login")

        # Password label
        password_label = ttk.Label(center_frame, text="Password:", font=("Segoe UI Semibold", 12), background="#ffffff")
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        # Password entry
        self.password_entry = ttk.Entry(center_frame, width=40, show="*", font=("Helvetica", 8))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_entry.insert(0, "Password")

        # path button
        self.path_button = Button(center_frame, text='Ścieżka', command=self.ask_for_directory, font=("Segoe UI Semibold", 12, "bold"))
        self.path_button.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # path entry
        self.path_entry = ttk.Entry(center_frame, width=40, font=("Segoe UI Semibold", 8, "bold"), foreground="#000000")
        self.path_entry.grid(row=2, column=1, padx=10, pady=10)

        # Dropdown label
        dropdown_label = ttk.Label(center_frame, text="Strona:", font=("Segoe UI Semibold", 12), background="#ffffff")
        dropdown_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        # Dropdown menu
        options = [
              "https://www.latiendadelapicultor.com",
              "https://apicolalospedroches.com",
              "https://www.honey-extractors.com",
              "https://www.legaitaly.com",
              "https://www.quartiitaly.it",
              "https://www.konigin.pl/",
              "http://pasieka-barc.pl/",
              "https://burnat.com.pl",
              "https://techtron-group.pl/",
              "https://apitec.pl/",
              "https://artykulypszczelarskiefit.pl/sklep/",
              "https://apiart.pl/",
              "https://www.adamek.net.pl",
              "https://www.ule-wyrobek.pl/",
              "https://apikoz.pl/",
              "https://sklep.apikoz.pl",
              "https://phbarc.pl/",
              "https://pszczelnictwo.com.pl"
                 ]
        self.dropdown = ttk.Combobox(center_frame, values=options, font=("Segoe UI Semibold", 8), width=40)
        self.dropdown.grid(row=3, column=1, padx=10, pady=10)
        self.dropdown.current(0)

        # Dropdown label
        dropdown_label2 = ttk.Label(center_frame, text="Wszystkie:", font=("Segoe UI Semibold", 12), background="#ffffff")
        dropdown_label2.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        # Dropdown menu
        options2 = ["Tak", "Nie"]
        self.dropdown2 = ttk.Combobox(center_frame, values=options2, font=("Segoe UI Semibold", 8), width=40)
        self.dropdown2.grid(row=4, column=1, padx=10, pady=10)
        self.dropdown2.current(0)

        # start button
        self.start_button = Button(center_frame, text='Start', command=self.start, font=("Segoe UI Semibold", 12, "bold"))
        self.start_button.grid(row=5, column=1, padx=10, pady=10, sticky=E)

        # text Area
        self.text_area = Text(center_frame, wrap=WORD, width=60, height=10, font=("Segoe UI", 8), background="#C5C5C5")
        self.text_area.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

        return root
    
    def ask_for_directory(self):
        selected_folder = filedialog.askdirectory()
        if os.path.isdir(selected_folder) == False:
            self.path_entry.insert(0, "")
            showerror("ERROR", "PODANA SCIEZKA NIE JEST FOLDEREM")
        self.path_entry.insert(0, selected_folder)

    def start(self):
        creds_checker = CredsChecker()
        users = creds_checker.get_users()
        if self.path_entry.get() == "":
            showerror("ERROR", "NIE PODANO ŚCIEŻKI")
            return
        if os.path.isdir(self.path_entry.get()) == False:
            showerror("ERROR", "PODANO NIEPRAWIDŁOWĄ ŚCIEŻKĘ")
            return
        if creds_checker.check_username(self.login_entry.get(), users) == False:
            return
        if creds_checker.check_password(self.login_entry.get(), self.password_entry.get(), users) == False:
            return
        
        selected_path = self.path_entry.get()
        selected_page = self.dropdown.get()
        scraping_methods = {
                                'https://www.quartiitaly.it': {'method': QarItaly(Text).export_products_to_xml},
                                'https://www.legaitaly.com': {'method': LegaItaly().export_products_to_xml},
                                'https://www.honey-extractors.com': {'method': HoneyExtractors().export_products_to_xml},
                                'https://apicolalospedroches.com': {'method': LaTienda().export_products_to_xml},
                                'https://www.latiendadelapicultor.com': {'method': LatienDae().export_products_to_xml},
                                'https://www.konigin.pl/': {'method': Koningin().export_products_to_xml},
                                "http://pasieka-barc.pl/": {'method': PasiekaBarc().export_products_to_xml},
                                'https://burnat.com.pl': {'method': Burnat().export_products_to_xml},
                                'https://techtron-group.pl/': {'method': Techtron().export_products_to_xml},
                                'https://apitec.pl/': {'method': Apitec().export_products_to_xml},
                                'https://artykulypszczelarskiefit.pl/sklep/': {'method': ArtykulyPszczelarskie().export_products_to_xml},
                                'https://apiart.pl/': {'method': Apiart().export_products_to_xml},
                                'https://www.adamek.net.pl': {'method': Adamek().export_products_to_xml},
                                'https://www.ule-wyrobek.pl/': {'method': UleWyrobek().export_products_to_xml},
                                'https://apikoz.pl/': {'method': Apikoz().export_products_to_xml},
                                'https://sklep.apikoz.pl': {'method': ApikozSklep().export_products_to_xml},
                                'https://phbarc.pl/': {'method': phBarc().export_products_to_xml},
                                'https://pszczelnictwo.com.pl': {'method': Lukasiewicz().export_products_to_xml}
        }
        today_str = datetime.datetime.now().strftime("%d%m%y_%H%M%S")

        if self.dropdown2.get() == 'Nie':
            self.disable_elements()

            try:
                scraping_methods[selected_page]['method'](selected_path)
                showinfo("INFORMACJA", f"POMYSLNIE ZAKONCZONO EKSPORT STRONY: {selected_page}")
                finish_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
                self.logger(today_str, f'EKSPORT STRONY: {selected_page} ZAKONCZONY POMYŚLNIE {finish_time}')
            except Exception as e:
                showerror("ERROR", f"WYSTABIL NIEOCZEKWIANY BLAD, kod bledu: {e}")
                finish_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
                self.logger(today_str, f'EKSPORT STRONY: {selected_page} ZAKONCZONY NIEPOMYŚLNIE {finish_time}, blad: {e}')

            self.enable_elements()

        if self.dropdown2.get() == 'Tak':
                self.disable_elements()

                for key in scraping_methods.keys():
                    try:
                        scraping_methods[key]['method'](selected_path)
                        finish_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
                        self.logger(today_str, f'EKSPORT STRONY: {key} ZAKONCZONY POMYŚLNIE {finish_time}')
                    except Exception as e:
                        finish_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
                        self.logger(today_str, f'EKSPORT STRONY: {key} ZAKONCZONY NIEPOMYŚLNIE {finish_time}')
                        pass

                self.enable_elements()
                showinfo("INFORMACJA", f"ZAKONCZONO EKSPORT STRON")
                
    def disable_elements(self):
        self.path_entry.config(state='disabled')
        self.login_entry.config(state='disabled')
        self.password_entry.config(state='disabled')
        self.start_button.config(state='disabled')
        self.path_button.config(state='disabled')

    def enable_elements(self):
        self.path_entry.config(state='normal')
        self.login_entry.config(state='normal')
        self.password_entry.config(state='normal')
        self.start_button.config(state='normal')
        self.path_button.config(state='normal')

    def logger(self, today:str, msg:str):
        if os.path.exists('./logs') == False:
            os.makedirs('logs')
        with open(f'./logs/log_{today}.txt', 'a') as file:
            file.write(f'{msg}\n')
        
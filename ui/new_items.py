from tkinter import *
from tkinter import ttk
from config import ConfigManager
from xml_manager.xml_parser import XMLParser
from database.dao import DAO
from config.ini_manager import INIManager
from tkinter import messagebox


class NewItems(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Paste types")
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.mod_frame = Frame(self.window)
        self.mod_frame.grid(row=2, pady=3, sticky="w")
        Label(self.mod_frame, text="Enter Mod name:").grid(row=0, column=0, padx=3, pady=3)
        self.modSelector = ttk.Combobox(self.mod_frame, values=self.config.get_mods())
        self.modSelector.set(self.config.get_mods()[0])
        self.modSelector.grid(row=0, column=1)
        self.ini_manger = INIManager("app.ini")
        self.database = DAO(self.ini_manger.read_ini("Database", "Database_Name"))
        self.duplicate = IntVar()
        self.duplicate.set(0)

        Checkbutton(self.mod_frame, text="Use Values of Duplicate Items", variable=self.duplicate) \
            .grid(row=0, column=2, padx=10)

        self.text_area = Text(self.window)
        self.text_area.grid(row=1, padx=3, pady=3)

        self.buttons = Frame(self.window)
        self.buttons.grid(row=3, sticky="w")
        Button(self.buttons, text="OK", height=1, width=10, command=self.__add_items) \
            .grid(padx=10, pady=10)
        self.window.wait_window()

    def __add_items(self):
        string_data = self.text_area.get(1.0, END).strip()
        if string_data == "":
            messagebox.showerror(title="Error", message="Empty Data", parent=self.window)
        else:
            if self.__check_xml(string_data) == 1:
                messagebox.showerror(title="Parsing Error", message="Beginning of type is wrong. type has to start "
                                                                    "with <type", parent=self.window)
            elif self.__check_xml(string_data) == 2:
                messagebox.showerror(title="Parsing Error", message="Beginning of type is wrong. types has to start "
                                                                    "with <types", parent=self.window)
            else:
                if string_data.startswith("<type n"):
                    string_data = "<types>\n  " + string_data + "\n</types>"
                xml_parser = XMLParser(string_data)
                items = xml_parser.get_items()
                for i in items:
                    i.mod = self.modSelector.get()
                    self.database.create_item(item=i, duplicate=self.duplicate.get())
                self.window.destroy()

    def __check_xml(self, text):
        if text.startswith("<type"):
            if text.endswith("</type>"):
                return 0
            else:
                return 2

        elif text.startswith("<types>"):
            if text.endswith("</types>"):
                return 0
            else:
                return 2
        else:
            return 1


def testWindow():
    window = Tk()
    NewItems(window)
    window.mainloop()

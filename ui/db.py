from tkinter import *

from database.init_db import InitDatabase
from config.ini_manager import INIManager
from database.dao import DAO


class DB(object):
    DATABASE_NAME = "dayz_items"
    INI_FILE = "../app.ini"
    manage_ini = INIManager(INI_FILE)

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)
        db_actions = [("New Database", "new"), ("Use Existing", "existing")]
        self.selected_db_action = StringVar()
        self.selected_db_action.set("existing")

        Radiobutton(self.configFrame, text=db_actions[0][0], variable=self.selected_db_action,
                    value=db_actions[0][1]).grid(row=6, column=0,
                                                 pady=10)
        Radiobutton(self.configFrame, text=db_actions[1][0], variable=self.selected_db_action,
                    value=db_actions[1][1]).grid(row=6, column=1)

        Label(self.configFrame, text="Database Name").grid(row=7, column=0, sticky="w")

        self.db_name = StringVar()
        self.db_name.set(self.manage_ini.read_ini("Database", "Database_Name"))
        self.db_name_entry = Entry(self.configFrame, textvariable=self.db_name)
        self.db_name_entry.grid(row=7, column=1, sticky="e", pady=5)
        self.db_status = StringVar()
        self.db_status.set("Database Connected to: " + self.manage_ini.read_ini("Database", "Database_Name"))
        Label(self.configFrame,
              textvariable=self.db_status).grid(
            columnspan=2, row=8, column=0,
            sticky="w")
        button_frame = Frame(self.window)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        Button(button_frame, text="Init Database", width=12, command=self.__init_db).grid(row=0, column=1, sticky="w",
                                                                                          padx=5)

        # windows.center(self.window)
        self.window.wait_window()

    def __init_db(self):
        if len(self.db_name.get().split(".")) != 2:
            self.db_status.set("Incorrect! Please use DB name with .db extension.")
        else:
            if self.db_name.get().split(".")[1] != "db":
                self.db_status.set("Incorrect! Please use DB name with .db extension.")
            else:
                if self.selected_db_action.get() == "new":
                    InitDatabase(self.db_name.get())
                    self.manage_ini.write_ini(section="Database", sub_section="Database_Name", value=self.db_name.get())
                    self.db_status.set("Database connected to: "+self.db_name.get())
                else:
                    if DAO(self.db_name.get()).items_table_exist():
                        self.manage_ini.write_ini(section="Database", sub_section="Database_Name", value=self.db_name.get())
                        self.db_status.set("Database connected to: "+self.db_name.get())
                    else:
                        self.db_status.set("items table doesn't exist! Please initialize your Database.")

    '''def openTypes(self):
        self.typesDir.set(windows.openFile("xml_manager"))

    def createTest(self):
        if self.v.get() == "create":
            self.passParams()
            self.createDatabase()
            windows.connectionSuccess(self.window)
            if self.typesDir.get() != "":
                windows.writeTypesToDatabase(self.typesDir.get())
        else:
            self.testDB()

    def createDatabase(self):
        try:
            dao.createDB(self.database.get())
            dao.loadDB(windows.getContent(windows.dataPath + "\\GENESIS.sql"))
        except Exception as e:
            windows.showError(self.window, "Error", "Failed to connect:\n" + str(e))
            windows.deleteParams()

    def testDB(self):
        self.passParams()
        try:
            dao.getNominalByType("gun")
            windows.connectionSuccess(self.window)
        except Exception as e:
            windows.showError(self.window, "Error", "Failed to connect:\n" + str(e))
            windows.deleteParams()

    def set(self):
        self.passParams()
        self.window.destroy()
        dao.setColumnNames()

    def passParams(self):
        dao.setConnectionParams(self.username.get(),
                                self.password.get(),
                                self.port.get(),
                                self.database.get(),
                                self.HostName.get(),
                                "8.0")

        dao.setConnectionParams(self.username.get(),
                                self.password.get(),
                                self.port.get(),
                                self.database.get(),
                                self.HostName.get(),
                                dao.getOdbcVersion())'''


def testWindow():
    window = Tk()
    DB(window)

    window.mainloop()

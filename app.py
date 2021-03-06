from tkinter import *
from tkinter import ttk
from config import ConfigManager
from database.dao import DAO
from model.item import Item
from ui.db import DB
from ui.new_items import NewItems
from ui.combo_box_manager import ComboBoxManager
from config.ini_manager import INIManager
from xml_manager.xml_writer import XMLWriter
import tkinter.filedialog as filedialog


class GUI(object):
    def __init__(self, main_container: Tk):
        #
        self.config = ConfigManager('config.xml')
        self.ini_manger = INIManager("app.ini")
        self.database = DAO(self.ini_manger.read_ini("Database", "Database_Name"))
        #
        self.window = main_container
        self.window.wm_title("Loot Editor v0.98.6")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.menu_bar = Menu(self.window)
        #
        self.__create_menu_bar()
        self.__create_entry_frame()
        self.__create_tree_view()
        self.__create_side_bar()
        self.__populate_items()
        #
        self.tree.bind("<ButtonRelease-1>", self.__fill_entry_frame)

    def __create_menu_bar(self):
        # file menus builder
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Setup Database", command=self.__open_db_window)
        file_menu.add_separator()
        file_menu.add_command(label="Add Items", command=self.__open_items_window)
        file_menu.add_command(label="Export XML File", command=self.__export_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)

        # database menus builder

        # mod menus builder
        mods_menu = Menu(self.menu_bar, tearoff=0)
        mods_menu.add_command(label="Deselect All")
        mods_menu.add_command(label="Select All")
        mods_menu.add_separator()
        for mod in self.config.get_mods():
            int_var = IntVar()

            mods_menu.add_checkbutton(label=mod, variable=int_var)
            int_var.set(1)

        # help menus builder
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="visit the loot editor github for ")

        # building menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Mods In Use", menu=mods_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # configuring menu bar
        self.window.config(menu=self.menu_bar)

    def __create_entry_frame(self):
        self.entryFrameHolder = Frame(self.window)
        self.entryFrameHolder.grid(row=0, column=0, sticky="nw")
        self.entryFrame = Frame(self.entryFrameHolder)
        self.entryFrame.grid(padx=8, pady=6)
        # labels
        Label(self.entryFrame, text="Name").grid(row=0, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Nominal").grid(row=1, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Min").grid(row=2, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Restock").grid(row=3, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Lifetime").grid(row=4, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Usages").grid(row=5, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Tiers").grid(row=6, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Type").grid(row=7, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Sub Type").grid(row=8, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Rarity").grid(row=9, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Mod").grid(row=10, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Trader").grid(row=11, column=0, sticky="w", pady=5)
        # input variables
        self.id = IntVar()
        self.name = StringVar()
        self.nominal = StringVar()
        self.min = StringVar()
        self.restock = StringVar()
        self.lifetime = StringVar()
        self.usages = StringVar()
        self.tires = StringVar()
        self.type = StringVar()
        self.sub_type = StringVar()
        self.rarity = StringVar()
        self.mod = StringVar()
        self.trader = StringVar()
        self.dynamic_event = IntVar()
        self.count_in_cargo = IntVar()
        self.count_in_hoarder = IntVar()
        self.count_in_map = IntVar()
        self.count_in_player = IntVar()
        # form fields
        self.nameField = Entry(self.entryFrame, textvariable=self.name)
        self.nameField.grid(row=0, column=1, sticky="w")
        self.nominalField = Entry(self.entryFrame, textvariable=self.nominal)
        self.nominalField.grid(row=1, column=1, sticky="w")
        self.minField = Entry(self.entryFrame, textvariable=self.min)
        self.minField.grid(row=2, column=1, sticky="w")
        self.restockField = Entry(self.entryFrame, textvariable=self.restock)
        self.restockField.grid(row=3, column=1, sticky="w")
        self.lifetimeField = Entry(self.entryFrame, textvariable=self.lifetime)
        self.lifetimeField.grid(row=4, column=1, sticky="w")
        self.usagesListBox = Listbox(self.entryFrame, height=4, selectmode="multiple", exportselection=False, )
        self.usagesListBox.grid(row=5, column=1, pady=5, sticky="w")
        usages = self.config.get_usages()
        for i in usages:
            self.usagesListBox.insert(END, i)

        self.tiersListBox = Listbox(self.entryFrame, height=4, selectmode="multiple", exportselection=False, )
        self.tiersListBox.grid(row=6, column=1, pady=5, sticky="w")
        tires = self.config.get_tires()
        for i in tires:
            self.tiersListBox.insert(END, i)
        self.typeOption = OptionMenu(self.entryFrame, self.type, *self.config.get_types()[1:])
        self.typeOption.grid(row=7, column=1, sticky="w", pady=5)
        self.subtypeAutoComp = ComboBoxManager(self.entryFrame, self.config.get_sub_types(), highlightthickness=1)
        self.subtypeAutoComp.grid(row=8, column=1, sticky="w", pady=5)
        self.rarityOption = OptionMenu(self.entryFrame, self.rarity, *self.config.get_rarities())
        self.rarityOption.grid(row=9, column=1, sticky="w", pady=5)
        self.modField = Entry(self.entryFrame, textvariable=self.mod)
        self.modField.grid(row=10, column=1, sticky="w", pady=5)
        self.traderField = Entry(self.entryFrame, textvariable=self.trader)
        self.traderField.grid(row=11, column=1, sticky="w")
        # check boxes frame
        self.checkBoxFrame = Frame(self.entryFrameHolder)
        self.checkBoxFrame.grid(row=1, column=0, columnspan=2, sticky="w")
        self.dynamic_event_check = Checkbutton(self.checkBoxFrame, text="Dynamic Event", variable=self.dynamic_event)
        self.dynamic_event_check.grid(row=0, column=0, sticky="w")
        self.count_in_cargo_check = Checkbutton(self.checkBoxFrame, text="Count in Cargo", variable=self.count_in_cargo)
        self.count_in_cargo_check.grid(row=1, column=0, sticky="w")
        self.count_in_hoarder_check = Checkbutton(self.checkBoxFrame, text="Count in Hoarder",
                                                  variable=self.count_in_hoarder)
        self.count_in_hoarder_check.grid(row=2, column=0, sticky="w")
        self.count_in_map_check = Checkbutton(self.checkBoxFrame, text="Count in Map", variable=self.count_in_map)
        self.count_in_map_check.grid(row=3, column=0, sticky="w")
        self.count_in_player_check = Checkbutton(self.checkBoxFrame, text="Count in Player",
                                                 variable=self.count_in_player)
        self.count_in_player_check.grid(row=4, column=0, sticky="w")

        Button(self.checkBoxFrame, text="Update", width=8, command=self.__update_item). \
            grid(row=5, column=0, pady=5, sticky="w")

        Button(self.checkBoxFrame, text="Delete", width=8, command=self.__delete_item). \
            grid(row=5, column=1, pady=5, sticky="w")

    def __create_tree_view(self):
        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")

        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(0, weight=1)
        self.column_info = self.config.get_tree_heading()
        self.tree = ttk.Treeview(self.treeFrame, columns=self.column_info[0], height=40)
        for col in self.column_info[1]:
            self.tree.heading(col[2], text=col[0], command=lambda _col=col[0]:
            self.tree_view_sort_column(self.tree, _col, False), )
            self.tree.column(col[2], width=col[1], stretch=0)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.treeView = self.tree

        vertical = ttk.Scrollbar(self.treeFrame, orient=VERTICAL)
        horizontal = ttk.Scrollbar(self.treeFrame, orient=HORIZONTAL)

        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="we")
        self.tree.config(yscrollcommand=vertical.set)
        self.tree.config(xscrollcommand=horizontal.set)
        vertical.config(command=self.tree.yview)
        horizontal.config(command=self.tree.xview)

    def __create_side_bar(self):
        self.filterFrameHolder = Frame(self.window)
        self.filterFrameHolder.grid(row=0, column=2, sticky="n")

        self.filterFrame = LabelFrame(self.filterFrameHolder, text="Filter")
        self.filterFrame.grid(row=1, column=0, pady=5)

        Label(self.filterFrame, text="Type").grid(row=1, column=0, sticky="w")
        Label(self.filterFrame, text="Subtype").grid(row=2, column=0, sticky="w")

        self.type_for_filter = StringVar()
        self.type_for_filter.set("all")
        OptionMenu(self.filterFrame, self.type_for_filter, *self.config.get_types()). \
            grid(row=1, column=1, sticky="w", padx=5)
        self.sub_type_combo_for_filter = ComboBoxManager(self.filterFrame, self.config.get_sub_types(),
                                                         highlightthickness=1, width=15)
        self.sub_type_combo_for_filter.grid(row=2, column=1, sticky="w", pady=5, padx=5)

        Button(self.filterFrame, text="Filter", width=12, command=self.__filter_items).grid(columnspan=2, pady=5,
                                                                                            padx=10, sticky='nesw')
        self.buttons_frame = Frame(self.filterFrame)
        self.buttons_frame.grid(row=4, columnspan=2)
        # Button(self.buttons, text="view linked items", width=12).grid(row=3)
        Button(self.buttons_frame, text="Search by Name", width=12, command=self.__search_by_name).grid(row=4)

    def __update_item(self):
        updated_item = Item()
        updated_item.id = self.id.get()
        updated_item.name = self.name.get()
        updated_item.nominal = self.nominal.get()
        updated_item.min = self.min.get()
        updated_item.lifetime = self.lifetime.get()
        updated_item.restock = self.restock.get()
        usages = self.usagesListBox.curselection()
        values = [self.usagesListBox.get(i) for i in usages]
        usages = ",".join(values)
        updated_item.usage = usages
        tires = self.tiersListBox.curselection()
        tire_values = [self.tiersListBox.get(i) for i in tires]
        tires = ",".join(tire_values)
        updated_item.tire = tires
        updated_item.rarity = self.rarity.get()
        updated_item.item_type = self.type.get()
        updated_item.sub_type = self.subtypeAutoComp.get()
        updated_item.mod = self.mod.get()
        print(updated_item.mod)
        updated_item.trader = self.trader.get()
        updated_item.dynamic_event = self.dynamic_event.get()
        updated_item.count_in_hoarder = self.count_in_hoarder.get()
        updated_item.count_in_cargo = self.count_in_cargo.get()
        updated_item.count_in_map = self.count_in_map.get()
        updated_item.count_in_player = self.count_in_player.get()
        self.database.update_item(updated_item)
        self.__populate_items()

    def __delete_item(self):
        self.database.delete_item(self.id.get())
        self.__populate_items()

    def __populate_items(self, items=None):
        if items is None:
            items = self.database.all_items()
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())
        for i in items:
            self.tree.insert("", "end", text=i[0], value=i[1:13])

    def __search_by_name(self):
        if self.name.get() != "":
            self.__populate_items(self.database.search_by_name(self.name.get()))

    def __filter_items(self):
        item_type = self.type_for_filter.get()
        if item_type == "all":
            self.__populate_items(self.database.all_items())
        else:
            if self.sub_type_combo_for_filter.get() != "":
                sub_type = self.sub_type_combo_for_filter.get()
            else:
                sub_type = None
            self.__populate_items(self.database.search_by_name(item_type, sub_type))

    def __fill_entry_frame(self, event):
        tree_row = self.tree.item(self.tree.focus())
        id = tree_row['text']
        item = self.database.get_item(id)
        self.id.set(id)
        self.name.set(item.name)
        self.nominal.set(item.nominal)
        self.min.set(item.min)
        self.lifetime.set(item.lifetime)
        self.restock.set(item.restock)
        self.mod.set(item.mod)
        self.trader.set(item.trader)
        usages = self.config.get_usages()
        _usages = str(item.usage).split(',')
        for i in range(len(usages)):
            self.usagesListBox.select_clear(i)
        for i in range(len(usages)):
            for j in _usages:
                if usages[i] == j:
                    self.usagesListBox.select_set(i)
        tires = self.config.get_tires()
        _tires = str(item.tire).split(',')
        for i in range(len(tires)):
            self.tiersListBox.select_clear(i)
        for i in range(len(tires)):
            for j in _tires:
                if tires[i] == j:
                    self.tiersListBox.select_set(i)

        self.rarity.set(item.rarity)
        self.type.set(item.item_type)
        self.subtypeAutoComp.set_value(item.sub_type)
        self.dynamic_event.set(item.dynamic_event)
        self.count_in_hoarder.set(item.count_in_hoarder)
        self.count_in_cargo.set(item.count_in_cargo)
        self.count_in_map.set(item.count_in_map)
        self.count_in_player.set(item.count_in_player)

    def __open_db_window(self):
        DB(self.window)

    def __open_items_window(self):
        NewItems(self.window)
        self.__populate_items()

    def __export_xml(self):
        file = filedialog.asksaveasfile(mode="a", defaultextension=".xml")
        xml_writer = XMLWriter(filename=file.name)
        items = self.database.get_items()
        xml_writer.export_xml(items)

    def tree_view_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda _col=col: self.tree_view_sort_column(tv, _col, not reverse))


window = Tk()
GUI(window)
window.mainloop()

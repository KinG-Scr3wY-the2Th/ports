#!/usr/bin/env python

from gi.repository import Gtk, GObject
import sys
installer = "/usr/local/lib/gbi/"
#sys.path.append(installer)
sys.path.append("/home/ericbsd/gbi/src/")
from language import Language
from installType import Types
from keyboard import Keyboard
from timezone import TimeZone
from use_disk import UFSDisk
from partition import Partitions
from use_zfs import ZFS
from root import RootUser
from addUser import AddUser
from install import Installs

logo = "/usr/local/lib/gbi/logo.png"

class MainWindow:

    def delete(self, widget, event=None):
        Gtk.main_quit()
        return False

    def next_page(self, widget, notebook):
        page = self.notebook.get_current_page()
        if page == 0:
            self.lang.save_selection()
            Kbbox = Gtk.VBox(False, 0)
            Kbbox.show()
            self.kb = Keyboard(self.button3)
            get_kb = self.kb.get_model()
            Kbbox.pack_start(get_kb, True, True, 0)
            label = Gtk.Label("Keyboard")
            self.notebook.insert_page(Kbbox, label, 1)
            self.window.show_all()
            self.notebook.next_page()
            self.button1.set_sensitive(True)
            self.button3.set_sensitive(False)
        elif page == 1:
            self.kb.save_selection()
            Tbbox = Gtk.VBox(False, 0)
            Tbbox.show()
            self.tz = TimeZone(self.button3)
            get_tz = self.tz.get_model()
            Tbbox.pack_start(get_tz, True, True, 0)
            label = Gtk.Label("TimeZone")
            self.notebook.insert_page(Tbbox, label, 2)
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(False)
        elif page == 2:
            typebox = Gtk.VBox(False, 0)
            typebox.show()
            self.types = Types()
            get_types = self.types.get_model()
            typebox.pack_start(get_types, True, True, 0)
            label = Gtk.Label("Types")
            self.notebook.insert_page(typebox, label, 3)
            self.window.show_all()
            self.notebook.next_page()
        elif page == 3:
            if self.types.get_type() == "disk":
                Udbox = Gtk.VBox(False, 0)
                Udbox.show()
                self.partition = UFSDisk(self.button3)
                get_UD = self.partition.get_model()
                Udbox.pack_start(get_UD, True, True, 0)
                label = Gtk.Label("UFS Disk Configuration")
                self.notebook.insert_page(Udbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
            elif self.types.get_type() == "custom":
                Pbox = Gtk.VBox(False, 0)
                Pbox.show()
                self.partition = Partitions(self.button3)
                get_part = self.partition.get_model()
                Pbox.pack_start(get_part, True, True, 0)
                label = Gtk.Label("UFS Custom Configuration")
                self.notebook.insert_page(Pbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
            elif self.types.get_type() == "zfs":
                Zbox = Gtk.VBox(False, 0)
                Zbox.show()
                self.partition = ZFS(self.button3)
                get_ZFS = self.partition.get_model()
                Zbox.pack_start(get_ZFS, True, True, 0)
                label = Gtk.Label("ZFS Configuration")
                self.notebook.insert_page(Zbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
        elif page == 4:
            self.partition.save_selection()
            Rbox = Gtk.VBox(False, 0)
            Rbox.show()
            self.rootuser = RootUser(self.button3)
            get_root = self.rootuser.get_model()
            Rbox.pack_start(get_root, True, True, 0)
            label = Gtk.Label("Root Password")
            self.notebook.insert_page(Rbox, label, 5)
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(False)
        elif page == 5:
            self.rootuser.save_selection()
            Abox = Gtk.VBox(False, 0)
            Abox.show()
            self.adduser = AddUser(self.button3)
            get_adduser = self.adduser.get_model()
            Abox.pack_start(get_adduser, True, True, 0)
            label = Gtk.Label("Adding User")
            self.notebook.insert_page(Abox, label, 6)
            self.button3.set_label("Install")
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(False)
        elif page == 6:
            self.adduser.save_selection()
            Ibox = Gtk.VBox(False, 0)
            Ibox.show()
            self.isntall = Installs(self.button1, self.button2, self.button3, self.notebook)
            get_install = self.isntall.get_model()
            Ibox.pack_start(get_install, True, True, 0)
            label = Gtk.Label("Installation")
            self.notebook.insert_page(Ibox, label, 7)
            self.window.show_all()
            self.notebook.next_page()
            self.button1.set_sensitive(False)
            self.button2.set_sensitive(False)
            self.button3.set_sensitive(False)

    def back_page(self, widget):
        page = self.notebook.get_current_page()
        if page == 1:
            self.button1.set_sensitive(False)
        elif page == 6:
            print page
            self.button3.set_label("Next")
        self.notebook.prev_page()
        self.button3.set_sensitive(True)

    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect("delete_event", self.delete)
        self.window.set_border_width(0)
        self.window.set_size_request(700, 500)
        self.window.set_resizable(False)
        self.window.set_title("GhostBSD Installer")
        self.window.set_border_width(0)
        self.window.set_icon_from_file(logo)
        mainVbox = Gtk.VBox(False, 0)
        mainVbox.show()
        self.window.add(mainVbox)
        # Create a new self.notebook
        self.notebook = Gtk.Notebook()
        mainVbox.pack_start(self.notebook, True, True, 0)
        self.notebook.show()
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)
        vbox = Gtk.VBox(False, 0)
        vbox.show()
        self.lang = Language()
        get_lang = self.lang.get_model()
        vbox.pack_start(get_lang, True, True, 0)
        label = Gtk.Label("Language")
        self.notebook.insert_page(vbox, label, 0)

        # Set what page to start at Language
        self.notebook.set_current_page(0)

        # Create buttons
        self.table = Gtk.Table(1, 6, True)

        self.button1 = Gtk.Button(label='Back')
        self.button1.connect("clicked", self.back_page)
        self.table.attach(self.button1, 3, 4, 0, 1)
        self.button1.show()
        self.button1.set_sensitive(False)
        
        self.button2 = Gtk.Button(label='Cancel')
        self.button2.connect("clicked", self.delete)
        self.table.attach(self.button2, 4, 5, 0, 1)
        self.button2.show()
        
        self.button3 = Gtk.Button(label='Next')
        self.button3.connect("clicked", self.next_page, self.notebook)
        self.table.attach(self.button3, 5, 6, 0, 1)
        self.button3.show()

        self.table.set_col_spacings(5)
        self.table.show()
        mainVbox.pack_start(self.table, False, False, 0)
        mainVbox.set_border_width(5)
        self.window.show_all()

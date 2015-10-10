#!/usr/bin/env python
#
#####################################################################
# Copyright (c) 2010-2015, GhostBSD. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistribution's of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistribution's in binary form must reproduce the above
#    copyright notice,this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES(INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#####################################################################

import gtk
import os.path
from subprocess import Popen, call
import shutil

# installer python script path
tmp = "/home/ghostbsd/.gbi/"
installer = "/usr/local/lib/gbi/"
time = '%stimezone' % tmp
signal = '%ssignal' % tmp
disk_schem = '%sscheme' % tmp

# script to starts
to_language = 'python %slanguage.py' % installer
to_keyboard = 'python %skeyboard.py' % installer
to_time = 'python %stimezone.py' % installer
to_type = 'python %stype.py' % installer
to_upgrade = 'python %stype.py' % installer
to_use_disk = 'python %suse_disk.py' % installer
to_partition = 'python %spartition.py' % installer
to_zfs = 'python %suse_zfs.py' % installer
to_root = 'python %sroot.py' % installer
to_user = 'python %suser.py' % installer
Part_label = '%spartlabel' % tmp
to_prepart = 'python %sprepart.py' % installer


# Function to close window.
def close_application(widget):
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    call("setxkbmap us", shell=True)
    gtk.main_quit()


# Function to go next.
def keyboard_window(widget):
    Popen(to_keyboard, shell=True)
    gtk.main_quit()


def language_window(widget):
    Popen(to_language, shell=True)
    call("setxkbmap us", shell=True)
    gtk.main_quit()


def time_window(widget):
    Popen(to_time, shell=True)
    gtk.main_quit()


def type_window(widget):
    if os.path.exists(time):
        Popen(to_type, shell=True)
        gtk.main_quit()


def disk_window(widget, nxt):
    read_file = open(signal, 'r')
    nxt = read_file.read()
    if nxt == 'disk':
        Popen(to_use_disk, shell=True)
        gtk.main_quit()
    elif nxt == 'custom':
        Popen(to_partition, shell=True)
        gtk.main_quit()
    elif nxt == 'zfs':
        Popen(to_zfs, shell=True)
        gtk.main_quit()

def custom_window(widget):
        Popen(to_partition, shell=True)
        gtk.main_quit()


def back_window(widget):
    read_file = open(signal, 'r')
    nxt = read_file.readlines()[0].rstrip()
    if nxt == 'disk':
        Popen(to_use_disk, shell=True)
        gtk.main_quit()
    elif nxt == 'custom':
        Popen(to_partition, shell=True)
        gtk.main_quit()
    elif nxt == "zfs":
        Popen(to_zfs, shell=True)
        gtk.main_quit()


def root_window(widget, data):
    partlabel = '%spartlabel' % tmp
    if data is True:
        if os.path.exists(partlabel):
            rd = open(partlabel, 'r')
            part = rd.readlines()
            print part
            # Find GPT scheme.
            rschm = open(disk_schem, 'r')
            schm = rschm.readlines()[0]
            print schm
            # if 'GPT' in schm:
            #     fs = part[1].split()[-1]
            #     print fs
            #     boot = part[0]
            #     if 'BOOT' in boot:
            #         pass
            #     else:
            #         message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK)
            #         message.set_markup("Boot patition is missing")
            #         message.run()
            #         message.destroy()
            #     if fs == '/':
            #         Popen(to_root, shell=True)
            #         gtk.main_quit()
            #     else:
            #         message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK)
            #         message.set_markup("Root(/) file system is missing")
            #         message.run()
            #         message.destroy()
            # else:
            #     fs = part[0].split()[-1]
            #     print(fs)
            #     if fs == '/':
            Popen(to_root, shell=True)
            gtk.main_quit()
            #     else:
            #         message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK)
            #         message.set_markup("Root(/) file system is missing")
            #         message.run()
            #         message.destroy()
        else:
            message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK)
            message.set_markup("No partition added")
            message.run()
            message.destroy()
    else:
        Popen(to_root, shell=True)
        gtk.main_quit()


def user_window(widget):
    Popen(to_user, shell=True)
    gtk.main_quit()


def language_bbox(horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", keyboard_window)
    return bbox


def Keyboard_bbox(horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_GO_BACK)
    bbox.add(button)
    button.connect("clicked", language_window)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", time_window)
    return bbox


def time_bbox(horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_GO_BACK)
    bbox.add(button)
    button.connect("clicked", keyboard_window)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", type_window)
    return bbox


def type_bbox(Next, horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_GO_BACK)
    bbox.add(button)
    button.connect("clicked", time_window)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", disk_window, Next)
    return bbox


def use_disk_bbox(horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_GO_BACK)
    bbox.add(button)
    button.connect("clicked", type_window)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", root_window, False)
    return bbox


def partition_bbox(horizontal, spacing, layout):
    bbox = gtk.HButtonBox()
    bbox.set_border_width(5)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)
    button = gtk.Button(stock=gtk.STOCK_GO_BACK)
    bbox.add(button)
    button.connect("clicked", type_window)
    button = gtk.Button(stock=gtk.STOCK_CANCEL)
    bbox.add(button)
    button.connect("clicked", close_application)
    button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
    bbox.add(button)
    button.connect("clicked", root_window, True)
    return bbox

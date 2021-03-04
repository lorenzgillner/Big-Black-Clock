#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio

filler = "<span font='Mono 64' weight='bold'>00</span>"

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(13)
        self.set_default_size(320, 120)
        self.set_resizable(True)

        self.running = False
        
        self.h = 0 
        self.m = 0
        self.s = 0

        self.h_s = "00"
        self.m_s = "00"
        self.s_s = "00"
        
        cbox = Gtk.Box(spacing=10)
        cbox.set_homogeneous(False)
        labelh = Gtk.Label()
        labelh.set_markup(filler)
        cbox.pack_start(labelh, True, True, 0)
        labelc0 = Gtk.Label()
        labelc0.set_markup("<span font='Mono 32' weight='bold'>:</span>")
        cbox.pack_start(labelc0, False, True, 0)
        labelm = Gtk.Label()
        labelm.set_markup(filler)
        cbox.pack_start(labelm, True, True, 0)
        labelc1 = Gtk.Label()
        labelc1.set_markup("<span font='Mono 32' weight='bold'>:</span>")
        cbox.pack_start(labelc1, True, True, 0)
        labels = Gtk.Label()
        labels.set_markup(filler)
        cbox.pack_start(labels, True, True, 0)

        self.add(cbox)
        
        hbar = Gtk.HeaderBar(title="Big Black Clock")
        hbar.set_show_close_button(True)
        self.set_titlebar(hbar)

        button = Gtk.Button(label="Start")
        button.get_style_context().add_class("suggested-action")
        button.connect("clicked", self.do_the_thing, labelh, labelm, labels)
        hbar.pack_start(button)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.reset, labelh, labelm, labels)
        hbar.pack_start(button)
    
    def tick(self, labelh, labelm, labels):
        if (self.s + 1) > 59:
            self.s = 0
            self.s_s = "00"

            if (self.m + 1) > 59:
                self.m = 0
                self.m_s = "00"
                
                if (self.h + 1) > 23:
                    self.h = 0
                    self.h_s = "00"

                else:
                    self.h += 1
                    self.h_s = str(self.h) if self.h > 9 else "0" + str(self.h)

            else:
                self.m += 1
                self.m_s = str(self.m) if self.m > 9 else "0" + str(self.m)

        else:
            self.s += 1
            self.s_s = str(self.s) if self.s > 9 else "0" + str(self.s)

        labelh.set_markup("<span font='Mono 64' weight='bold'>" + self.h_s + "</span>")
        labelm.set_markup("<span font='Mono 64' weight='bold'>" + self.m_s + "</span>")
        labels.set_markup("<span font='Mono 64' weight='bold'>" + self.s_s + "</span>")

        return self.running

    def start(self, button, labelh, labelm, labels):
        self.running = True
        button.set_label("Stop")
        button.get_style_context().add_class("destructive-action")
        self.timeout_id = GLib.timeout_add(1000, self.tick, labelh, labelm, labels)

    def reset(self, butoon, labelh, labelm, labels):
        labelh.set_markup(filler)
        labelm.set_markup(filler)
        labels.set_markup(filler)
        self.h = 0
        self.m = 0
        self.s = 0

    def stop(self, button):
        self.running = False
        button.set_label("Start")
        button.get_style_context().remove_class("destructive-action")
        button.get_style_context().add_class("suggested-action")
        GLib.source_remove(self.timeout_id)

    def do_the_thing(self, button, labelh, labelm, labels):
        if not self.running:
            self.start(button, labelh, labelm, labels)
        else:
            self.stop(button)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


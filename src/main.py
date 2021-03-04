# main.py
#
# Copyright 2020 Latesil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, Handy, GObject, Gdk
from .window import ExifRemoverWindow


class Application(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='com.github.Latesil.exif-remover',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self._init_style()
        self._window = None

    @GObject.Property(type=ExifRemoverWindow, flags=GObject.ParamFlags.READABLE)
    def window(self):
        return self._window

    def do_startup(self):
        Gtk.Application.do_startup(self)
        Handy.init()

    def _init_style(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/Latesil/exif-remover/com.github.Latesil.exif-remover.css')
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_activate(self):
        if not self._window:
            self._window = ExifRemoverWindow(self)
        self._window.present()


def main(version):
    app = Application()
    return app.run(sys.argv)

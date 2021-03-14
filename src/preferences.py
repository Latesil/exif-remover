# preferences.py
#
# Copyright 2021 Latesil
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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Handy, Gio


@Gtk.Template(resource_path='/com/github/Latesil/exif-remover/ui/preferences.ui')
class PreferencesWindow(Handy.PreferencesWindow):
    __gtype_name__ = "hdy_preferences_dialog"

    rename_entry = Gtk.Template.Child()
    rename_folder_entry = Gtk.Template.Child()

    def __init__(self, app, *args, **kwargs):
        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.Latesil.exif-remover')
        self.rename_entry.set_text(self.settings.get_string('output-filename'))
        self.rename_folder_entry.set_text(self.settings.get_string('folder-for-clean-photos'))

    @Gtk.Template.Callback()
    def on_rename_entry_changed(self, entry):
        self.settings.set_string('output-filename', entry.get_text())

    @Gtk.Template.Callback()
    def on_rename_folder_entry_changed(self, entry):
        self.settings.set_string('folder-for-clean-photos', entry.get_text())
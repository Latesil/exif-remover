# window.py
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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


@Gtk.Template(resource_path='/com/gitlab/Latesil/exif-remover/window.ui')
class ExifRemoverWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExifRemoverWindow'

    add_button = Gtk.Template.Child()
    rename_checkbox = Gtk.Template.Child()
    preferences_button = Gtk.Template.Child()
    about_button = Gtk.Template.Child()
    rename_entry = Gtk.Template.Child()
    main_info_label = Gtk.Template.Child()
    about_dialog = Gtk.Template.Child()
    preferences_dialog = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_add_button_clicked(self, button):
        print('on_add_button_clicked')

    @Gtk.Template.Callback()
    def on_rename_checkbox_toggled(self, box):
        print('on_rename_checkbox_toggled')

    @Gtk.Template.Callback()
    def on_preferences_button_clicked(self, button):
        preferences = self.preferences_dialog
        preferences.run()
        preferences.destroy()

    @Gtk.Template.Callback()
    def on_about_button_clicked(self, button):
        about = self.about_dialog
        about.run()
        about.destroy()

    @Gtk.Template.Callback()
    def on_rename_entry_changed(self, entry):
        print('on_rename_entry_changed')
        

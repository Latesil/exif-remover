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

from locale import gettext as _
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, GObject
from .start_view import StartView
from .folder_box import FolderBox


@Gtk.Template(resource_path='/com/github/Latesil/exif-remover/window.ui')
class ExifRemoverWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'ExifRemoverWindow'

    active_view = GObject.Property(type=GObject.GObject, default=None)

    content_box = Gtk.Template.Child()
    main_stack = Gtk.Template.Child()
    # open_output_folder_button = Gtk.Template.Child()
    # rename_checkbox = Gtk.Template.Child()
    # preferences_button = Gtk.Template.Child()
    # about_button = Gtk.Template.Child()
    # rename_entry = Gtk.Template.Child()
    # main_info_label = Gtk.Template.Child()
    # about_dialog = Gtk.Template.Child()
    # preferences_dialog = Gtk.Template.Child()
    # info_bar = Gtk.Template.Child()
    # main_box = Gtk.Template.Child()
    # main_list_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.github.Latesil.exif-remover')

        start = StartView()
        self.main_stack.connect("notify::visible-child", self._on_main_stack_visible_child_changed)
        self.main_stack.add_named(start, "startview")

        # self.settings.connect("changed::folder-quantity", self.on_folder_quantity_changed, None)

        # if self.settings.get_string("output-filename") == "":
        #     self.settings.reset('output-filename')

        # self.rename_checkbox.set_active(self.settings.get_boolean("rename"))

    def _on_main_stack_visible_child_changed(self, k, v):
        self.props.active_view = self.main_stack.props.visible_child

    # @Gtk.Template.Callback()
    # def on_add_button_clicked(self, button):
    #     chooser = Gtk.FileChooserDialog(title=_("Open Folder"),
    #                                     transient_for=self,
    #                                     action=Gtk.FileChooserAction.SELECT_FOLDER,
    #                                     buttons=(_("Cancel"), Gtk.ResponseType.CANCEL,
    #                                              _("OK"), Gtk.ResponseType.OK))
    #     response = chooser.run()
    #     if response == Gtk.ResponseType.OK:
    #         f = chooser.get_filename()
    #         new_box = FolderBox(f)
    #         new_box.set_visible(True)
    #         new_row = Gtk.ListBoxRow()
    #         new_row.add(new_box)
    #         new_row.set_visible(True)
    #         new_row.set_selectable(False)
    #         self.main_list_box.add(new_row)
    #         chooser.destroy()
    #     else:
    #         chooser.destroy()

    # @Gtk.Template.Callback()
    # def on_rename_checkbox_toggled(self, box):
    #     if box.get_active():
    #         self.settings.set_boolean('rename', True)
    #     else:
    #         self.settings.set_boolean('rename', False)

    # @Gtk.Template.Callback()
    # def on_preferences_button_clicked(self, button):
    #     preferences = self.preferences_dialog
    #     self.rename_entry.set_text(self.settings.get_string('output-filename'))
    #     preferences.run()
    #     preferences.hide()

    # @Gtk.Template.Callback()
    # def on_about_button_clicked(self, button):
    #     about = self.about_dialog
    #     about.run()
    #     about.hide()

    # @Gtk.Template.Callback()
    # def on_rename_entry_changed(self, entry):
    #     self.settings.set_string('output-filename', entry.get_text())

    # @Gtk.Template.Callback()
    # def on_ExifRemoverWindow_destroy(self, w):
    #     self.settings.set_int('folder-quantity', 0)

    # @Gtk.Template.Callback()
    # def on_open_folder_button_clicked(self, btn):
    #     folder = getattr(btn, 'folder')
    #     GLib.spawn_async(['/usr/bin/xdg-open', folder])

    # @Gtk.Template.Callback()
    # def on_open_output_folder_button_clicked(self, btn):
    #     folder = getattr(btn, 'output_folder')
    #     GLib.spawn_async(['/usr/bin/xdg-open', folder])


# file_box.py
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
from locale import gettext as _
import threading
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GObject
from .helpers import get_files_and_folders, clear_metadata


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/file_box.ui")
class FileBox(Gtk.Box):
    __gtype_name__ = "FileBox"

    path = GObject.Property(type=str, default=None)
    same_folder = GObject.Property(type=bool, default=True)

    exif_file_box = Gtk.Template.Child()
    file_image_event_box = Gtk.Template.Child()
    file_image = Gtk.Template.Child()
    exif_file_label = Gtk.Template.Child()
    change_file_output_box = Gtk.Template.Child()
    set_file_folder_row = Gtk.Template.Child()
    change_output_label = Gtk.Template.Child()
    set_file_folder_button = Gtk.Template.Child()
    reset_file_folder_revealer = Gtk.Template.Child()
    close_exif_file_button = Gtk.Template.Child()
    clear_exif_file_button = Gtk.Template.Child()

    def __init__(self, app, path):
        super().__init__()
        self._application = app
        self._window = app.props.window
        self.settings = Gio.Settings.new('com.github.Latesil.exif-remover')
        self.props.path = path

        if self.props.path is None:
            print('Sorry, something went wrong (path is empty)')
            return

        self.path = self.props.path
        self.custom_path_set = False
        self.exif_file_label.props.label = self.path
        self.parent_folder = GLib.path_get_dirname(self.path)
        self.allowed_files = ['jpg', 'png', 'jpeg']

    @Gtk.Template.Callback()
    def on_file_image_event_box_clicked(self, event, widget):
        print("on_file_image_event_box_clicked")

    @Gtk.Template.Callback()
    def on_enter_notify_event(self, event, widget):
        image_style_context = self.folder_image.get_style_context()
        image_style_context.add_class('half-opacity')

    @Gtk.Template.Callback()
    def on_leave_notify_event(self, event, widget):
        image_style_context = self.folder_image.get_style_context()
        image_style_context.remove_class('half-opacity')

    @Gtk.Template.Callback()
    def on_close_exif_file_clicked(self, button):
        parent = self._window.main_stack.get_visible_child()
        self.destroy()
        if not parent.folders_view_container.get_children():
            self._window.main_stack.set_visible_child_name(self._window.start_view.props.title)

    @Gtk.Template.Callback()
    def on_clear_exif_file_clicked(self, button):
        output_folder = self.get_output_path()
        input_file = Gio.File.new_for_path(self.path)
        name = self.get_output_filename(output_folder)

        output_file = Gio.File.new_for_path(
            GLib.build_pathv(
                GLib.DIR_SEPARATOR_S, [
                    output_folder,
                    name
                ]
            )
        )

        try:
            input_file.copy(output_file, Gio.FileCopyFlags.NONE)
        except GLib.Error as err:
            if err.code == 2:  # file exists
                print('skipped: ', output_file.get_path())
            else:
                print(err.domain, ':', err.message, 'code:', err.code)
                return

    @Gtk.Template.Callback()
    def on_change_file_output_box_changed(self, box):
        if box.props.active == 0:  # same folders
            self.set_folder_row.props.visible = False
            self.props.same_folder = True
            self.settings.reset("output-folder")
            self.custom_path_set = False
        else:
            self.set_folder_row.props.visible = True
            self.props.same_folder = False
            if self.change_output_label.props.label != '/new/output/folder':  # not good but...
                self.settings.set_string("output-folder", self.change_output_label.props.label)
                self.custom_path_set = True

    @Gtk.Template.Callback()
    def on_set_file_folder_button_clicked(self, button):
        self.custom_path_set = True
        self.reset_file_folder_revealer.set_reveal_child(True)
        chooser = Gtk.FileChooserNative.new(_("Open Folder"),
                                            self._window,
                                            Gtk.FileChooserAction.SELECT_FOLDER)
        response = chooser.run()
        if response == Gtk.ResponseType.ACCEPT:
            f = chooser.get_filename()
            if self.settings.set_string("output-folder", f):
                self.change_output_label.props.label = f
            else:
                print('Sorry, folder:', f, 'was not writable')
            chooser.destroy()
        else:
            self.reset_file_folder_revealer.set_reveal_child(False)
            chooser.destroy()

    @Gtk.Template.Callback()
    def on_reset_file_folder_button_clicked(self, button):
        self.settings.reset("output-folder")
        self.reset_file_folder_revealer.set_reveal_child(False)
        self.change_output_label.props.label = '/new/output/folder'
        self.custom_path_set = False

    def clean_file_metadata(self, i, o):
        clear_metadata(i, o)

    def get_output_path(self):
        output_folder_path = self.settings.get_string("output-folder")  # "" by default
        output_final_folder = self.settings.get_string("folder-for-clean-photos")  # 'cleared' by default

        if self.props.same_folder:  # same where file was
            if output_folder_path == "":
                output_folder_path = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [
                    self.parent_folder, output_final_folder
                ])
        else:
            if output_folder_path == "":
                output_folder_path = GLib.build_pathv(
                    GLib.DIR_SEPARATOR_S, [
                        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
                        output_final_folder
                    ]
                )

        output_folder_path_file = Gio.File.new_for_path(output_folder_path)
        if not GLib.file_test(output_folder_path, GLib.FileTest.EXISTS | GLib.FileTest.IS_DIR):
            Gio.File.make_directory(output_folder_path_file)

        return output_folder_path

    def get_output_filename(self, file, n=1):
        if self.settings.get_boolean('rename'):
            if self.settings.get_string("output-filename") == "":
                self.settings.reset('output-filename')
            name = self.settings.get_string('output-filename') + "_" + str(n)
        else:
            name = GLib.path_get_basename(self.path)

        return name

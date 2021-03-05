import threading
import time

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, GObject
from .helpers import get_files_and_folders
from .exif_file import ExifFile


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/FilesView.ui")
class FilesView(Gtk.Stack):
    __gtype_name__ = "FilesView"

    title = GObject.Property(type=str, default=None)
    files_view_container = Gtk.Template.Child()
    files_revealer = Gtk.Template.Child()
    selected_children_label = Gtk.Template.Child()
    show_only_selected_checkbox = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__()

        self.app = app
        self._window = self.app.props.window
        self.headerbar = self._window.left_header
        self.allowed_files = ['jpg', 'png', 'jpeg']
        self.connect('notify::title', self.on_title_changed)

    @Gtk.Template.Callback()
    def on_selected_children_changed(self, widget):
        if widget.get_selected_children():
            self.files_revealer.set_reveal_child(True)
            selected_children = len(widget.get_selected_children())
            self.selected_children_label.props.label = str(selected_children)
        else:
            self.files_revealer.set_reveal_child(False)

    @Gtk.Template.Callback()
    def on_select_all_button_clicked(self, button):
        self.files_view_container.select_all()

    @Gtk.Template.Callback()
    def on_unselect_all_button_clicked(self, button):
        self.files_view_container.unselect_all()
        self.show_only_selected_checkbox.props.active = False
        for i in self.files_view_container.get_children():
            i.props.visible = True

    @Gtk.Template.Callback()
    def on_show_only_selected_checkbox_toggled(self, checkbox):
        selected = self.files_view_container.get_selected_children()
        all_photos = self.files_view_container.get_children()
        if checkbox.props.active:
            for i in all_photos:
                if i not in selected:
                    i.props.visible = False
        else:
            for i in all_photos:
                i.props.visible = True

    def on_title_changed(self, widget, param):
        if self.props.title is None:
            return

        files_in_view = []
        self.headerbar.props.title = self.props.title
        folders, files = get_files_and_folders(self.props.title)

        for f in files:
            simple_file = Gio.File.new_for_path(f)
            try:
                name, ext = simple_file.get_basename().rsplit('.', 1)
            except ValueError:
                ext = ""

            if ext in self.allowed_files and not name.startswith('.'):
                files_in_view.append(f)

        if files_in_view:
            for f in files_in_view:
                thread = threading.Thread(target=self.update_file_view, args=(f,))
                thread.daemon = True
                thread.start()

    def update_file_view(self, f):
        GLib.idle_add(self.populate_file_view, f)
        time.sleep(0.2)

    def populate_file_view(self, files):
        exif_file = ExifFile(files)
        self.files_view_container.insert(exif_file, -1)

import gi
import threading
import time
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, GObject
from .helpers import get_files_and_folders
from .exif_file import ExifFile

lock = threading.Lock()

@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/FilesView.ui")
class FilesView(Gtk.Stack):
    __gtype_name__ = "FilesView"

    title = GObject.Property(type=str, default=None)
    files_view_container = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__()

        self.app = app
        self._window = self.app.props.window
        self.headerbar = self._window.left_header
        self.allowed_files = ['jpg', 'png', 'jpeg']
        self.connect('notify::title', self.on_title_changed)

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
                thread = threading.Thread(target=self.populate_file_view, args=(f,))
                thread.daemon = True
                thread.start()

    def populate_file_view(self, file):
        exif_file = ExifFile(file)
        self.files_view_container.insert(exif_file, -1)

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy
from .exif_folder import ExifFolder


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/FoldersView.ui")
class FoldersView(Gtk.Stack):
    __gtype_name__ = "FoldersView"

    folders_view_container = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        exif_folder = ExifFolder()

        self.folders_view_container.add(exif_folder)

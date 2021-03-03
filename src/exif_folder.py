import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFolder.ui")
class ExifFolder(Gtk.Box):
    __gtype_name__ = "ExifFolder"

    exif_folders_label = Gtk.Template.Child()

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.exif_folders_label.props.label = path

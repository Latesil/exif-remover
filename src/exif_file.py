import gi
from locale import gettext as _

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, Gdk


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFile.ui")
class ExifFile(Gtk.Box):
    __gtype_name__ = "ExifFile"

    exif_file_label = Gtk.Template.Child()

    def __init__(self, path):
        super().__init__()
        self.path = path

        self.exif_file_label.props.label = GLib.basename(path)
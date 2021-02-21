import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy

@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/FoldersView.ui")
class FoldersView(Gtk.Stack):
    __gtype_name__ = "FoldersView"

    def __init__(self):
        super().__init__()
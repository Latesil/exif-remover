import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, GObject

@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/StartView.ui")
class StartView(Gtk.Stack):
    __gtype_name__ = "StartView"

    title = GObject.Property(type=str, default="startview")

    def __init__(self):
        super().__init__()
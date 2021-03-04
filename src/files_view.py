import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, GObject


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/FilesView.ui")
class FilesView(Gtk.Stack):
    __gtype_name__ = "FilesView"

    path = GObject.Property(type=str, default=None)

    files_view_main_label = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__()

        self.app = app
        self._window = self.app.props.window
        self.headerbar = self._window.left_header

        self.connect('notify::path', self.on_path_changed)

    def on_path_changed(self, widget, param):
        self.files_view_main_label.props.label = self.props.path
        self.headerbar.props.title = self.props.path

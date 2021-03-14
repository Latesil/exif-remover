import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/FoldersView.ui")
class FoldersView(Gtk.Stack):
    __gtype_name__ = "FoldersView"

    title = GObject.Property(type=str, default="foldersview")

    folders_view_container = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    def add_folder_to_view(self, folder):
        self.folders_view_container.add(folder)

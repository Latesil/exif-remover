import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

@Gtk.Template(resource_path='/com/gitlab/Latesil/exif-remover/folder_box.ui')
class FolderBox(Gtk.Box):

    __gtype_name__ = "FolderBox"

    folder_box_label = Gtk.Template.Child()

    i = 0

    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.gitlab.Latesil.exif-remover')

        FolderBox.i += 1
        self.settings.set_int('folder-quantity', FolderBox.i)
        self.label = label
        self.folder_box_label.set_text(self.label)

    @Gtk.Template.Callback()
    def on_remove_exif_button_clicked(self, button):
        FolderBox.i -= 1

        self.settings.set_int('folder-quantity', FolderBox.i)
        self.get_parent().destroy()
    

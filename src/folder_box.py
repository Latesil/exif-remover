import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk

@Gtk.Template(resource_path='/com/gitlab/Latesil/exif-remover/folder_box.ui')
class FolderBox(Gtk.Box):

    __gtype_name__ = "FolderBox"

    folder_box_label = Gtk.Template.Child()
    remove_exif_button = Gtk.Template.Child()
    folder_box_event_box = Gtk.Template.Child()

    i = 0

    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.gitlab.Latesil.exif-remover')

        FolderBox.i += 1
        self.settings.set_int('folder-quantity', FolderBox.i)
        self.label = label
        self.folder_box_event_box.get_child().set_text(self.label)
        self.output_folder = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES) + '/cleared'

    @Gtk.Template.Callback()
    def on_folder_box_event_box_button_press_event(self, widget, event):
        if event.button == 3:
            FolderBox.i -= 1
            self.settings.set_int('folder-quantity', FolderBox.i)
            self.get_parent().destroy()

    @Gtk.Template.Callback()
    def on_remove_exif_button_clicked(self, button):
        folders, files = get_files_and_folders(self.label)
        for f in files:
            print(f)


def get_files_and_folders(folder, absolute_folders_paths=True):
    folder_list = []
    files_list = []

    path = Gio.File.new_for_path(folder)
    enumerator = path.enumerate_children(Gio.FILE_ATTRIBUTE_STANDARD_NAME, Gio.FileQueryInfoFlags.NONE)
    info = enumerator.next_file()
    while info is not None:
        if info.get_file_type() == Gio.FileType.DIRECTORY:
            if absolute_folders_paths:
                folder_path = path.get_path() + '/' + info.get_name()
            else:
                folder_path = info.get_name()
            folder_list.append(folder_path)
            info = enumerator.next_file()
        else:
            abs_path = path.get_path() + '/' + info.get_name()
            files_list.append(abs_path)
            info = enumerator.next_file()

    return folder_list, files_list

    

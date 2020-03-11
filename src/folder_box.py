import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GExiv2', '0.10')
from gi.repository import Gtk, Gio, GLib, GExiv2, GObject

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
        self.destination_folder = Gio.File.new_for_path(self.output_folder)

        if not GLib.file_test(self.output_folder, GLib.FileTest.EXISTS):
            Gio.File.make_directory(self.destination_folder)


    @Gtk.Template.Callback()
    def on_folder_box_event_box_button_press_event(self, widget, event):
        if event.button == 3:
            FolderBox.i -= 1
            self.settings.set_int('folder-quantity', FolderBox.i)
            self.get_parent().destroy()

    @Gtk.Template.Callback()
    def on_remove_exif_button_clicked(self, button):
        folders, files = get_files_and_folders(self.label)
        GExiv2.initialize()
        for f in files:
            try:
                f_in = Gio.File.new_for_path(f)

                #TODO
                name = f_in.get_basename()

                f_out = Gio.File.new_for_path(self.output_folder + '/' + name)
                f_in.copy(f_out, Gio.FileCopyFlags.NONE)
                exif = GExiv2.Metadata()
                exif.open_path(f_in.get_path())
                exif.clear_comment()
                exif.clear_exif()
                exif.clear_iptc()
                exif.clear_xmp()
                exif.delete_gps_info()

                #TODO
                #exif.erase_exif_thumbnail()

                exif.clear()
                exif.save_file(f_out.get_path())

            except GLib.Error as err:
                print('%s: %s in file: %s (code: %s)' % (err.domain, err.message, f, err.code))
                if err.code == 2: #file exists
                    continue

        #wtf is this?
        infobar = self.get_parent().get_parent().get_parent().get_parent().get_parent().get_children()[1]
        label = infobar.get_children()[0].get_children()[0].get_children()[0].get_children()[0]

        label.set_text('Done')
        infobar.props.revealed = True




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

    

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, Gdk


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFolder.ui")
class ExifFolder(Gtk.Box):
    __gtype_name__ = "ExifFolder"

    exif_folders_label = Gtk.Template.Child()
    set_folder_row = Gtk.Template.Child()
    folder_image = Gtk.Template.Child()

    def __init__(self, app, path):
        super().__init__()
        self._application = app
        self._window = app.props.window
        self.path = path
        self.exif_folders_label.props.label = path

    @Gtk.Template.Callback()
    def on_image_event_box_clicked(self, event, widget):
        GLib.spawn_async(['/usr/bin/xdg-open', self.path])

    @Gtk.Template.Callback()
    def on_enter_notify_event(self, event, widget):
        image_style_context = self.folder_image.get_style_context()
        image_style_context.add_class('half-opacity')


    @Gtk.Template.Callback()
    def on_leave_notify_event(self, event, widget):
        image_style_context = self.folder_image.get_style_context()
        image_style_context.remove_class('half-opacity')

    @Gtk.Template.Callback()
    def on_close_exif_folder_clicked(self, button):
        print('on_close_exif_folder_clicked')

    @Gtk.Template.Callback()
    def on_clear_exif_folder_clicked(self, button):
        print('on_clear_exif_folder_clicked')

    @Gtk.Template.Callback()
    def on_show_files_button_clicked(self, button):
        self._window.set_files_view(self.path)


    @Gtk.Template.Callback()
    def on_change_output_box_changed(self, box):
        if box.props.active == 0:
            self.set_folder_row.props.visible = False
        else:
            self.set_folder_row.props.visible = True

    @Gtk.Template.Callback()
    def on_set_folder_button_clicked(self, button):
        print('on_set_folder_button_clicked')

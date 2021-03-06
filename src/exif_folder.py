import gi
from locale import gettext as _

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, Gdk
from .helpers import get_files_and_folders


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFolder.ui")
class ExifFolder(Gtk.Box):
    __gtype_name__ = "ExifFolder"

    exif_folders_label = Gtk.Template.Child()
    set_folder_row = Gtk.Template.Child()
    folder_image = Gtk.Template.Child()
    change_output_label = Gtk.Template.Child()
    show_files_button = Gtk.Template.Child()
    show_files_row = Gtk.Template.Child()

    def __init__(self, app, path):
        super().__init__()
        self._application = app
        self._window = app.props.window
        self.path = path
        self.exif_folders_label.props.label = path
        self.allowed_files = ['jpg', 'png', 'jpeg']
        self.files_in_view = []
        folders, files = get_files_and_folders(self.path)
        for f in files:
            simple_file = Gio.File.new_for_path(f)
            try:
                name, ext = simple_file.get_basename().rsplit('.', 1)
            except ValueError:
                ext = ""

            if ext in self.allowed_files and not name.startswith('.'):
                self.files_in_view.append(f)
        self.show_files_row.props.subtitle = str(len(self.files_in_view))

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
        parent = self._window.main_stack.get_visible_child()
        self.destroy()
        if not parent.folders_view_container.get_children():
            self._window.main_stack.set_visible_child_name(self._window.start_view.props.title)

    @Gtk.Template.Callback()
    def on_clear_exif_folder_clicked(self, button):
        print('on_clear_exif_folder_clicked')

    @Gtk.Template.Callback()
    def on_show_files_button_clicked(self, button):
        self._window.set_files_view(self.path, self.files_in_view)

    @Gtk.Template.Callback()
    def on_change_output_box_changed(self, box):
        if box.props.active == 0:
            self.set_folder_row.props.visible = False
        else:
            self.set_folder_row.props.visible = True

    @Gtk.Template.Callback()
    def on_set_folder_button_clicked(self, button):
        chooser = Gtk.FileChooserDialog(title=_("Open Folder"),
                                        transient_for=self._window,
                                        action=Gtk.FileChooserAction.SELECT_FOLDER,
                                        buttons=(_("Cancel"), Gtk.ResponseType.CANCEL,
                                                 _("OK"), Gtk.ResponseType.OK))
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            f = chooser.get_filename()
            self.change_output_label.props.label = f
            chooser.destroy()
        else:
            chooser.destroy()

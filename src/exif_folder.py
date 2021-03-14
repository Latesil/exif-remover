import gi
from locale import gettext as _
import threading
import time

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, GLib, Handy, Gdk, GObject
from .helpers import get_files_and_folders, clear_metadata


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFolder.ui")
class ExifFolder(Gtk.Box):
    __gtype_name__ = "ExifFolder"

    path = GObject.Property(type=str, default=None)
    same_folder = GObject.Property(type=bool, default=True)

    exif_folders_label = Gtk.Template.Child()
    set_folder_row = Gtk.Template.Child()
    folder_image = Gtk.Template.Child()
    change_output_label = Gtk.Template.Child()
    show_files_button = Gtk.Template.Child()
    show_files_row = Gtk.Template.Child()
    reset_folder_revealer = Gtk.Template.Child()

    def __init__(self, app, path):
        super().__init__()
        self._application = app
        self._window = app.props.window
        self.settings = Gio.Settings.new('com.github.Latesil.exif-remover')
        self.all_photos_to_process = True
        self.props.path = path

        if self.props.path is None:
            print('Sorry, something went wrong (path is empty)')
            return

        self.path = self.props.path
        self.custom_path_set = False
        self.exif_folders_label.props.label = self.path
        self.allowed_files = ['jpg', 'png', 'jpeg']
        self.files_in_view = []
        self.files_to_process = []
        folders, files = get_files_and_folders(self.path)
        for f in files:
            simple_file = Gio.File.new_for_path(f)
            try:
                name, ext = simple_file.get_basename().rsplit('.', 1)
            except ValueError:
                ext = ""

            if ext.lower() in self.allowed_files and not name.startswith('.'):
                self.files_in_view.append(simple_file)
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
        n = 1
        self.settings.set_boolean('done', False)
        output_folder_path = self.settings.get_string("output-folder")  # "" by default
        output_final_folder = 'cleared'  # TODO not hardcode

        if self.props.same_folder:  # same where file was
            if output_folder_path == "":
                output_folder_path = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [
                    self.path, output_final_folder
                ])
        else:
            if output_folder_path == "":
                output_folder_path = GLib.build_pathv(
                    GLib.DIR_SEPARATOR_S, [
                        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
                        output_final_folder
                    ]
                )

        output_folder_path_file = Gio.File.new_for_path(output_folder_path)
        if not GLib.file_test(output_folder_path, GLib.FileTest.EXISTS | GLib.FileTest.IS_DIR):
            Gio.File.make_directory(output_folder_path_file)

        print('output folder path will be:', output_folder_path)

        if self.all_photos_to_process:
            self.files_to_process = self.files_in_view

        if self.files_to_process:
            count_files_to_process = len(self.files_to_process)
            for file in self.files_to_process:
                input_file = Gio.File.new_for_path(
                    GLib.build_pathv(GLib.DIR_SEPARATOR_S, [file.get_path()])
                )

                if self.settings.get_boolean('rename'):
                    if self.settings.get_string("output-filename") == "":
                        self.settings.reset('output-filename')
                    name = self.settings.get_string('output-filename') + "_" + str(n)
                else:
                    name = input_file.get_basename()

                output_file = Gio.File.new_for_path(
                    GLib.build_pathv(
                        GLib.DIR_SEPARATOR_S, [
                            output_folder_path,
                            name
                        ]
                    )
                )

                try:
                    input_file.copy(output_file, Gio.FileCopyFlags.NONE)
                except GLib.Error as err:
                    if err.code == 2:  # file exists
                        print('skipped: ', output_file.get_path())
                        continue
                    else:
                        print(err.domain, ':', err.message, 'code:', err.code)
                        return

                thread = threading.Thread(target=self.clean_file_metadata, args=[input_file, output_file])
                thread.daemon = True
                thread.start()

                n += 1
                count_files_to_process -= 1

                if count_files_to_process == 0:
                    self.settings.set_boolean('done', True)
                    self._window.recent_folder = output_folder_path
        else:
            print('There is no files to process')
            return

    @Gtk.Template.Callback()
    def on_show_files_button_clicked(self, button):
        self.all_photos_to_process = False
        self._window.set_files_view(self.path, self.files_in_view)

    @Gtk.Template.Callback()
    def on_change_output_box_changed(self, box):
        if box.props.active == 0:  # same folders
            self.set_folder_row.props.visible = False
            self.props.same_folder = True
            self.settings.reset("output-folder")
            self.custom_path_set = False
        else:
            self.set_folder_row.props.visible = True
            self.props.same_folder = False
            if self.change_output_label.props.label != '/new/output/folder':
                self.settings.set_string("output-folder", self.change_output_label.props.label)
                self.custom_path_set = True

    @Gtk.Template.Callback()
    def on_set_folder_button_clicked(self, button):
        self.custom_path_set = True
        self.reset_folder_revealer.set_reveal_child(True)
        chooser = Gtk.FileChooserNative.new(_("Open Folder"),
                                            self._window,
                                            Gtk.FileChooserAction.SELECT_FOLDER)
        response = chooser.run()
        if response == Gtk.ResponseType.ACCEPT:
            f = chooser.get_filename()
            if self.settings.set_string("output-folder", f):
                self.change_output_label.props.label = f
            else:
                print('Sorry, folder:', f, 'was not writable')
            chooser.destroy()
        else:
            self.reset_folder_revealer.set_reveal_child(False)
            chooser.destroy()

    @Gtk.Template.Callback()
    def on_reset_folder_button_clicked(self, button):
        self.settings.reset("output-folder")
        self.reset_folder_revealer.set_reveal_child(False)
        self.change_output_label.props.label = '/new/output/folder'
        self.custom_path_set = False

    def clean_file_metadata(self, input, output):
        GLib.idle_add(self.trigger_metadata_clean, input, output)
        time.sleep(0.2)  # need this for some reason

    def trigger_metadata_clean(self, i, o):
        clear_metadata(i, o)

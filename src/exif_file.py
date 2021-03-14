# exif_file.py
#
# Copyright 2021 Latesil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf


@Gtk.Template(resource_path="/com/github/Latesil/exif-remover/ui/ExifFile.ui")
class ExifFile(Gtk.FlowBoxChild):
    __gtype_name__ = "ExifFile"

    exif_file_label = Gtk.Template.Child()
    exif_file_image = Gtk.Template.Child()

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.basename = GLib.basename(self.path)
        self.set_size_request(150, 230)
        self.exif_file_label.props.label = self.basename
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.path, 120, -1, True)
        self.exif_file_image.set_from_pixbuf(self.image)
        self.set_tooltip_text(self.basename)

    def get_path(self):
        return self.path

    def get_basename(self):
        return self.basename

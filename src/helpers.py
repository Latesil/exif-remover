# helpers.py
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
gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2, Gio, GLib
from typing import Tuple, List, Optional


def get_files_and_folders(folder, absolute_folders_paths=True) -> Tuple[List[str], List[str]]:
    folder_list: List[str] = []
    files_list: List[str] = []
    path: Gio.File = Gio.File.new_for_path(folder)
    enumerator: Optional[Gio.FileEnumerator] = path.enumerate_children(Gio.FILE_ATTRIBUTE_STANDARD_NAME,
                                                                       Gio.FileQueryInfoFlags.NONE)
    info: Optional[Gio.FileInfo] = enumerator.next_file()
    while info is not None:
        if info.get_file_type() == Gio.FileType.DIRECTORY:
            if absolute_folders_paths:
                folder_path: str = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [path.get_path(), info.get_name()])
            else:
                folder_path: str = info.get_name()
            folder_list.append(folder_path)
            info: Optional[Gio.FileInfo] = enumerator.next_file()
        else:
            abs_path: str = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [path.get_path(), info.get_name()])
            files_list.append(abs_path)
            info: Optional[Gio.FileInfo] = enumerator.next_file()

    return folder_list, files_list


def clear_metadata(input_file, output_file):
    exif: GExiv2.Metadata = GExiv2.Metadata()
    exif.open_path(input_file.get_path())

    exif.clear_comment()
    exif.clear_exif()
    exif.clear_iptc()
    exif.clear_xmp()
    exif.delete_gps_info()

    # TODO
    # exif.erase_exif_thumbnail()

    exif.clear()
    exif.save_file(output_file.get_path())

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

# def clear_metadata(input_file, output_file):
#     exif: GExiv2.Metadata = GExiv2.Metadata()
#     exif.open_path(input_file.get_path())

#     exif.clear_comment()
#     exif.clear_exif()
#     exif.clear_iptc()
#     exif.clear_xmp()
#     exif.delete_gps_info()

#     #TODO
#     #exif.erase_exif_thumbnail()

#     exif.clear()
#     exif.save_file(output_file.get_path())

import gi
gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2, Gio

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

def clear_metadata(input_file, output_file):
    exif = GExiv2.Metadata()
    exif.open_path(input_file.get_path())

    exif.clear_comment()
    exif.clear_exif()
    exif.clear_iptc()
    exif.clear_xmp()
    exif.delete_gps_info()

    #TODO
    #exif.erase_exif_thumbnail()

    exif.clear()
    exif.save_file(output_file.get_path())

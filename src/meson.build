pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'exif_remover')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'exif-remover.in',
  output: 'exif-remover',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

exif_remover_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'helpers.py',
  'start_view.py',
  'folders_view.py',
  'exif_folder.py',
  'files_view.py',
  'exif_file.py',
  'AboutDialog.py',
  'preferences.py',
  'file_box.py',
]

install_data(exif_remover_sources, install_dir: moduledir)

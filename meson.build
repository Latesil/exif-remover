project('exif-remover',  
          version: '0.1.1',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')

message('Looking for dependencies')
dependency('glib-2.0')
dependency('gobject-introspection-1.0', version: '>=1.35.9')
dependency('gtk+-3.0', version: '>=3.24.1')
dependency('libhandy-1', version: '>=1.0.0')

appname = 'com.github.Latesil.exif-remover'

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
sizes = ['24', '32', '48', '64', '96', '128', '192', '256', '512']

foreach size : sizes
    install_data([appname + '-' + size + '.png'],
                 rename : [appname + '.png'],
      install_dir: join_paths(get_option('datadir'), 'icons/hicolor/' + size + 'x' + size + '/apps')
    )
endforeach

# install_data([appname + '-symbolic.svg'],
#              rename : [appname + '-symbolic.svg'],
#   install_dir: join_paths(get_option('datadir'), 'icons/hicolor/scalable/apps')
# )

install_data([appname + '-symbolic.svg'],
             rename : [appname + '-symbolic.svg'],
  install_dir: join_paths(get_option('datadir'), 'icons/hicolor/symbolic/apps')
)

message('done with icons')

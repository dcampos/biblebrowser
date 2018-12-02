message('Compiling schemas')

biblebrowser_settings = gnome.compile_schemas()
install_data(
  project_id + '.gschema.xml',
  install_dir: 'share/glib-2.0/schemas'
)

message('Making a .desktop file')
install_data(
  project_id + '.desktop',
  install_dir: join_paths(get_option('datadir'), 'applications')
)

icondir = join_paths(datadir, 'icons/hicolor')
install_data(
  'org.biblebrowser.svg',
  install_dir: join_paths(icondir, 'scalable/apps')
)

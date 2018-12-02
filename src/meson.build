pkgdatadir = join_paths(get_option('prefix'), datadir, meson.project_name())
moduledir = join_paths(pkgdatadir, 'biblebrowser')
#gnome = import('gnome')

biblebrowser_resources = gnome.compile_resources('biblebrowser',
  'biblebrowser.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

#python3 = import('python3')

#conf = configuration_data()
#conf.set('PYTHON', python3.find_python().path())
#conf.set('VERSION', meson.project_version())
#conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
#conf.set('pkgdatadir', pkgdatadir)

#configure_file(
  #input: 'biblebrowser.in',
  #output: 'biblebrowser',
  #configuration: conf,
  #install: true,
  #install_dir: get_option('bindir')
#)

biblebrowser_sources = [
  '__init__.py',
  'biblebrowser.py',
]

install_data(biblebrowser_sources, install_dir: moduledir)

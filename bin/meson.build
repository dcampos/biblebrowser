conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
#conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'bible-browser.in',
  output: 'bible-browser',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

biblebrowser = join_paths(meson.build_root(), 'bin/bible-browser')
run_target('run',
  command: [biblebrowser],
  depends: [
    biblebrowser_resources,
    biblebrowser_settings
  ]
)
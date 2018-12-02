project('bible-browser',
	version: '0.1.01',
	meson_version: '>=0.40.0')

project_id = 'org.biblebrowser'

python3 = import('python3')
gnome = import('gnome')

prefix = get_option('prefix')
bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
localedir = join_paths(prefix, get_option('localedir'))
pkgdatadir = join_paths(datadir, meson.project_name())


#install_data('bin/bible-browser', install_dir: bindir)

message('Installing data files')
subdir('data')
subdir('src')
subdir('bin')
#subdir('po')

meson.add_install_script('postinstall.py')

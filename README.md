# Bible Browser

Bible Browser is a tiny Python GTK+3 application for easily reading multiple Bible versions and comparing them side by side.

## Features

![Bible Browser Screenshot](biblebrowser.png)

* Lookup by book, chapter and verse
* Normal and parallel views
* Highlight current verse
* Plenty of Bible versions available from the SWORD Project

## Installation

The following commands can be used to install the application on your (Linux) system:

```
meson build
cd build
sudo ninja install
```

## Related projects

* [The SWORD Project](http://crosswire.org/sword/index.jsp): a Crosswire project that provides tools for writing Bible-related software.
* [pysword](https://gitlab.com/tgc-dk/pysword/): native Python library for reading SWORD modules.
* [Xiphos](https://github.com/crosswire/xiphos): multi-platform Bible study tool from Crosswire.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

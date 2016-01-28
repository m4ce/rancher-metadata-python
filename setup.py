from distutils.core import setup

version = '0.17.1'

setup(
  name = 'rancher_metadata',
  packages = ['rancher_metadata'],
  version = version,
  description = 'Python library for Rancher Metadata API',
  author = 'Matteo Cerutti',
  author_email = 'matteo.cerutti@hotmail.co.uk',
  url = 'https://github.com/m4ce/python-rancher_metadata',
  download_url = 'https://github.com/m4ce/python-rancher_metadata/tarball/%s' % (version,),
  keywords = ['rancher'],
  classifiers = [],
  install_requires = ["requests"]
)

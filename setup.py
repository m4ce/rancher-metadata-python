from distutils.core import setup

version = '0.17.14'

setup(
  name = 'rancher-metadata',
  packages = ['rancher_metadata'],
  version = version,
  description = 'Python library for Rancher Metadata API',
  author = 'Matteo Cerutti',
  author_email = 'matteo.cerutti@hotmail.co.uk',
  url = 'https://github.com/m4ce/rancher-metadata-python',
  download_url = 'https://github.com/m4ce/rancher-metadata-python/tarball/%s' % (version,),
  keywords = ['rancher'],
  classifiers = [],
  install_requires = ["requests"]
)

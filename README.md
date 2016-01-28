# Python library for Rancher Metadata API
This is a simple Python library that allows to interact with the Rancher Metadata REST API.

Pull requests to add additional API features (as documented at http://docs.rancher.com/rancher/metadata-service/) are very welcome. I only implemented what I needed.

## Install
To install it simply issue the following command:

```
pip install rancher_metadata
```

## Usage
```
from rancher_metadata import MetadataAPI
metadata_api = MetadataAPI(api_url = "http://rancher-metadata/2015-12-19")

print("Container ID: %d" % metadata_api.get_container_id())
print("Container Service ID: %d" % metadata_api.get_container_service_id())
print("Container IP: %s" % metadata_api.get_container_ip())
print("Container Name: %s" % metadata_api.get_container_name())
print("Container Service Name: %s" % metadata_api.get_container_service_name())
print("Container Hostname: %s" % metadata_api.get_container_hostname())

containers = metadata_api.wait_service_containers()
for name, container in containers:
  print("Container %s is up  (IP: %s, Index: %d)" % (name, container['primary_ip'], container['create_index']))

metadata = metadata_api.get_service_metadata()
print(metadata)
```

## Contact
Matteo Cerutti - matteo.cerutti@hotmail.co.uk

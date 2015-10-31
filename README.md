# Rancher Metadata Python API
This is a simple Python API that allows to interact with the Rancher Metadata REST API.

Pull requests to add additional API features (as documented at http://docs.rancher.com/rancher/metadata-service/) are very welcome. I only implemented what I needed.

## Install
To install it simply issue the following command:

```
pip install rancher_metadata
```

## Usage
```
from rancher_metadata import MetadataAPI
metadata_api = MetadataAPI(api_url = "http://rancher-metadata/latest")

print "Container ID: " + metadata_api.get_container_id()
print "Container IP: " + metadata_api.get_container_ip()
print "Container Name: " + metadata_api.get_container_name()
print "Container Service Name: " + metadata_api.get_container_service_name()
print "Container Hostname: " + metadata_api.get_container_hostname()

containers = metadata_api.wait_service_containers()
for container in containers:
  print "Container " + container + " is up  (IP: " + metadata_api.get_container_ip(container) + ", Index: " + metadata_api.get_container_id(container)

metadata = metadata_api.get_service_metadata()
print metadata
```

## Contact
Matteo Cerutti - matteo.cerutti@hotmail.co.uk

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
  print("Container %s is up (IP: %s, Index: %d, Service ID: %d)" % (name, container['primary_ip'], container['create_index'], metadata_api.get_container_service_id(name)))

metadata = metadata_api.get_service_metadata()
print(metadata)

print("Service scale size: %s" % metadata_api.get_service_scale_size())
```

Other examples:

```
# look up all containers
for container in metadata_api.get_containers():
  print(container)

# look up all services
for service in metadata_api.get_services():
  print(service)

# look up all stacks
for stack in metadata_api.get_stacks():
  print(stack)

# look up all hosts
for host in metadata_api.get_hosts():
  print(host)

# look up current container
print(metadata_api.get_container())

# look up a container by name
print(metadata_api.get_container("my_container"))

# look up a container's IP by name
print("A container IP: %s" % metadata_api.get_container_ip("container_name"))

# look up current service
print(metadata_api.get_service())

# look up a specific service running in the current stack
print(metadata_api.get_service(service_name = 'my_service'))

# look up a specific service running in another stack
print(metadata_api.get_service(service_name = 'my_service', stack_name = 'my_stack'))

# look up a specific service's containers running in the current stack
for container in metadata_api.get_service_containers(service_name = 'my_service'):
  print(container)

# look up a specific service's containers running in an another stack
for container in metadata_api.get_service_containers(service_name = 'my_service', stack_name = 'my_stack'):
  print(container)

# look up current stack
print(metadata_api.get_stack())

# look up a specific stack by name
print(metadata_api.get_stack("my_stack"))

# look up services running in current stack
for service in metadata_api.get_stack_services():
  print(service)

# look up services running in another stack
for service in metadata_api.get_stack_services("my_stack"):
  print(service)

# look up current host
print(metadata_api.get_host())

# look up a specific host by name
print(metadata_api.get_host("my_host"))

# returns true if the container is running in Rancher-managed network
if is_network_managed():
  print("I am running in the managed network")
else:
  print("I am running in host-based networking")
```

## Contact
Matteo Cerutti - matteo.cerutti@hotmail.co.uk

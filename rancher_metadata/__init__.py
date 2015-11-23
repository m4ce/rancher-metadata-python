#
# __init__.py
#
# Author: Matteo Cerutti <matteo.cerutti@hotmail.co.uk>
#

import requests
import json
import time
import re

class MetadataAPI:
  def __init__(self, **kwargs):
    if 'api_url' not in kwargs:
      self.api_url = "http://rancher-metadata/latest"
    else:
      self.api_url = kwargs['api_url']

  def is_error(self, data):
    if isinstance(data, dict):
      if 'code' in data and data['code'] == 404:
        return True

    return False

  def api_get(self, query):
    req = requests.get(self.api_url + query, headers = {"Content-Type": "application/json", "Accept": "application/json"}).json()

    if self.is_error(req):
      return None
    else:
      return req

  def get_services(self):
    return self.api_get("/services")

  def get_service(self, service_name = None, stack_name = None):
    if service_name is None:
      return self.api_get("/self/service")
    else:
      if stack_name is None:
        return self.api_get("/services/" + service_name)
      else:
        for s in self.get_services():
          if s['stack_name'] == stack_name and s['service_name'] == service_name:
            return s

  def get_service_field(self, field, service_name, stack_name):
    if service_name is None:
      return self.api_get("/self/service/" + field)
    else:
      if stack_name is None:
        return self.api_get("/services/" + service_name + "/" + field)
      else:
        s = self.get_service(service_name, stack_name)
        if field in s:
          return s[field]
        else:
          return None

  def get_service_scale_size(self, service_name = None, stack_name = None):
    self.get_service_field("scale", service_name, stack_name)

  def get_service_containers(self, service_name = None, stack_name = None):
    self.get_service_field("containers", service_name, stack_name)

  def get_service_metadata(self, service_name = None, stack_name = None):
    self.get_service_field("metadata", service_name, stack_name)

  def get_service_links(self, service_name = None, stack_name = None):
    self.get_service_field("links", service_name, stack_name)

  def wait_service_containers(self, service_name = None, stack_name = None):
    scale = self.get_service_scale_size(service_name, stack_name)
    containers = []

    while True:
      t = self.get_service_containers(service_name, stack_name)

      for n in list(set(t) - set(containers)):
        yield n

      containers = t

      if (len(containers) < scale):
        time.sleep(0.5)
      else:
        break

  def get_stacks(self):
    return self.api_get("/stacks")

  def get_stack(self, stack_name = None):
    if stack_name is None:
      return self.api_get("/self/stack")
    else:
      return self.api_get("/stacks/" + stack_name)

  def get_containers(self):
    return self.api_get("/containers")

  def get_container(self, container_name = None):
    if container_name is None:
      return self.api_get("/self/container")
    else:
      return self.api_get("/containers/" + container_name)

  def get_container_field(self, field, container_name):
    if container_name is None:
      return self.api_get("/self/container/" + field)
    else:
      return self.api_get("/containers/" + container_name + "/" + field)

  def get_container_id(self, container_name = None):
    self.get_container_field("create_index", container_name)

  def get_container_ip(self, container_name = None):
    if container_name is None:
      # are we running within the rancher managed network?
      if self.is_network_managed():
        return self.api_get("/self/container/primary_ip")
      else:
        return self.get_host_ip()
    else:
      return self.api_get("/containers/" + container_name + "/primary_ip")

  def get_container_name(self, container_name = None):
    self.get_container_field("name", container_name)

  def get_container_service_name(self, container_name = None):
    self.get_container_field("service_name", container_name)

  def get_container_hostname(self, container_name = None):
    self.get_container_field("hostname", container_name)

  def get_container_service_id(self, container_name = None):
    index = self.get_container_field("service_index", container_name)

    # use the container name index as the unique service index
    if index is None:
      m = re.search("(\d+)$", self.get_container_name(container_name))
      if m:
        index = m.group(1)

    return index

  def get_container_host_uuid(self, container_name = None):
    index = self.get_container_field("host_uuid", container_name)

  def is_network_managed(self):
    # in managed network, we don't get to see any information about the container :(

    if self.get_container_id():
      return True
    else:
      return False

  def get_hosts(self):
    return self.api_get("/hosts")

  def get_host(self, host_name):
    if host_name is None:
      return self.api_get("/self/host")
    else:
      return self.api_get("/hosts/" + host_name)

  def get_host_field(self, field, host_name):
    if host_name is None:
      return self.api_get("/self/host/" + field)
    else:
      return self.api_get("/hosts/" + host_name + "/" + field)

  def get_host_ip(self, host_name = None):
    self.get_host_field("agent_ip", host_name)

  def get_host_uuid(self, host_name = None):
    self.get_host_field("uuid", host_name)

  def get_host_name(self, host_name = None):
    self.get_host_field("name", host_name)

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
      self.api_url = ["http://rancher-metadata/latest"]
    else:
      if isinstance(kwargs['api_url'], list):
        self.api_url = kwargs['api_url']
      else:
        self.api_url = [kwargs['api_url']]

    if 'max_attempts' in kwargs:
      self.max_attempts = kwargs['max_attempts']
    else:
      self.max_attempts = 3

  def is_error(self, data):
    if isinstance(data, dict):
      if 'code' in data and data['code'] == 404:
        return True

    return False

  def api_get(self, query):
    success = False
    i = 1

    while (i <= self.max_attempts and not success):
      for url in self.api_url:
        try:
          req = requests.get(url + query, headers = {"Content-Type": "application/json", "Accept": "application/json"}).json()
          success = True
          break
        except Exception as e:
          print("Failed to query Rancher Metadata API on " + url + " - Caught exception (" + str(e) + ")")

      i = i + 1

    if not success:
      raise RuntimeError("Failed to query Rancher Metadata API (" + str(i) + " out of " + str(self.max_attempts) + " attempts failed)")

    if self.is_error(req):
      return None
    else:
      return req

  def get_services(self):
    return self.api_get("/services")

  def get_service(self, **kwargs):
    if not kwargs:
      return self.api_get("/self/service")
    else:
      if 'service_name' not in kwargs:
        raise ValueError("Attribute 'service_name' is required")

      if 'stack_name' not in kwargs:
        return self.api_get("/services/" + kwargs['service_name'])
      else:
        for s in self.get_services():
          if s['stack_name'] == kwargs['stack_name'] and s['name'] == kwargs['service_name']:
            return s

  def get_service_field(self, field, **kwargs):
    if not kwargs:
      return self.api_get("/self/service/" + field)
    else:
      if 'service_name' not in kwargs:
        raise ValueError("Attribute 'service_name' is required")

      if 'stack_name' not in kwargs:
        return self.api_get("/services/" + kwargs['service_name'] + "/" + field)
      else:
        s = self.get_service(**kwargs)
        if s and field in s:
          return s[field]
        else:
          return None

  def get_service_scale_size(self, **kwargs):
    return self.get_service_field("scale", **kwargs)

  def get_service_containers(self, **kwargs):
    return self.get_service_field("containers", **kwargs)

  def get_service_metadata(self, **kwargs):
    return self.get_service_field("metadata", **kwargs)

  def get_service_links(self, **kwargs):
    return self.get_service_field("links", **kwargs)

  def wait_service_containers(self, **kwargs):
    scale = self.get_service_scale_size(**kwargs)
    containers = []

    while True:
      t = self.get_service_containers(**kwargs)

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
    return self.get_container_field("create_index", container_name)

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
    return self.get_container_field("name", container_name)

  def get_container_service_name(self, container_name = None):
    return self.get_container_field("service_name", container_name)

  def get_container_stack_name(self, container_name = None):
    return self.get_container_field("stack_name", container_name)

  def get_container_hostname(self, container_name = None):
    return self.get_container_field("hostname", container_name)

  def get_container_service_id(self, container_name = None):
    index = None

    service_index = self.get_container_field("service_index", container_name)

    # use the container name index as the unique service index
    if service_index is None:
      m = re.search("(\d+)$", self.get_container_name(container_name))
      if m:
        index = int(m.group(1))
    else:
      index = int(service_index)

    return index

  def get_container_host_uuid(self, container_name = None):
    return self.get_container_field("host_uuid", container_name)

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
    return self.get_host_field("agent_ip", host_name)

  def get_host_uuid(self, host_name = None):
    return self.get_host_field("uuid", host_name)

  def get_host_name(self, host_name = None):
    return self.get_host_field("name", host_name)

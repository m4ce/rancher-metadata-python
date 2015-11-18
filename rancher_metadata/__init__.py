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

  def api_get(self, query):
    req = requests.get(self.api_url + query, headers = {"Content-Type": "application/json", "Accept": "application/json"})
    return req.json()

  def wait_service_containers(self, service = None):
    scale = self.get_service_scale_size(service)
    containers = []

    while True:
      t = self.get_service_containers(service)

      for n in list(set(t) - set(containers)):
        yield n

      containers = t

      if (len(containers) < scale):
        time.sleep(0.5)
      else:
        break

  def get_service_scale_size(self, service = None):
    if service is None:
      return self.api_get("/self/service/scale")
    else:
      return self.api_get("/services/" + service + "/scale")

  def get_service_containers(self, service = None):
    if service is None:
      return self.api_get("/self/service/containers")
    else:
      return self.api_get("/services/" + service + "/containers")

  def get_service_metadata(self, service = None):
    if service is None:
      return self.api_get("/self/service/metadata")
    else:
      return self.api_get("/services/" + service + "/metadata")

  def get_container_id(self, container = None):
    if container is None:
      return self.api_get("/self/container/create_index")
    else:
      return self.api_get("/containers/" + container + "/create_index")

  def get_container_ip(self, container = None):
    if container is None:
      return self.api_get("/self/container/primary_ip")
    else:
      return self.api_get("/containers/" + container + "/primary_ip")

  def get_container_name(self, container = None):
    if container is None:
      return self.api_get("/self/container/name")
    else:
      return self.api_get("/containers/" + container + "/name")

  def get_container_service_name(self, container = None):
    if container is None:
      return self.api_get("/self/container/service_name")
    else:
      return self.api_get("/containers/" + container + "/service_name")

  def get_container_hostname(self, container = None):
    if container is None:
      return self.api_get("/self/container/hostname")
    else:
      return self.api_get("/containers/" + container + "/hostname")

  def get_container_service_id(self, container = None):
    index = None

    if container is None:
      index = self.api_get("/self/container/service_index")
    else:
      index = self.api_get("/containers/" + container + "/service_index")

    if isinstance(index, dict):
      m = re.search("(\d+)$", self.get_container_name(container))
      if m:
        index = m.group(1)
      else:
        index = None

    return index

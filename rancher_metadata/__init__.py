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

  def is_error(self, data):
    if isinstance(data, dict):
      if 'code' in data and data['code'] == 404:
        return True

    return False

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
    ret = None

    if service is None:
      ret = self.api_get("/self/service/scale")
    else:
      ret = self.api_get("/services/" + service + "/scale")

    if self.is_error(ret):
      ret = None

    return ret

  def get_service_containers(self, service = None):
    ret = None

    if service is None:
      ret = self.api_get("/self/service/containers")
    else:
      ret = self.api_get("/services/" + service + "/containers")

    if self.is_error(ret):
      ret = None

    return ret

  def get_service_metadata(self, service = None):
    ret = None

    if service is None:
      ret = self.api_get("/self/service/metadata")
    else:
      ret = self.api_get("/services/" + service + "/metadata")

    if self.is_error(ret):
      ret = None

    return ret

  def get_service_links(self, service = None):
    ret = None

    if service is None:
      ret = self.api_get("/self/service/links")
    else:
      ret = self.api_get("/services/" + service + "/links")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_id(self, container = None):
    ret = None

    if container is None:
      ret = self.api_get("/self/container/create_index")
    else:
      ret = self.api_get("/containers/" + container + "/create_index")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_ip(self, container = None):
    ret = None

    if container is None:
      # are we running within the rancher managed network?
      if is_network_managed():
        ret = self.api_get("/self/container/primary_ip")
      else:
        ret = self.get_host_ip()
    else:
      ret = self.api_get("/containers/" + container + "/primary_ip")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_name(self, container = None):
    ret = None

    if container is None:
      ret = self.api_get("/self/container/name")
    else:
      ret = self.api_get("/containers/" + container + "/name")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_service_name(self, container = None):
    ret = None

    if container is None:
      ret = self.api_get("/self/container/service_name")
    else:
      ret = self.api_get("/containers/" + container + "/service_name")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_hostname(self, container = None):
    ret = None

    if container is None:
      ret = self.api_get("/self/container/hostname")
    else:
      ret = self.api_get("/containers/" + container + "/hostname")

    if self.is_error(ret):
      ret = None

    return ret

  def get_container_service_id(self, container = None):
    ret = None

    if container is None:
      ret = self.api_get("/self/container/service_index")
    else:
      ret = self.api_get("/containers/" + container + "/service_index")

    if self.is_error(ret):
      ret = None
    else:
      if isinstance(index, dict):
        m = re.search("(\d+)$", self.get_container_name(container))
        if m:
          ret = m.group(1)
        else:
          ret = None

    return ret

  def is_network_managed():
    # in managed network, we don't get to see any information about the container :(

    if is_error(self.get_container_id()):
      return False
    else:
      return True

  def get_host_ip(self, host):
    ret = None

    if host is None:
      ret = self.api_get("/self/host/agent_ip")
    else:
      ret = self.api_get("/hosts/" + host + "/agent_ip")

    if self.is_error(ret):
      ret = None

    return ret

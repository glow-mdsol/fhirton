import datetime
import json
import logging
import uuid
from urllib.parse import urljoin, urlparse, parse_qs, urlunparse
import importlib
import redis

import os
import requests
import sys

from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.meta import Meta

logging.basicConfig()
logger = logging.getLogger(__name__)


class PseudoSubscription:
    def __init__(self,
                 name,
                 base_url,
                 endpoint,
                 reason,
                 criteria,
                 last_updated=None,
                 active=True):
        self.reason = reason
        self.name = name
        self.base_url = base_url
        self.endpoint = urlunparse(urlparse(endpoint))
        if not last_updated:
            self.last_updated = datetime.datetime.now()
        else:
            self.last_updated = last_updated
        self._criteria = criteria
        self.active = active

    def __str__(self):
        return "Subscription for resource %s with criteria %s" % (self.resource_type, self.params)

    @property
    def params(self):
        expl = urlparse(self._criteria)
        params = parse_qs(expl.query)
        for k,v in params.items():
            params[k] = v[0]
        #params.update(dict(_lastUpdated=self.last_updated.isoformat()))
        return params

    @property
    def resource_type(self):
        expl = urlparse(self._criteria)
        return expl.path

    def execute(self, server):
        fhir_module = importlib.import_module("fhirclient.models.{}".format(self.resource_type.lower()))
        resource_type = getattr(fhir_module, self.resource_type)
        search = FHIRSearch(resource_type=resource_type,
                            struct=self.params)
        results = search.perform_resources(server=server)
        sess = requests.Session()
        for result in results:
            # print("Got result: {}".format(result))
            meta = result.meta  # type: Meta
            content = dict(resource=dict(resource_type=result.resource_type,
                                         criteria=self._criteria,
                                         id=result.id,
                                         last_updated=meta.lastUpdated.isostring))
            print("Content: {}".format(content))
            p = sess.post(self.endpoint, json=json.dumps(content))
            print("Posted: {0.status}".format(p))

    def poll(self):
        l = urljoin(self.base_url, self.resource_type.capitalize())
        req = requests.get(l, params=self.params)
        steps = 0
        if req.status_code == 200:
            results = req.json()
            if results.get('total', 0) > 0:
                for entry in results.get("entry", []):
                    steps += 1
                    p = requests.post(self.endpoint,
                                      json=dict(fullUrl=entry.get('fullUrl'),
                                                resource=dict(resourceType=entry.get('resourceType'),
                                                              id=entry.get('id'),
                                                              meta=entry.get('meta'))))
                    if not p.status_code == 200:
                        logger.error("Callback failed: {}".format(p.text))
        return steps


def start(base_url, subscriptions):
    if not os.path.exists(subscriptions):
        print("No such subscriptions")
        sys.exit(1)
    l = json.load(subscriptions)
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
    for subs in l:
        crit = l.get('criteria')
        expl = urlparse(crit)
        resource_type = expl.path
        parms = parse_qs(expl.query)
        uniq = str(uuid.uuid4())
        endpoint = subs.get("channel").get("endpoint")
        g = PseudoSubscription(uniq, base_url, endpoint, resource_type, criteria=parms)

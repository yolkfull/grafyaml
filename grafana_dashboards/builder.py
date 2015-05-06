# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import requests
import yaml

from oslo_config import cfg

grafana_opts = [
    cfg.StrOpt(
        'url', default='http://grafana.example.org',
        help='URL for grafana server.'),
    cfg.StrOpt(
        'apikey', default='',
        help='API key for access grafana.'),
]

grafana_group = None
list_opts = lambda: [(grafana_group, grafana_opts), ]

CONF = cfg.CONF
CONF.register_opts(grafana_opts)


class Grafana(object):
    def __init__(self, url, key):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer %s' % key,
        })

    def create_dashboard(self, data, overwrite=False):
        data['overwrite'] = overwrite
        headers = {
            'Content-Type': 'application/json',
        }
        res = self.session.post(
            self.url, data=json.dumps(data), headers=headers)
        res.raise_for_status()


class Builder(object):
    def __init__(self):
        self.grafana = Grafana(CONF.url, CONF.apikey)

    def update_dashboard(self, path):
        data = yaml.load(open(path))
        self.grafana.create_dashboard(data, overwrite=True)
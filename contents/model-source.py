#!/usr/bin/env python3

# Copyright 2023 thecodye
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import common

def build_agent(agent, tags=None):
    data = {}
    if os.environ.get('RD_CONFIG_USE_AGENT_ID', False):
        data['nodename'] = agent['hostname'] + " - " + agent['agent_id']
    else:
        data['nodename'] = agent['hostname']
    data['tags'] = tags
    data['agentId'] = agent['agent_id']
    data['hostname'] = agent['hostname']
    data['description'] = agent['description']
    data['serialNumber'] = agent['serial_number']
    data['osArch'] = agent['goarch']
    data['osFamily'] = agent['plat']
    data['osName'] = agent['operating_system']
    data['client'] = agent['client_name']
    data['clientId'] = os.environ.get('RD_CONFIG_CLIENTID', None)
    data['site'] = agent['site_name']
    data['siteId'] = os.environ.get('RD_CONFIG_SITEID', None)
    data['model'] = agent['make_model']

    # set node-executor & file copier
    data['node-executor'] = "trmm.node-executor"
    data['file-copier'] = "trmm.file-copy"

    return data

trmm = common.TacticalRMM()

tags = os.environ.get('RD_CONFIG_TAGS')

siteid = os.environ.get('RD_CONFIG_SITEID', None)
clientid = os.environ.get('RD_CONFIG_CLIENTID', None)

agents = trmm.get_agents(site_id=siteid, client_id=clientid)

node_set = []

for i in agents:
    if i['status'] != 'online' or os.environ.get('RD_CONFIG_PLATFORM', i['plat']) != i['plat']:
        continue
    node_set.append(build_agent(i, tags))

print(json.dumps(node_set, indent=4, sort_keys=True))
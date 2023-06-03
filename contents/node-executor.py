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
import common
import sys
import re

agentid = sys.argv[1]
if agentid is None:
    raise Exception("Agent ID is required")

command = ' '.join(sys.argv[2:])
if command is None:
    raise Exception("Command is required")

trmm = common.TacticalRMM()

agent = trmm.get_agent(agentid)

if agent is None:
    raise Exception("Agent not found")

timeout = os.environ.get('RD_CONFIG_TIMEOUT', 360)

if agent['status'] != 'online':
    raise Exception("Agent is not online")

if agent['plat'] == 'windows':
    shell = os.environ.get('RD_CONFIG_WIN_SHELL', 'powershell')
    ret = trmm.send_agent_cmd(agentid, command, shell=shell, timeout=timeout)
    print(re.sub(r'\\.',lambda x:{'\\n':'\n','\\r':'\r','\\t':'\t'}.get(x[0],x[0]),ret.content.decode()[1:-1]))
    sys.exit(0)
elif agent['plat'] == 'linux':
    shell = os.environ.get('RD_CONFIG_LINUX_SHELL', '/bin/bash')
    ret = trmm.send_agent_cmd(agentid, command, shell="custom", custom_shell=shell, timeout=timeout)
    print(re.sub(r'\\.',lambda x:{'\\n':'\n','\\r':'\r','\\t':'\t'}.get(x[0],x[0]),ret.content.decode()[1:-1]))
    sys.exit(0)

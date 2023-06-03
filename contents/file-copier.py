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
import base64

agentid = sys.argv[1]
if agentid is None:
    raise Exception("Agent ID is required")

source_file = os.environ.get('RD_FILE_COPY_FILE')
destination_file = os.environ.get('RD_FILE_COPY_DESTINATION')

# force print destination
print(destination_file)

trmm = common.TacticalRMM()

agent = trmm.get_agent(agentid)

if agent is None:
    print("Agent not found", file=sys.stderr)
    sys.exit(1)

timeout = os.environ.get('RD_CONFIG_TIMEOUT', 360)

if agent['status'] != 'online':
    print("Agent is not online", file=sys.stderr)
    sys.exit(1)

with open(source_file, "rb") as f:
    encoded_file = base64.b64encode(f.read())

if agent['plat'] == 'windows':
    shell = "powershell"
    command = f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded_file.decode()}')) | Out-File -FilePath {destination_file} -Encoding UTF8"
    ret = trmm.send_agent_cmd(agentid, command, shell=shell, timeout=timeout)
    sys.exit(0)
elif agent['plat'] == 'linux':
    shell = os.environ.get('RD_CONFIG_LINUX_SHELL', '/bin/sh')
    command = f"echo {encoded_file.decode()} | base64 -d > {destination_file}"
    ret = trmm.send_agent_cmd(agentid, command, shell="custom", custom_shell=shell, timeout=timeout)
    sys.exit(0)

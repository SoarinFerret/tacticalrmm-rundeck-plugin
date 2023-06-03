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

import requests
import os

class TacticalRMM:
    def __init__(self, host: str = None, access_token: str = None):
        self.host = os.environ.get('RD_CONFIG_URL') if host is None else host
        self.access_token = os.environ.get('RD_CONFIG_ACCESS_TOKEN') if access_token is None else access_token

        if not self.access_token:
            self.access_token = os.environ.get('RD_CONFIG_TOKEN_STORAGE_PATH')

        if self.host is None or self.access_token is None:
            raise Exception("Host and Access Token must be provided")
        
        # check API access works
        if self.request("GET", "/core/version/").status_code != 200:
            raise Exception("Invalid Host or Access Token")
    
    def request(self, method: str, path: str, **kwargs):
        url = f"{self.host}{path}"
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.access_token,
        }
        return requests.request(method, url, headers=headers, **kwargs)
    
    def get_clients(self):
        return self.request("GET", "/clients/").json()
    
    def get_client(self, client_id: int):
        return self.request("GET", f"/clients/{client_id}/").json()
    
    def get_sites(self):
        return self.request("GET", "/sites/").json()
    
    def get_site(self, site_id: int):
        return self.request("GET", f"/sites/{site_id}/").json()
    
    def get_agents(self, client_id: int = None, site_id: int = None, monitoring_type: str = "server"):
        if client_id is not None:
            return self.request("GET", f"/agents/?monitoring_type={monitoring_type}&client={client_id}").json()
        elif site_id is not None:
            return self.request("GET", f"/agents/?monitoring_type={monitoring_type}&site={site_id}").json()
        # can't use monitoring_type if client_id or site_id is None
        return self.request("GET", "/agents/").json()
    
    def get_agent(self, agent_id: str):
        return self.request("GET", f"/agents/{agent_id}/").json()
    
    def send_agent_cmd(self, agent_id: str, cmd: str, shell: str = "cmd", custom_shell: str = None, timeout: int = 30, run_as_user: bool = False):
        return self.request("POST", f"/agents/{agent_id}/cmd/", json={"cmd": cmd, "shell": shell, "custom_shell": custom_shell, "timeout": timeout, "run_as_user": run_as_user})
    
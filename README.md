# Tactical RMM Plugin for Rundeck

This plugin integrates Tactical RMM with Rundeck. Right now, its more of a Proof of Concept that anything - I threw it together one night and ended up being surprisingly more functional than I expected. Is is probably not considered production ready though - use at your own risk.

## KNOWN ISSUES

* Every script / command returns successfully even if it actually failed because no exit codes are returned from the node-executor. This is a limitation of the existing Tactical RMM API and rmmagent functionality when using the `/agents/xxx/cmd/` endpoint. After speaking with the development team on the discord, this may be fixed in the future with a potential new API endpoint.
* `stdout` and `stderr` are both returned as `stdout` in the Rundeck job output. Currently, Tactical RMM does not separate out these two streams from the remote server. Maybe this will be fixed in the above mentioned new endpoint.
* The plugin does not currently support the "Run As" functionality of Rundeck or TacticalRMM. Everything is ran as "system" on windows, or "root" on linux. This is due to how Tactical RMM handles sending commands to the agent. I have no intention of fixing this.
* You can only connect to 1 Tactical RMM server at a time per project. This is due to the way the plugin's node-executor and file-copier function. If you need to connect to multiple Tactical RMM servers, you will need to use multiple projects.

## Installation

### Pre-requisites

In order to properly work, this plugin requires the following on the Rundeck server:
* Python3
* Python3 Requests

To install on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-requests -y
```

Additionally, you will need the following from the Tactical RMM server:
* API Url - ex: https://rmmm-api.example.com (no trailing slash)
* API Key - This can be found in the TacticalRMM web interface under Settings -> Global Settings -> API Keys

### Plugin Installation

- Download the latest release from the [releases page](https://github.com/soarinferret/tacticalrmm-rundeck-plugin/releases)
- Go to Settings -> Plugins -> Upload Plugin to install

### Plugin Configuration

The easiest way to configure this plugin is to use the Rundeck GUI. Go to Project Settings -> Edit Configuration -> Default Node Executor and Default File Copier and fill in the fields. After saving the configuration, you can change the node configuration back to the previous settings - the plugin will still work. It stores the following variables in the project configuration (or you can add them manually by editing the project.properties file):

```
project.plugin.FileCopier.trmm.file-copy.linux_shell=/bin/bash
project.plugin.FileCopier.trmm.file-copy.timeout=360
project.plugin.FileCopier.trmm.file-copy.token_storage_path=keys/trmm_access token
project.plugin.FileCopier.trmm.file-copy.url=https\://rmm-api.example.com
project.plugin.FileCopier.trmm.file-copy.win_shell=powershell
project.plugin.NodeExecutor.trmm.node-executor.linux_shell=/bin/bash
project.plugin.NodeExecutor.trmm.node-executor.timeout=360
project.plugin.NodeExecutor.trmm.node-executor.token_storage_path=keys/trmm_access token
project.plugin.NodeExecutor.trmm.node-executor.url=https\://rmm-api.example.com
project.plugin.NodeExecutor.trmm.node-executor.win_shell=powershell
```

#### Resource Model Source / Adding Nodes

Go to Project Settings -> Edit Nodes and add the "TacticalRMM / Resource Model" - edit options as necessary.

## Usage

When selecting a Node imported from the TacticalRMM Resource Model, it will automatically use the `trmm.node-executor` and `trmm.file-copy` for running commands and scripts - no action required by you. It should act as a drop in replacement.

## Development / Testing

This plugin was developed and tested with Rundeck 4.13.0 and Tactical RMM 0.15.12. It may work with other versions, but I have not tested it.

To develop the plugin, you can do the following:
```bash
# Clone the repo
git clone https://github.com/SoarinFerret/tacticalrmm-rundeck-plugin.git

cd tacticalrmm-rundeck-plugin/testing

# Start the dev environment
docker-compose up -d

# Install dependencies in dev environment
docker-compose exec rundeck sudo apt update
docker-compose exec rundeck sudo apt install python3 python3-requests -y

# Build / Install the plugin
./build.sh test

# visit http://localhost:4440 to access the Rundeck web interface with login admin/admin
```

## Notice

"Tactical RMM" is a registered trademark of [AmidaWare LLC](https://docs.tacticalrmm.com/license/). This project is not affiliated, endorsed, or developed with Tactical RMM or AmidaWare LLC in any way. This project is developed by a third party and is not supported by Tactical RMM or AmidaWare LLC.

A special thanks to the team behind Tactical RMM for their hard work and dedication to the project. Without them, this plugin would not be possible.
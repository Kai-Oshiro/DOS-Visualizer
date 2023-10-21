#!/usr/bin/env python
import os
import subprocess
from my_module import argument, config

# Get arguments
args = argument.get_args()
#print(f"args: {args}\n")

# Get path to a config file
conf_file = args["f"]

print(f"\n###Config file process###")
print(f"{conf_file} is referenced as a configuration file.\n")

# Set config file to "configparser"
conf_proc = config.ConfigProcessor(conf_file)

# Get params from the config file
all_conf_list = conf_proc.read_config()

for conf in all_conf_list:
    print(conf)




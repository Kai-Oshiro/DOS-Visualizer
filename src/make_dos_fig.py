#!/usr/bin/env python
import subprocess
from my_module import argument, config

# Get arguments
args = argument.get_args()
#print(f"args: {args}\n")

# Get path to a config file
conf_file = args["f"]

# Get params from the config file
conf_proc = config.ConfigProcessor(conf_file)

dir_list = conf_proc.read_job_dir()

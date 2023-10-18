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

# Get params from the config file
conf_proc = config.ConfigProcessor(conf_file)

# Get directory list
dir_dict = conf_proc.read_job_dir()
dir_list = list(dir_dict.values())

# Get atom idx
# idx_dict = {'group1': [string of atom indexes in grop1], ...}
# examples of atom index string are '1', '1 2 3' or '1-3'.
idx_dict = conf_proc.read_atom_idx()
#print(f"idx_dict:\n{idx_dict}\n")

# idx_grop_list = [[atom indexes in group 1], [that in group 2], ...]
idx_group_list = []
# examples of "idx_str" are '1', '1 2', '1-3' or '1 2 3-5'.
for idx_str in idx_dict.values():
    # example of "idx_list" is ['1', '2', '3-5']
    idx_list = idx_str.split()
    #print(f"idx_list:\n{idx_list}")

    # [atom indexes in each grop]
    new_idx_list = []
    # Get list of index for each atom group.
    for idx in idx_list:
        if "-" in idx:
            # Split numbers joined by "-" and convert it from str to int.
            start, end = map(int, idx.split("-"))
            temp_list = list(range(start, end+1))
            new_idx_list.extend(temp_list)
        else:
            new_idx_list.append(int(idx))
        idx_group_list.append(new_idx_list)
    #print(f"new_idx_list:\n{new_idx_list}\n")
print(f"idx_group_list:\n{idx_group_list}\n")

# Get current working directory
cwd = os.getcwd()
for job_dir in dir_list:
    # Move to job directory
    os.chdir(job_dir)

    with open(f"./dos_dat/PDOS_A{idx}_UP.dat", "r") as f:
        contents = f.readlines()
    os.chdir(cwd)

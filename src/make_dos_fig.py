#!/usr/bin/env python
import os
import sys
import pandas as pd
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

for conf_dict in all_conf_list:
    #print(conf_dict[])
    for k, v in conf_dict.items():
        print(f"{k}: {v}")
    print()

    job_path = conf_dict["job"]
    cwd = os.getcwd()

    for atoms_group in conf_dict["atoms"]:
        # Move to job directory
        os.chdir(job_path)

        for atom in atoms_group:
            #print(atom)

            file_path = f"./dos_dat/PDOS_A{atom}_UP.dat"
            df_up = pd.read_csv(file_path, sep="\s+")

            file_path = f"./dos_dat/PDOS_A{atom}_DW.dat"
            df_dw = pd.read_csv(file_path, sep="\s+")
            df_dw = df_dw.sort_values(by="#Energy", ascending=False)

            df_both = pd.concat([df_up, df_dw], axis=0)
            df_both = df_both.reset_index(drop=True)
            #print(df_both)

        #print()
        os.chdir(cwd)





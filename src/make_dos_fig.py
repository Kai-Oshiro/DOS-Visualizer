#!/usr/bin/env python
import os
import pandas as pd
from my_module import argument, config, file

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
    #print(conf_dict)
    for k, v in conf_dict.items():
        print(f"{k}: {v}")
    print()


    cwd = os.getcwd()
    job_path = conf_dict["job"]
    os.chdir(job_path) # Move to job directory

    pdos_list = []
    for atoms_group, orbitals_group in zip(conf_dict["atoms"], conf_dict["orbitals"]):


        first_itr = True
        for atoms in atoms_group:
            #print(atom)
            if first_itr:
                read_file = file.ReadFile(atoms=atoms_group[0], orbitals_group=orbitals_group)
                len_data = read_file.get_len()
                s_pdos = pd.Series([0] * len_data) # Define a "pd.Series" with 0 for each value
                first_itr = False

            read_file = file.ReadFile(atoms=atoms, orbitals_group=orbitals_group)
            df_sum = read_file.get_df()
            s_pdos += df_sum

        pdos_list.append(s_pdos)

    #figure.MakeFig(pdos_)

    print(len(pdos_list))

    #print()
    os.chdir(cwd)





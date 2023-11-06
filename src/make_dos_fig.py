#!/usr/bin/env python
import os
import glob
import pandas as pd
from my_module import argument, config, file, figure

# Get arguments
# arg_dict = # {f: '/path/to/conf/file'}
arg_dict = argument.get_args()

# Get path to a config file
conf_file = arg_dict["f"]

print(f"\n###Config file process###")
print(f"{conf_file} is referenced as a configuration file.\n")

print("Following parameters were used to create figures.\n")

# Set config file to "configparser"
conf_proc = config.ConfigProcessor(conf_file)

# Get params from the config file
all_conf_list = conf_proc.read_config()

for conf_dict in all_conf_list:
    #print(conf_dict)
    for k, v in conf_dict.items():
        print(f"{k}: {v}")
    print()

print(f"###Figure preparation process###")
print("Following files were generated.")
for conf_dict in all_conf_list:

    cwd = os.getcwd()
    job_path = conf_dict["job"]
    os.chdir(job_path) # Move to job directory

    dos_list = []
    for atoms_group, orbitals_group in zip(conf_dict["atoms"], conf_dict["orbitals"]):


        first_itr = True
        for atoms in atoms_group:
            read_file = file.ReadFile(atoms=atoms, orbitals_group=orbitals_group)

            if first_itr:
                s_atom_ene = read_file.get_ene()
                atom_ene = s_atom_ene.values
                len_data = read_file.get_len()
                s_group_dos = pd.Series([0] * len_data) # Define a "pd.Series" with 0 for each value
                first_itr = False

            s_atom_dos = read_file.get_dos()
            s_group_dos += s_atom_dos

        dos_list.append(s_group_dos.values)

    make_fig = figure.MakeFig(dos_list=dos_list, atom_ene=atom_ene, conf_dict=conf_dict)
    fname = make_fig.plot_pdos()

    file_path = glob.glob(f"{job_path}/{fname}*")[0]
    print(f"{file_path}")

    os.chdir(cwd)
print()




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
        #print(f"{k}: {v}, {type(v)}")
        print(f"{k}: {v}")
    print()

print(f"###Figure preparation process###")
print("Following files were generated.")
# all_conf_list = [conf_dict of section 1, ... conf_dict of section N]
# conf_dict = {'pram 1': value, ... 'pram N': value }
# conf_dict = {'atoms': [[1, 2, 3], ... [4, 5]], ... 'orbitals': [[px, py, pz], ... [tot]]}
for conf_dict in all_conf_list:

    cwd = os.getcwd()
    job_path = conf_dict["job"]
    os.chdir(job_path) # Move to job directory

    dos_list = []
    # atoms_group = [1, 2, 3] (list of atom indices)
    # orbitals_group = [px, py, pz] (list of orbitals)
    for atoms_group, orbitals_group in zip(conf_dict["atoms"], conf_dict["orbitals"]):

        first_itr = True
        # atoms = 1 (atom index)
        for atoms in atoms_group:
            read_file = file.ReadFile(atoms=atoms, orbitals_group=orbitals_group)

            if first_itr:
                # s_atom_ene is a pandas Series
                # 0      -38.80734
                #           ...
                # 2399   -38.80734
                # Name: #Energy, Length: 2400, dtype: float64
                s_atom_ene = read_file.get_ene()
                atom_ene = s_atom_ene.values # Convert pd.Series to np.ndarray
                len_data = read_file.get_len()
                s_group_dos = pd.Series([0] * len_data) # Define a "pd.Series" with 0 for each value
                first_itr = False

            # s_atom_dos and s_group_dos are pandas Series
            # 0       0.0
            #        ...
            # 2399    0.0
            # Length: 2400, dtype: float64
            s_atom_dos = read_file.get_dos()
            s_group_dos += s_atom_dos

        # Convert pd.Series to np.ndarray
        # Append np.ndarray to list
        dos_list.append(s_group_dos.values)

    make_fig = figure.MakeFig(dos_list=dos_list, atom_ene=atom_ene, conf_dict=conf_dict)
    fname = make_fig.plot_pdos()

    full_job_path = os.getcwd()
    file_path = glob.glob(f"{full_job_path}/{fname}*")[0]
    print(f"{file_path}")

    os.chdir(cwd)
print()




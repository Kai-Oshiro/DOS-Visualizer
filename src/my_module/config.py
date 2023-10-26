import re
import sys
import configparser

class ConfigProcessor:
    def __init__(self, conf_file=None):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.optionxform = str
        self.config_ini.read(conf_file)

    def check_param(self, key=None, conf_dict=None):
        if conf_dict[key] == None:
            print(f"Each section should have \"{conf_dict[key]}\" parameter.\n")
            sys.exit()

    def compare_key_len(self, key1="atoms", key2=None, conf_dict=None):
        if conf_dict[key2] != None:
            if len(conf_dict[key1].split(",")) != len(conf_dict[key2].split(",")):
                section_name = conf_dict["section"]
                print(f"Length of \"{key1}\" and \"{key2}\" in [\"{section_name}\"]  dosen't match.\n")
                sys.exit()

    # Read "JOB_DIR" section
    def read_config(self):
        section_list = self.config_ini.sections()

        all_conf_list = []
        for section in section_list:
            configs = self.config_ini[section]
            conf_dict = dict(configs)
            conf_dict["section"] = section

            # List of items that can be set in .ini
            keys_to_check = ["job", "name", "atoms", "orbitals", "colors", "lines"]

            # If key does not exist in .ini, set "None".
            for key in keys_to_check:
                if key not in conf_dict:
                    conf_dict[key] = None

            # Check params
            self.check_param(key="atoms", conf_dict=conf_dict)
            self.check_param(key="orbitals", conf_dict=conf_dict)

            self.compare_key_len(key2="orbitals", conf_dict=conf_dict)
            self.compare_key_len(key2="colors", conf_dict=conf_dict)
            self.compare_key_len(key2="lines", conf_dict=conf_dict)

            # Update "atoms" parameter
            # conf_dict["atoms"] = "1 2 3, 1-3, ... 1 2 3-5"
            # atoms_group_list = [[1, 2, 3], [1, 2, 3], ... [1, 2, 3, 4, 5]]
            atoms_group_list = []
            for atoms_group in conf_dict["atoms"].split(","):
                atoms_list = []
                for atoms in atoms_group.split():
                    if "-" in atoms: # Split numbers joined by "-" and convert it from str to int
                        start, end = map(int, atoms.split("-"))
                        atoms_list.extend(list(range(start, end+1)))
                    else:
                        atoms_list.append(int(atoms))

                atoms_group_list.append(atoms_list)
            conf_dict["atoms"] = atoms_group_list

            # Update "orbitals" parameter
            # conf_dict["orbitals"] = "s, px py pz, ... tot"
            # orbitals_group_list = [[s], [px, py, pz], ... [tot]]
            orbitals_group_list = []
            for orbitals_group in conf_dict["orbitals"].split(","):
                orbitals_list = []
                for orbitals in orbitals_group.split():
                    orbitals_list.append(orbitals)

                orbitals_group_list.append(orbitals_list)
            conf_dict["orbitals"] = orbitals_group_list

            # Update "colors" parameter
            # conf_dict["colors"] = "darkgray, red, darkorange, limegreen"
            # conf_dict["colors"] = ['darkgray', 'red', 'darkorange', 'limegreen']
            if conf_dict["colors"] != None:
                colors_list = conf_dict["colors"].split(",")
                colors_list = [c.replace(" ", "") for c in colors_list]
                conf_dict["colors"] = colors_list

            # Update "lines" parameter
            # conf_dict["lines"] = "solid, dashed, dashdot, dotted"
            # conf_dict["lines"] = ['solid', 'dashed', 'dashdot', 'dotted']
            if conf_dict["lines"] != None:
                lines_list = conf_dict["lines"].split(",")
                lines_list = [l.replace(" ", "") for l in lines_list]
                conf_dict["lines"] = lines_list

            all_conf_list.append(conf_dict)

        return all_conf_list

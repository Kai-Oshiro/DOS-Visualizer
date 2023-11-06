import re
import sys
import configparser
from distutils.util import strtobool

class ConfigProcessor:
    def __init__(self, conf_file=None):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.optionxform = str
        self.config_ini.read(conf_file)

    def check_param(self, key=None):
        if self.conf_dict[key] == None:
            print(f"Each section should have \"{self.conf_dict[key]}\" parameter.\n")
            sys.exit()

    def compare_key_len(self, key1="atoms", key2=None):
        if self.conf_dict[key2] != None:
            if len(self.conf_dict[key1].split(",")) != len(self.conf_dict[key2].split(",")):
                section_name = self.conf_dict["section"]
                print(f"Length of \"{key1}\" and \"{key2}\" in [\"{section_name}\"]  dosen't match.\n")
                sys.exit()

    def check_len(self, key=None, nlen=None):
        if len(self.conf_dict[key].split(",")) != nlen:
            print(f"Length of \"{key}\" isn't {nlen}.")

    def str_to_list(self, key=None):
        if self.conf_dict[key] != None:
            _list = self.conf_dict[key].split(",")
            _list = [v.replace(" ", "") for v in _list]
            self.conf_dict[key] = _list

    # Read "JOB_DIR" section
    def read_config(self):
        section_list = self.config_ini.sections()

        all_conf_list = []
        for section in section_list:
            configs = self.config_ini[section]
            self.conf_dict = dict(configs)
            self.conf_dict["section"] = section

            # List of items that can be set in .ini
            keys_list = ["section", "job", "atoms", "orbitals",
                        "labels", "colors", "lines", "figname",
                        "fontsize", "dpi", "x_lim", "y_lim", "grid"]

            # If key does not exist in .ini, set "None".
            for key in keys_list:
                if key not in self.conf_dict:
                    self.conf_dict[key] = None

            # Check params
            self.check_param(key="atoms")
            self.check_param(key="orbitals")

            self.compare_key_len(key2="labels")
            self.compare_key_len(key2="orbitals")
            self.compare_key_len(key2="colors")
            self.compare_key_len(key2="lines")

            if self.conf_dict["x_lim"] != None:
                self.check_len(key="x_lim", nlen=2)
            if self.conf_dict["y_lim"] != None:
                self.check_len(key="y_lim", nlen=2)

            # Update "atoms" parameter
            # self.conf_dict["atoms"] = "1 2 3, 1-3, ... 1 2 3-5"
            # self.conf_dict["atoms"] = [[1, 2, 3], [1, 2, 3], ... [1, 2, 3, 4, 5]] (= atoms_group_list)
            atoms_group_list = []
            for atoms_group in self.conf_dict["atoms"].split(","):
                atoms_list = []
                for atoms in atoms_group.split():
                    if "-" in atoms: # Split numbers joined by "-" and convert it from str to int
                        start, end = map(int, atoms.split("-"))
                        atoms_list.extend(list(range(start, end+1)))
                    else:
                        atoms_list.append(int(atoms))

                atoms_group_list.append(atoms_list)
            self.conf_dict["atoms"] = atoms_group_list

            # Update "orbitals" parameter
            # self.conf_dict["orbitals"] = "s, px py pz, ... tot"
            # self.conf_dict["orbitals"] = [[s], [px, py, pz], ... [tot]] (= orbitals_group_list)
            orbitals_group_list = []
            for orbitals_group in self.conf_dict["orbitals"].split(","):
                orbitals_list = []
                for orbitals in orbitals_group.split():
                    orbitals_list.append(orbitals)

                orbitals_group_list.append(orbitals_list)
            self.conf_dict["orbitals"] = orbitals_group_list

            # Update "labels" parameter
            # self.conf_dict["labels"] = "Ce, O, Fe, H2SO4"
            # self.conf_dict["labels"] = ['Ce', 'O', 'Fe', 'H2SO4']
            self.str_to_list(key="labels")

            # Update "colors" parameter
            # self.conf_dict["colors"] = "darkgray, red, darkorange, limegreen"
            # self.conf_dict["colors"] = ['darkgray', 'red', 'darkorange', 'limegreen']
            self.str_to_list(key="colors")

            # Update "lines" parameter
            # self.conf_dict["lines"] = "solid, dashed, dashdot, dotted"
            # self.conf_dict["lines"] = ['solid', 'dashed', 'dashdot', 'dotted']
            self.str_to_list(key="lines")

            # Update "x_lim" parameter
            # self.conf_dict["x_lim"] = "lower limit, upper limit"
            # self.conf_dict["x_lim"] = ['lower limit', 'upper limit']
            self.str_to_list(key="x_lim")
            if self.conf_dict["x_lim"] != None: # Convert str to int.
                self.conf_dict["x_lim"] = [float(v) for v in self.conf_dict["x_lim"]]

            # Update "y_lim" parameter
            # self.conf_dict["y_lim"] = "lower limit, upper limit"
            # self.conf_dict["y_lim"] = ['lower limit', 'upper limit']
            self.str_to_list(key="y_lim")
            if self.conf_dict["y_lim"] != None: # Convert str to int.
                self.conf_dict["y_lim"] = [float(v) for v in self.conf_dict["y_lim"]]

            # Convert str to bool
            if self.conf_dict["grid"] != None:
                self.conf_dict["grid"] = strtobool(self.conf_dict["grid"]) # Convert str to int
                self.conf_dict["grid"] = bool(self.conf_dict["grid"]) # Convert int to bool

            # Sort self.conf_dict according to the order of keys_list
            sorted_conf_dict = {key: self.conf_dict[key] for key in keys_list}
            all_conf_list.append(sorted_conf_dict)

        return all_conf_list

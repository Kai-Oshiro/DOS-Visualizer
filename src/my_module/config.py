import re
import sys
import configparser
from distutils.util import strtobool

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

    def check_len(self, key=None, conf_dict=None, nlen=None):
        if len(conf_dict[key].split(",")) != nlen:
            print(f"Length of \"{key}\" isn't {nlen}.")

    def str_to_list(self, conf_dict=None, key=None):
        if conf_dict[key] != None:
            _list = conf_dict[key].split(",")
            _list = [v.replace(" ", "") for v in _list]
            conf_dict[key] = _list

    # Read "JOB_DIR" section
    def read_config(self):
        section_list = self.config_ini.sections()

        all_conf_list = []
        for section in section_list:
            configs = self.config_ini[section]
            conf_dict = dict(configs)
            conf_dict["section"] = section

            # List of items that can be set in .ini
            keys_list = ["section", "job", "atoms", "orbitals",
                        "labels", "colors", "lines", "figname",
                        "fontsize", "dpi", "x_lim", "y_lim", "grid"]

            # If key does not exist in .ini, set "None".
            for key in keys_list:
                if key not in conf_dict:
                    conf_dict[key] = None

            # Check params
            self.check_param(key="atoms", conf_dict=conf_dict)
            self.check_param(key="orbitals", conf_dict=conf_dict)

            self.compare_key_len(key2="labels", conf_dict=conf_dict)
            self.compare_key_len(key2="orbitals", conf_dict=conf_dict)
            self.compare_key_len(key2="colors", conf_dict=conf_dict)
            self.compare_key_len(key2="lines", conf_dict=conf_dict)

            if conf_dict["x_lim"] != None:
                self.check_len(key="x_lim", conf_dict=conf_dict, nlen=2)
            if conf_dict["y_lim"] != None:
                self.check_len(key="y_lim", conf_dict=conf_dict, nlen=2)

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

            # Update "labels" parameter
            # conf_dict["labels"] = "Ce, O, Fe, H2SO4"
            # conf_dict["labels"] = ['Ce', 'O', 'Fe', 'H2SO4']
            self.str_to_list(conf_dict=conf_dict, key="labels")

            # Update "colors" parameter
            # conf_dict["colors"] = "darkgray, red, darkorange, limegreen"
            # conf_dict["colors"] = ['darkgray', 'red', 'darkorange', 'limegreen']
            self.str_to_list(conf_dict=conf_dict, key="colors")

            # Update "lines" parameter
            # conf_dict["lines"] = "solid, dashed, dashdot, dotted"
            # conf_dict["lines"] = ['solid', 'dashed', 'dashdot', 'dotted']
            self.str_to_list(conf_dict=conf_dict, key="lines")

            # Update "x_lim" parameter
            # conf_dict["x_lim"] = "lower limit, upper limit"
            # conf_dict["x_lim"] = ['lower limit', 'upper limit']
            self.str_to_list(conf_dict=conf_dict, key="x_lim")
            if conf_dict["x_lim"] != None: # Convert str to int.
                conf_dict["x_lim"] = [float(v) for v in conf_dict["x_lim"]]

            # Update "y_lim" parameter
            # conf_dict["y_lim"] = "lower limit, upper limit"
            # conf_dict["y_lim"] = ['lower limit', 'upper limit']
            self.str_to_list(conf_dict=conf_dict, key="y_lim")
            if conf_dict["y_lim"] != None: # Convert str to int.
                conf_dict["y_lim"] = [float(v) for v in conf_dict["y_lim"]]

            # Convert str to bool
            if conf_dict["grid"] != None:
                conf_dict["grid"] = strtobool(conf_dict["grid"]) # Convert str to int.
                conf_dict["grid"] = bool(conf_dict["grid"]) # Convert int to bool.

            sorted_conf_dict = {key: conf_dict[key] for key in keys_list}
            all_conf_list.append(sorted_conf_dict)

        return all_conf_list

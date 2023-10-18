import configparser

class ConfigProcessor:
    def __init__(self, conf_file=None):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.optionxform = str
        self.config_ini.read(conf_file)

    # Read "JOB_DIR" section
    def read_job_dir(self):
        try:
            job_dir = self.config_ini["JOB_DIR"]
            dir_dict = dict(job_dir)
        except:
            print(f"\"JOB_DIR\" section does not exist.\n")
        return dir_dict

    # Read "ATOM_IDX" section
    def read_atom_idx(self):
        try:
            atom_idx = self.config_ini["ATOM_IDX"]
            idx_dict = dict(atom_idx)
        except:
            print(f"\"ATOM_IDX\" section does not exist.\n")
        return idx_dict

#    def read_params(self):
#        atom_idx = self.config_ini["PARAMS"]["atom_idx"]
#        return atom_idx


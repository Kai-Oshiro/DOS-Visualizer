import configparser

class ConfigProcessor: # Define class
    def __init__(self, conf_file=None): # Define constructor
        print(f"###Config file process###")
        print(f"{conf_file} is referenced as a configuration file.\n")
        self.config_ini = configparser.ConfigParser()
        self.config_ini.optionxform = str
        self.config_ini.read(conf_file)

    def read_job_dir(self):
        # Read "JOB_DIR" section
        try:
            dir_list = self.config_ini["JOB_DIR"]
        except:
            print(f"\"JOB_DIR\" section does not exist.")
        return dir_list





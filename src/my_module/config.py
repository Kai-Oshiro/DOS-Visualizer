import configparser

class ConfigProcessor:
    def __init__(self, conf_file=None):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.optionxform = str
        self.config_ini.read(conf_file)

    # Read "JOB_DIR" section
    def read_config(self):
        section_list = self.config_ini.sections()

        all_conf_list = []
        for section in section_list:
            configs = self.config_ini[section]
            conf_dict = dict(configs)
            all_conf_list.append(conf_dict)

        return all_conf_list

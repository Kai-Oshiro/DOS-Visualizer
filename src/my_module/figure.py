import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MakeFig:
    def __init__(self, dos_list=None, atom_ene=None, conf_dict=None):
        self.dos_list = dos_list
        self.atom_ene = atom_ene
        self.conf_dict = conf_dict

    def plot_pdos(self):
        # self.conf_dict["dpi"]: str or None
        if self.conf_dict["dpi"] != None:
            dpi = float(self.conf_dict["dpi"])
        else:
            dpi = None
        plt.figure(dpi=dpi)

        for idx, group_dos in enumerate(self.dos_list):
            # self.conf_dict["labels"]: list or None
            if self.conf_dict["labels"] == None:
                label = f"grop_{idx+1}"
            else:
                label = self.conf_dict["labels"][idx]

            # self.conf_dict["colors"]: list or None
            if self.conf_dict["colors"] == None:
                color = None
            else:
                color = self.conf_dict["colors"][idx]

            # self.conf_dict["lines"]: list or None
            if self.conf_dict["lines"] == None:
                linestyle = None
            else:
                linestyle = self.conf_dict["lines"][idx]

            plt.plot(self.atom_ene, group_dos, label=label, color=color, linestyle=linestyle)

        # self.conf_dict["fontsize"]: str or None
        if self.conf_dict["fontsize"] == None:
            fontsize = None
        else:
            fontsize = self.conf_dict["fontsize"]
            fontsize = float(fontsize)

        plt.xlabel(r"$\it{E} - \it{E}_{\rm{f}}$ / eV", fontsize=fontsize)
        plt.ylabel("PDOS", fontsize=fontsize)
        plt.tick_params(labelsize=fontsize)
        plt.legend(fontsize=fontsize)

        # self.conf_dict["x_lim"]: list or None
        if self.conf_dict["x_lim"] != None:
            plt.xlim(self.conf_dict["x_lim"][0], self.conf_dict["x_lim"][1])
        # self.conf_dict["y_lim"]: list or None
        if self.conf_dict["y_lim"] != None:
            plt.ylim(self.conf_dict["y_lim"][0], self.conf_dict["y_lim"][1])
        # self.conf_dict["grid"]: bool or None
        if self.conf_dict["grid"]:
            plt.grid()

        d_today = str(datetime.date.today())
        d_today = d_today.replace("-","")

        # self.conf_dict["figname"]: str or None
        if self.conf_dict["figname"] == None:
            section_name = self.conf_dict["section"] # self.conf_dict["section"]: str
            fname = f"{d_today}_{section_name}"
        else:
            fname = self.conf_dict["figname"]

        plt.savefig(fname, dpi=dpi)

        return fname
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MakeFig:
    def __init__(self, dos_list=None, atom_ene=None, conf_dict=None):
        self.dos_list = dos_list
        self.atom_ene = atom_ene
        self.section = conf_dict["section"]
        self.labels_list = conf_dict["labels"]
        self.colors_list = conf_dict["colors"]
        self.lines_list = conf_dict["lines"]
        self.figname = conf_dict["figname"]
        self.fontsize = conf_dict["fontsize"]
        self.dpi = conf_dict["dpi"]
        self.x_lim = conf_dict["x_lim"]
        self.y_lim = conf_dict["y_lim"]
        self.grid = conf_dict["grid"]

    def plot_pdos(self):
        if self.dpi != None: dpi = float(self.dpi)
        else: dpi = None
        plt.figure(dpi=dpi)

        for idx, group_dos in enumerate(self.dos_list):
            if self.labels_list == None: label = f"grop_{idx+1}"
            else: label = self.labels_list[idx]

            if self.colors_list == None: color = None
            else: color = self.colors_list[idx]

            if self.lines_list == None: linestyle = None
            else: linestyle = self.lines_list[idx]

            plt.plot(self.atom_ene, group_dos, label=label, color=color, linestyle=linestyle)

        if self.fontsize == None: fontsize = None
        else: fontsize = self.fontsize

        plt.xlabel(r"$\it{E} - \it{E}_{\rm{f}}$ / eV", fontsize=fontsize)
        plt.ylabel("PDOS", fontsize=fontsize)
        plt.tick_params(labelsize=fontsize)
        plt.legend(fontsize=fontsize)

        if self.x_lim != None:
            plt.xlim(self.x_lim[0], self.x_lim[1])
        if self.y_lim != None:
            plt.ylim(self.y_lim[0], self.y_lim[1])
        if self.grid:
            plt.grid()

        d_today = str(datetime.date.today())
        d_today = d_today.replace("-","")

        if self.figname == None:
            fname = f"{d_today}_{self.section}"
        else:
            fname = self.figname

        plt.savefig(fname, dpi=dpi)

        return fname
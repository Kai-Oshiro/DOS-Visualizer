import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MakeFig:
    def __init__(self, dos_list=None, atom_ene=None, conf_dict=None):
        self.dos_list = dos_list
        self.atom_ene = atom_ene
        self.colors_list = conf_dict["colors"]
        self.lines_list = conf_dict["lines"]
        self.section = conf_dict["section"]
        self.figname = conf_dict["figname"]

    def plot_pdos(self):
        dpi=300
        plt.figure(dpi=dpi)

        for idx, group_dos in enumerate(self.dos_list):
            if self.colors_list == None:
                color = None
            else:
                color = self.colors_list[idx]

            if self.lines_list == None:
                linestyle = None
            else:
                linestyle = self.lines_list[idx]

            plt.plot(self.atom_ene, group_dos, label=f"grop_{idx+1}", color=color, linestyle=linestyle)

        plt.xlabel(r"$\it{E} - \it{E}_{\rm{f}}$ / eV", fontsize=12)
        plt.ylabel("PDOS", fontsize=12)
        plt.tick_params(labelsize=12)
        #plt.xlim(-4, 4)
        #plt.ylim(-0, 5)
        plt.legend(fontsize=12)
        plt.grid()

        d_today = str(datetime.date.today())
        d_today = d_today.replace("-","")

        if self.figname == None:
            fname = f"{d_today}_{self.section}"
        else:
            fname = self.figname
        plt.savefig(fname, dpi=dpi)

        return fname
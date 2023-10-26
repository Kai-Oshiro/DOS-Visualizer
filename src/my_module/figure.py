import matplotlib.pyplot as plt

class MakeFig:
    def __init__(self, pdos_list=None, conf_dict=None):
        self.pdos_list = pdos_list
        self.colors_list = conf_dict["colors"]
        self.lines_list = conf_dict["lines"]
        self.name = conf_dict["name"]

    def plot_pdos(self):
        dpi=300
        plt.figure(dpi=dpi)

        for idx, s_pdos in enumerate(self.pdos_list):
            if self.colors_list == None:
                color = None
            else:
                color = self.colors_list[idx]

            if self.lines_list == None:
                linestyle = None
            else:
                linestyle = self.lines_list[idx]

            plt.plot(s_pdos, label=f"grop_{idx+1}", color=color, linestyle=linestyle)

        plt.xlabel("PDOS", fontsize=12)
        plt.ylabel(r"$E - E_{f} / eV$", fontsize=12)
        plt.tick_params(labelsize=12)
        #plt.xlim(-4, 4)
        #plt.ylim(-0, 5)
        plt.legend(fontsize=12)
        plt.grid() # グリッド線

        if self.name == None:
            name = "Test"
        plt.savefig("Test", dpi=dpi)
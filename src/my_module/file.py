import pandas as pd

class ReadFile:
    def __init__(self, atoms=None, orbitals_group=None):
        self.atoms = atoms
        self.orbitals_group = orbitals_group

    def get_df(self):
        file_path = f"./dos_dat/PDOS_A{self.atoms}_UP.dat"
        df_up = pd.read_csv(file_path, sep="\s+")

        file_path = f"./dos_dat/PDOS_A{self.atoms}_DW.dat"
        df_dw = pd.read_csv(file_path, sep="\s+")
        df_dw = df_dw.sort_values(by="#Energy", ascending=False)

        df_both = pd.concat([df_up, df_dw], axis=0)
        df_both = df_both.reset_index(drop=True)

        df_sum = df_both[self.orbitals_group].sum(axis=1)
        #name = "_".join(self.orbitals_group)
        #df_sum.name = name

        #print(df_both)
        #print(df_sum.name)
        #print(df_sum)

        return df_sum

    def get_len(self):
        df_sum = self.get_df()
        return len(df_sum)
import pandas as pd

class ReadFile:
    def __init__(self, atoms=None, orbitals_group=None):
        self.atoms = atoms
        self.orbitals_group = orbitals_group

    def get_ene(self):
        file_path = f"./dos_dat/PDOS_A{self.atoms}_UP.dat"
        df_up = pd.read_csv(file_path, sep="\s+")

        file_path = f"./dos_dat/PDOS_A{self.atoms}_DW.dat"
        df_dw = pd.read_csv(file_path, sep="\s+")
        df_dw = df_dw.sort_values(by="#Energy", ascending=False)

        df_both = pd.concat([df_up, df_dw], axis=0)
        df_both = df_both.reset_index(drop=True)

        s_atom_ene = df_both["#Energy"]

        return s_atom_ene

    def get_dos(self):
        file_path = f"./dos_dat/PDOS_A{self.atoms}_UP.dat"
        df_up = pd.read_csv(file_path, sep="\s+")

        file_path = f"./dos_dat/PDOS_A{self.atoms}_DW.dat"
        df_dw = pd.read_csv(file_path, sep="\s+")
        df_dw = df_dw.sort_values(by="#Energy", ascending=False)

        df_both = pd.concat([df_up, df_dw], axis=0)
        df_both = df_both.reset_index(drop=True)

        s_atom_dos = df_both[self.orbitals_group].sum(axis=1)

        return s_atom_dos

    def get_len(self):
        s_atom_ene = self.get_ene()
        return len(s_atom_ene)

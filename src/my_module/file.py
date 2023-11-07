import pandas as pd

class ReadFile:
    def __init__(self, atoms=None, orbitals_group=None):
        self.atoms = atoms # atom index
        self.orbitals_group = orbitals_group # list of orbitals

    def get_ene(self):
        # df_up is a pandas DataFrame
        # df_up        #Energy    s   py   pz   px  dxy  dyz  dz2  dxz  dx2  fy3x2  fxyz  fyz2  fz3  fxz2  fzx2  fx3  tot
        # 0    -38.80734  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # ...        ...  ...  ...  ...  ...  ...  ...  ...  ...  ...    ...   ...   ...  ...   ...   ...  ...  ...
        # 1199  21.19266  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # [1200 rows x 18 columns]
        file_path = f"./dos_dat/PDOS_A{self.atoms}_UP.dat"
        df_up = pd.read_csv(file_path, sep="\s+")

        # df_dw is a pandas DataFrame
        # df_dw        #Energy    s   py   pz   px  dxy  dyz  dz2  dxz  dx2  fy3x2  fxyz  fyz2  fz3  fxz2  fzx2  fx3  tot
        # 1199  21.19266  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # ...        ...  ...  ...  ...  ...  ...  ...  ...  ...  ...    ...   ...   ...  ...   ...   ...  ...  ...
        # 0    -38.80734  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # [1200 rows x 18 columns]
        file_path = f"./dos_dat/PDOS_A{self.atoms}_DW.dat"
        df_dw = pd.read_csv(file_path, sep="\s+")
        df_dw = df_dw.sort_values(by="#Energy", ascending=False) # Sort in descending order

        # df_both is a pandas DataFrame
        #        #Energy    s   py   pz   px  dxy  dyz  dz2  dxz  dx2  fy3x2  fxyz  fyz2  fz3  fxz2  fzx2  fx3  tot
        # 0    -38.80734  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # ...        ...  ...  ...  ...  ...  ...  ...  ...  ...  ...    ...   ...   ...  ...   ...   ...  ...  ...
        # 2399 -38.80734  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0    0.0   0.0   0.0  0.0   0.0   0.0  0.0  0.0
        # [2400 rows x 18 columns]
        df_both = pd.concat([df_up, df_dw], axis=0)
        df_both = df_both.reset_index(drop=True)

        # s_atom_ene is a pandas Series
        # 0      -38.80734
        #           ...
        # 2399   -38.80734
        # Name: #Energy, Length: 2400, dtype: float64
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

        # s_atom_dos is a pandas Series
        # 0       0.0
        #        ...
        # 2399    0.0
        # Length: 2400, dtype: float64
        s_atom_dos = df_both[self.orbitals_group].sum(axis=1)

        return s_atom_dos

    def get_len(self):
        s_atom_ene = self.get_ene()
        return len(s_atom_ene)

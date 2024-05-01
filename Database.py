import pandas as pd


class MovieDB:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file, lineterminator='\n')

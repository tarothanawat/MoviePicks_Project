import pandas as pd
import os


def csv_loader(folder, csv_name):
    current_dir = os.getcwd()
    path = os.path.join(current_dir,folder,csv_name)
    data = pd.read_csv(path)
    return data


class MovieDB:
    def __init__(self):
        self.orig_df = csv_loader(os.getcwd(), 'movies_with_links.csv')
        self.orig_df['release_date'] = pd.to_datetime(self.orig_df['release_date'])


    def get_orig_df(self):
        return self.orig_df



    def get_separated_genres(self, df):
        df.loc[:, 'genres'] = df['genres'].apply(lambda x: eval(x))
        df_sep_genres = df.explode('genres')
        df_sep_genres.reset_index(drop=True, inplace=True)
        return df_sep_genres


    def get_df_no_zero(self,df):
        no_zeros = df.loc[(df['revenue'] != 0) & (df['budget'] != 0)]
        return no_zeros

    def filter_by_attribute(self, df, key, value):
        filtered = df[df[key] == value]
        return filtered

    def storytelling(self, df, lang):
        # df_no_zeros = self.get_df_no_zero(df)
        df_by_lang = self.filter_by_attribute(df, 'original_language',lang)
        df_sep_genre = self.get_separated_genres(df_by_lang)
        return df_by_lang, df_sep_genre

    def search_handler(self):
        pass



if __name__ == '__main__':
    movie_db = MovieDB()

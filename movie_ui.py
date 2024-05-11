import tkinter as tk
from tkinter import ttk, Scrollbar
from Database import MovieDB
from MovieController import StorytellingGraph, ExplorationGraph
import webbrowser

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie picks application")
        self.movie_db = MovieDB()
        self.df = self.movie_db.get_orig_df()
        # self.minsize(800, 600)

        self.init_frames()
        self.populate_dropdowns()
        self.init_components()

    def init_components(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Exit", command=self.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def init_frames(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.search_page = SearchPage(self.notebook)
        self.data_storytelling_page = DataStorytellingPage(self.notebook)
        self.data_exploration_page = DataExplorationPage(self.notebook, self.df, self.movie_db)

        self.notebook.add(self.search_page, text="Search Page")
        self.notebook.add(self.data_storytelling_page, text="Data Storytelling")
        self.notebook.add(self.data_exploration_page, text="Data Exploration")


    def populate_dropdowns(self):
        languages = self.df['original_language'].unique()
        self.data_storytelling_page.language_dropdown['values'] = [x for x in languages]

        stories = ['Descriptive statistics of revenue and budget', 'Correlation of revenue and budget',
                   'Histogram of revenue and budget',
                   'Bar graph of avg revenue and budget by genre', 'Trend of revenue over the years']
        self.data_storytelling_page.story_dropdown['values'] = stories


class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = MovieDB()
        self.df = self.db.get_orig_df()
        self.df_sep_genres = self.db.get_separated_genres(self.df)
        self.configure(bg='#FAC589')
        self.init_components()

    def init_components(self):
        self.init_fonts()
        self.init_frames()
        self.init_top_frame()
        self.init_filters_frame()
        self.init_results_frame()

    def init_fonts(self):
        self.font_small = ('Arial', 12)
        self.font_head = ('Arial', 14)

    def init_frames(self):
        self.top_frame = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.filters_frame = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.results_frame = ttk.LabelFrame(self, relief=tk.RAISED, borderwidth=1, text='Search results')

        self.top_frame.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.filters_frame.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.results_frame.grid(column=1, row=0, sticky='nesw', padx=5, pady=5, rowspan=2)

        self.rowconfigure(0, weight=1)  # Top frame row
        self.rowconfigure(1, weight=1)  # Filters frame row

        # Set column weight for filters_frame to 1
        self.filters_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=10)

    def init_top_frame(self):
        self.label_1 = ttk.Label(self.top_frame, text='Search for a movie: ', font=self.font_head)
        self.search_input = tk.StringVar()
        self.search_bar = ttk.Entry(self.top_frame, textvariable=self.search_input, font=self.font_head, width=25)
        self.search_button = ttk.Button(self.top_frame, text='Search', command=self.filter_results)

        self.label_1.grid(row=0, column=0, padx=5, pady=5)
        self.search_bar.grid(row=0, column=1, padx=5, pady=5)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Bind the Enter key to the filter_results method
        self.search_bar.bind('<Return>', lambda event: self.filter_results())

    def init_filters_frame(self):
        self.label_filter = ttk.Label(self.filters_frame, text='Filters', font=self.font_head)
        self.label_release_year = ttk.Label(self.filters_frame, text='Release Year Range:', font=self.font_small)
        self.release_year_from = ttk.Entry(self.filters_frame, font=self.font_small, width=5)
        self.label_to = ttk.Label(self.filters_frame, text='to', font=self.font_small)
        self.release_year_to = ttk.Entry(self.filters_frame, font=self.font_small, width=5)
        self.genres_label = ttk.Label(self.filters_frame, text='Genres:', font=self.font_small)

        self.genre_list_var = tk.Variable()
        self.genre_list_box = tk.Listbox(self.filters_frame, selectmode=tk.MULTIPLE, listvariable=self.genre_list_var)
        for value in self.df_sep_genres['genres'].unique():
            self.genre_list_box.insert(tk.END, value)

        # Add scrollbar to the genre list box
        genre_scrollbar = Scrollbar(self.filters_frame, orient=tk.VERTICAL, )
        genre_scrollbar.config(command=self.genre_list_box.yview)
        self.genre_list_box.config(yscrollcommand=genre_scrollbar.set, width=15)
        genre_scrollbar.grid(row=2, column=1, sticky='ns')

        self.lang_list_label = ttk.Label(self.filters_frame, text='Original Language', font=self.font_small)
        self.lang_list_var = tk.StringVar()
        self.lang_combobox = ttk.Combobox(self.filters_frame, textvariable=self.lang_list_var, font=self.font_small,
                                          state='readonly')
        self.lang_combobox['values'] = list(self.df_sep_genres['original_language'].unique())

        self.rating_label = ttk.Label(self.filters_frame, text='Rating', font=self.font_small)
        self.rating_combobox = ttk.Combobox(self.filters_frame,
                                            values=['None', 'Most Rated', 'Least Rated'],
                                            font=self.font_small,
                                            state='readonly')
        self.rating_combobox.set('None')  # Set default selection to 'None'

        self.popularity_label = ttk.Label(self.filters_frame, text='Popularity', font=self.font_small)
        self.popularity_combobox = ttk.Combobox(self.filters_frame,
                                                values=['None', 'Most Popular', 'Least Popular'],
                                                font=self.font_small,
                                                state='readonly')
        self.label_filter.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.label_release_year.grid(row=1, column=0, padx=5, pady=5)
        self.release_year_from.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.label_to.grid(row=1, column=1, padx=5, pady=5, sticky='ns')
        self.release_year_to.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        self.genres_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.genre_list_box.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.lang_list_label.grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.lang_combobox.grid(row=2, column=3, padx=5, pady=5)

        self.rating_label.grid(row=3, column=0, padx=5, pady=5)
        self.rating_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.popularity_label.grid(row=3, column=2, padx=5, pady=5)
        self.popularity_combobox.grid(row=3, column=3, padx=5, pady=5)

    def init_results_frame(self):
        self.results_tree_view = ttk.Treeview(self.results_frame,
                                              columns=('Title', 'Release Year', 'Genres', 'Vote Average', 'Popularity'),
                                              show='headings')
        self.results_tree_view.heading('Title', text='Title')
        self.results_tree_view.heading('Release Year', text='Release Year')
        self.results_tree_view.heading('Genres', text='Genres')
        self.results_tree_view.heading('Vote Average', text='Vote Average')
        self.results_tree_view.heading('Popularity', text='Popularity')

        for col in self.results_tree_view['columns']:
            self.results_tree_view.column(col, width=175, anchor=tk.CENTER)

        # Add scrollbar to the results treeview
        results_scrollbar = Scrollbar(self.results_frame, orient=tk.VERTICAL)
        results_scrollbar.config(command=self.results_tree_view.yview)
        self.results_tree_view.config(yscrollcommand=results_scrollbar.set)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_tree_view.bind('<ButtonRelease-1>', self.open_imdb_link)

        self.results_tree_view.pack(expand=True, fill=tk.BOTH)

    def open_imdb_link(self, event):
        item = self.results_tree_view.item(self.results_tree_view.focus())
        title = item['values'][0]  # Assuming title is the first column
        row = self.df[self.df['title'] == title].iloc[0]
        imdb_link = row['imdb_link']
        if imdb_link:
            webbrowser.open(imdb_link)

    def filter_results(self):
        # Clear previous search results
        for item in self.results_tree_view.get_children():
            self.results_tree_view.delete(item)

        # Get user input
        search_term = self.search_input.get()
        release_year_from = self.release_year_from.get()
        release_year_to = self.release_year_to.get()
        selected_genres = [self.genre_list_box.get(index) for index in self.genre_list_box.curselection()]
        selected_language = self.lang_combobox.get()  # Get the selected language directly from the Combobox
        rating_filter = self.rating_combobox.get()
        popularity_filter = self.popularity_combobox.get()

        # Filter the DataFrame based on user input
        filtered_df = self.df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False)]
        if release_year_from:
            release_year_from = int(release_year_from)
            filtered_df = filtered_df[filtered_df['release_year'] >= release_year_from]
        if release_year_to:
            release_year_to = int(release_year_to)
            filtered_df = filtered_df[filtered_df['release_year'] <= release_year_to]
        if not release_year_from and not release_year_to:
            # If both "from" and "to" are not filled, search for all years
            pass
        if selected_genres:
            filtered_df = filtered_df[
                filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]
        if selected_language:  # Check if a language is selected
            filtered_df = filtered_df[filtered_df['original_language'] == selected_language]
        if rating_filter == 'Most Rated':
            filtered_df = filtered_df.sort_values(by='vote_average', ascending=False)
        elif rating_filter == 'Least Rated':
            filtered_df = filtered_df.sort_values(by='vote_average', ascending=True)
        if popularity_filter == 'Most Popular':
            filtered_df = filtered_df.sort_values(by='popularity', ascending=False)
        elif popularity_filter == 'Least Popular':
            filtered_df = filtered_df.sort_values(by='popularity', ascending=True)

        for index, row in filtered_df.iterrows():
            values = tuple(row[['title', 'release_year', 'genres', 'vote_average', 'popularity']])
            self.results_tree_view.insert('', 'end', values=values)

class DataStorytellingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = ttk.Label(self, text="Data Storytelling Page", font=('Arial',20))
        self.label.pack(pady=20)
        self.init_components()
        self.storytelling_manager = StorytellingGraph(self)
        self.current_canvas = None

    def init_components(self):
        # Dropdown menu for selecting original language
        self.language_label = ttk.Label(self, text="Select Original Language:")
        self.language_label.pack()
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, width=42, state='readonly')
        self.language_dropdown.pack(pady=5)

        # Dropdown menu for selecting the story to tell
        self.story_label = ttk.Label(self, text="Select the Story to know:")
        self.story_label.pack()
        self.story_var = tk.StringVar()
        self.story_dropdown = ttk.Combobox(self, textvariable=self.story_var, width=42, state='readonly')
        self.story_dropdown.pack(pady=5)

        # Button to show the selected story
        self.show_story_button = ttk.Button(self, text="Show Story", command=self.show_story)
        self.show_story_button.pack()

    def show_story(self):
        selected_language = self.language_var.get()
        selected_story = self.story_var.get()
        # Use the selected language and story to show the relevant information or visualization
        self.storytelling_manager.selected_language = selected_language

        if self.current_canvas:
            self.current_canvas.pack_forget()

        if selected_story == "Descriptive statistics of revenue and budget":
            self.current_canvas = self.storytelling_manager.get_descriptive_stats(self)

        elif selected_story == "Correlation of revenue and budget":
            self.current_canvas = self.storytelling_manager.get_correlation(self)

        elif selected_story == "Histogram of revenue and budget":
            self.current_canvas = self.storytelling_manager.get_histogram(self)

        elif selected_story == "Bar graph of avg revenue and budget by genre":
            self.current_canvas = self.storytelling_manager.get_bar_graph(self)

        elif selected_story == "Trend of revenue over the years":
            self.current_canvas = self.storytelling_manager.get_trend(self)
        self.current_canvas.pack(pady=5)


class DataExplorationPage(tk.Frame):
    def __init__(self, parent, df, db):
        super().__init__(parent)
        self.graph_controller = ExplorationGraph(self)
        self.init_components()
        self.df = df
        self.db = db
        self.df_sep_genres = self.db.get_separated_genres(self.df)

        self.selected_genre = []
        self.current_plot = None
        self.current_canvas = None  # Initialize current_canvas

    def init_components(self):
        self.font_combo = ('Arial', 8)
        self.font = ('Arial', 14)
        self.left_frame = tk.Frame(self, bg='black')
        self.right_frame = tk.Frame(self)

        # Right
        graph_label = ttk.Label(self.right_frame, text='Select Graph Type:', font=self.font)
        self.graph_combobox_var = tk.StringVar()
        self.graph_combobox = ttk.Combobox(self.right_frame, textvariable=self.graph_combobox_var, width=42,
                                            font=self.font_combo)
        self.graph_combobox.bind('<<ComboboxSelected>>', self.init_sub_frame)
        self.graph_combobox['values'] = ['Bar Graph', 'Line Plot', 'Scatter Plot'] #'Histogram', 'Scatter Plot'
        graph_label.pack(pady=20)
        self.graph_combobox.pack()



        self.left_frame.grid(column=0, row=0, sticky='nesw')
        self.right_frame.grid(column=1, row=0, sticky='nesw')

        # Configure grid row and column weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def show_graph(self):
        if self.current_canvas:
            self.current_canvas.pack_forget()

        if self.current_graph == "Bar Graph":
            x_attribute = self.x_axis_var.get()
            y_attribute = self.y_axis_var.get()
            selected_sub_values = self.get_selected_sub_values()
            self.current_canvas = self.graph_controller.plot_bar_graph(
                self.left_frame,
                x_attribute,
                selected_sub_values,
                y_attribute
            )
            self.current_canvas.pack(pady=5)
        elif self.current_graph == 'Line Plot':
            x_attribute = self.x_axis_var.get()
            y_attribute = self.y_axis_var.get()
            selected_sub_values = self.get_selected_sub_values()
            self.current_canvas = self.graph_controller.plot_line_plot(
                self.left_frame,
                x_attribute,
                selected_sub_values,
                y_attribute
            )
            self.current_canvas.pack(pady=5)
        elif self.current_graph == 'Scatter Plot':
            x_attribute = self.x_axis_var.get()
            y_attribute = self.y_axis_var.get()
            selected_sub_values = self.get_selected_sub_values()
            self.current_canvas = self.graph_controller.plot_scatter_plot(
                self.left_frame,
                x_attribute,
                y_attribute
            )
            self.current_canvas.pack(pady=5)
    def get_selected_sub_values(self):
        selected_indices = self.x_sub_listbox.curselection()
        selected_sub_values = [self.x_sub_listbox.get(idx) for idx in selected_indices]
        return selected_sub_values

    def init_sub_frame(self, *args):
        # Remove the sub_frame if it exists
        if hasattr(self, 'sub_frame'):
            self.sub_frame.pack_forget()


        self.current_graph = self.graph_combobox_var.get()
        x_axis = ['genres', 'release_year', 'original_language']
        y_axis = ['revenue', 'budget', 'profit']
        num_att = ['revenue', 'budget', 'profit', 'release_year']
        line_x = ['genres', 'original_language']
        self.sub_frame = tk.Frame(self.right_frame)
        self.x_axis_var = tk.StringVar()
        self.y_axis_var = tk.StringVar()
        self.x_axis_combobox = ttk.Combobox(self.sub_frame, textvariable=self.x_axis_var, width=42,
                                            font=self.font_combo)
        self.x_axis_combobox.bind('<<ComboboxSelected>>', self.sub_menu_handler)

        # Define a dictionary to map each X-axis option to its sub-values

        self.x_sub_values = {
            'genres': self.df_sep_genres['genres'].unique(),
            'original_language': self.df['original_language'].unique(),
            'release_year': self.df['release_year'].sort_values().unique()
        }

        self.x_sub_list_var = tk.Variable()
        self.x_sub_listbox = tk.Listbox(self.sub_frame, selectmode=tk.MULTIPLE, listvariable=self.x_sub_list_var)
        self.x_sub_listbox.bind('<<ListboxSelect>>', self.update_selected_sub_values)

        self.y_axis_combobox = ttk.Combobox(self.sub_frame, textvariable=self.y_axis_var, width=42,
                                            font=self.font_combo)
        if self.current_graph == 'Line Plot':
            self.x_axis_combobox['values'] = line_x
        else:
            self.x_axis_combobox['values'] = x_axis

        self.y_axis_combobox['values'] = y_axis

        # Add labels between the comboboxes
        ttk.Label(self.sub_frame, text="X Axis:").pack()
        self.x_axis_combobox.pack()

        ttk.Label(self.sub_frame, text="Y Axis:").pack()
        self.y_axis_combobox.pack()
        if self.current_graph == "Bar Graph" or self.current_graph == 'Line Plot':
            ttk.Label(self.sub_frame, text="Sub-Values:").pack()
            self.x_sub_listbox.pack()
        else:
            self.x_axis_combobox['values'] = num_att
            self.y_axis_combobox['values'] = num_att

        self.show_graph_button = ttk.Button(self.sub_frame, text="Show Graph",
                                            command=self.show_graph)  # Changed button name

        self.show_graph_button.pack()
        self.sub_frame.pack()

        # Pack the sub_frame if the current graph type requires it
    def sub_menu_handler(self, *args):
        current_x = self.x_axis_var.get()
        if current_x in self.x_sub_values:
            sub_values = self.x_sub_values[current_x]
            self.x_sub_listbox.delete(0, tk.END)  # Clear the listbox
            for value in sub_values:
                self.x_sub_listbox.insert(tk.END, value)

    def update_selected_sub_values(self, event=None):
        self.selected_genre = self.get_selected_sub_values()
        if self.x_axis_var.get() == 'release_year':
            self.x_sub_listbox['selectmode'] = tk.EXTENDED
        else:
            self.x_sub_listbox['selectmode'] = tk.MULTIPLE



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

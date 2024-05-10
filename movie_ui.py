import tkinter as tk
from tkinter import ttk
from Database import MovieDB
from graphing import StorytellingGraph, ExplorationGraph


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

        self.search_page = SearchPage(self.notebook, self.df, self.movie_db)
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
    def __init__(self, parent, df, db):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Search Page")
        self.label.pack(pady=20)
        self.df = df
        self.db = db

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
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, width=42)
        self.language_dropdown.pack(pady=5)

        # Dropdown menu for selecting the story to tell
        self.story_label = ttk.Label(self, text="Select the Story to know:")
        self.story_label.pack()
        self.story_var = tk.StringVar()
        self.story_dropdown = ttk.Combobox(self, textvariable=self.story_var, width=42)
        self.story_dropdown.pack(pady=5)

        # Button to show the selected story
        self.show_story_button = ttk.Button(self, text="Show Story", command=self.show_story)
        self.show_story_button.pack()

    def show_story(self):
        selected_language = self.language_var.get()
        selected_story = self.story_var.get()
        # Use the selected language and story to show the relevant information or visualization
        print("Selected Language:", selected_language)
        print("Selected Story:", selected_story)
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
        self.graph_combobox['values'] = ['Bar Graph', 'Line Plot', 'Histogram', 'Scatter Plot']
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

    def get_selected_sub_values(self):
        selected_indices = self.x_sub_listbox.curselection()
        selected_sub_values = [self.x_sub_listbox.get(idx) for idx in selected_indices]
        return selected_sub_values

    def init_sub_frame(self, *args):
        # Remove the sub_frame if it exists
        if hasattr(self, 'sub_frame'):
            self.sub_frame.pack_forget()

        self.current_graph = self.graph_combobox_var.get()
        x_axis = ['genres', 'original_language']
        y_axis = ['revenue', 'budget', 'profit']
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
        }

        self.x_sub_list_var = tk.Variable()
        self.x_sub_listbox = tk.Listbox(self.sub_frame, selectmode=tk.MULTIPLE, listvariable=self.x_sub_list_var)
        self.x_sub_listbox.bind('<<ListboxSelect>>', self.update_selected_sub_values)

        self.y_axis_combobox = ttk.Combobox(self.sub_frame, textvariable=self.y_axis_var, width=42,
                                            font=self.font_combo)
        self.x_axis_combobox['values'] = x_axis
        self.y_axis_combobox['values'] = y_axis

        # Add labels between the comboboxes
        ttk.Label(self.sub_frame, text="X Axis:").pack()
        self.x_axis_combobox.pack()

        ttk.Label(self.sub_frame, text="Y Axis:").pack()
        self.y_axis_combobox.pack()
        ttk.Label(self.sub_frame, text="Sub-Values:").pack()
        self.x_sub_listbox.pack()

        self.show_graph_button = ttk.Button(self.sub_frame, text="Show Graph",
                                            command=self.show_graph)  # Changed button name

        self.show_graph_button.pack()

        # Pack the sub_frame if the current graph type requires it
        if self.current_graph == "Bar Graph" or self.current_graph == 'Line Plot':
            self.sub_frame.pack()

    def sub_menu_handler(self, *args):
        current_x = self.x_axis_var.get()
        if current_x in self.x_sub_values:
            sub_values = self.x_sub_values[current_x]
            self.x_sub_listbox.delete(0, tk.END)  # Clear the listbox
            for value in sub_values:
                self.x_sub_listbox.insert(tk.END, value)

    def update_selected_sub_values(self, event=None):
        self.selected_genre = self.get_selected_sub_values()



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from Database import MovieDB
from graphing import StorytellingGraph


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
        self.data_exploration_page = DataExplorationPage(self.notebook)

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
        self.label = ttk.Label(self, text="Search Page")
        self.label.pack(pady=20)


class DataStorytellingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = ttk.Label(self, text="Data Storytelling Page", font=('Arial',20))
        self.label.pack(pady=20)
        self.init_components()
        self.storytelling_manager = StorytellingGraph()

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
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Data Exploration Page")
        self.label.pack(pady=20)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

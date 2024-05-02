import tkinter as tk
from tkinter import ttk

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie picks application")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.search_page = SearchPage(self.notebook)
        self.data_storytelling_page = DataStorytellingPage(self.notebook)
        self.data_exploration_page = DataExplorationPage(self.notebook)

        self.notebook.add(self.search_page, text="Search Page")
        self.notebook.add(self.data_storytelling_page, text="Data Storytelling")
        self.notebook.add(self.data_exploration_page, text="Data Exploration")

class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Search Page")
        self.label.pack(pady=20)

class DataStorytellingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Data Storytelling Page")
        self.label.pack(pady=20)



class DataExplorationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Data Exploration Page")
        self.label.pack(pady=20)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

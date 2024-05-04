import matplotlib as plt
from Database import MovieDB
plt.use("TkAgg")
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure
import pandas as pd


class StorytellingGraph:

    def __init__(self):
        super().__init__()
        self.db = MovieDB()
        self.df = self.db.get_orig_df()
        self._selected_language = None

    @property
    def selected_language(self):
        return self._selected_language

    @selected_language.setter
    def selected_language(self, new_lang):
        self._selected_language = new_lang
        self.df_by_lang, self.df_sep_genre = self.db.storytelling(self.df, self._selected_language)

    def get_descriptive_stats(self, root):
        statistics = self.df_by_lang[['budget', 'revenue']].describe()

        # Format the descriptive statistics for better readability
        formatted_stats = statistics.round(2)
        formatted_stats.index = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
        formatted_stats.columns = ['Revenue', 'Budget']

        # Convert the DataFrame to a formatted string
        formatted_string = formatted_stats.to_string()

        # Create a text widget to display the formatted descriptive statistics
        text_widget = tk.Text(root, height=10, width=50)
        text_widget.insert(tk.END, formatted_string)
        return text_widget

    def get_correlation(self, root):
        frame = tk.Frame(root)

        # Calculate correlation matrix
        statistics = self.df_by_lang[['budget', 'revenue']].corr()

        # Format the descriptive statistics for better readability
        formatted_stats = statistics.round(2)
        formatted_stats.index = ['Revenue', 'Budget']
        formatted_stats.columns = ['Revenue', 'Budget']
        formatted_string = formatted_stats.to_string()

        # Create a text widget for displaying the correlation matrix
        text_widget = tk.Text(frame, height=4, width=50)
        text_widget.insert(tk.END, formatted_string)
        text_widget.pack()

        # Create a figure and subplot for the scatter plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Plot the scatter plot on the subplot
        sns.scatterplot(x='budget', y='revenue', data=self.df_by_lang, ax=ax)
        ax.set_title('Scatter Plot of Revenue vs Budget')
        ax.set_xlabel('Budget')
        ax.set_ylabel('Revenue')
        ax.grid(True)

        # Create a canvas widget for displaying the scatter plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Return the frame containing the correlation matrix and scatter plot
        return frame

    def get_histogram(self, root):
        frame = tk.Frame(root)
        fig = Figure(figsize=(10, 6))

        # Add first subplot for the revenue histogram
        ax1 = fig.add_subplot(121)
        ax1.hist(self.df_by_lang['revenue'], bins=20, color='skyblue', edgecolor='black')
        ax1.set_title('Histogram of Revenue')
        ax1.set_xlabel('Revenue')
        ax1.set_ylabel('Frequency')
        ax1.grid(True)

        # Add second subplot for the budget histogram
        ax2 = fig.add_subplot(122)
        ax2.hist(self.df_by_lang['budget'], bins=20, color='salmon', edgecolor='black')
        ax2.set_title('Histogram of Budget')
        ax2.set_xlabel('Budget')
        ax2.set_ylabel('Frequency')
        ax2.grid(True)

        # Create a canvas widget for displaying the plots
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Return the frame containing the plots
        return frame

    def get_bar_graph(self, root):
        frame = tk.Frame(root)
        fig = Figure(figsize=(12, 6))  # Increase the width of the figure
        ax = fig.add_subplot(111)

        # Group by genre and calculate average metrics
        avg_metrics_by_genre = self.df_sep_genre.groupby('genres')[['revenue', 'budget']].mean().reset_index()

        # Plot bar chart
        ax.bar(avg_metrics_by_genre.index, avg_metrics_by_genre['revenue'], color='skyblue', label='Revenue')
        ax.bar(avg_metrics_by_genre.index, avg_metrics_by_genre['budget'], color='salmon', label='Budget')

        ax.set_xticks(avg_metrics_by_genre.index)
        ax.set_xticklabels(avg_metrics_by_genre['genres'], rotation=30)
        ax.set_xlabel('Genre')
        ax.set_ylabel('Average')
        ax.set_title('Average Revenue, Budget by Genre')
        ax.legend()

        # Create a canvas widget for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Return the frame containing the plot
        return frame

    def get_trend(self, root):
        frame = tk.Frame(root)

        # Create a new figure
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        self.df_by_lang.loc[:, 'year'] = self.df_by_lang['release_date'].dt.year

        # Plot line plot
        sns.lineplot(x='year', y='revenue', data=self.df_by_lang, color='skyblue', ax=ax)
        ax.set_xlabel('Year')
        ax.set_ylabel('Average Revenue')
        ax.set_title('Average Revenue Trend Over the Years')
        ax.grid(True)
        fig.tight_layout()

        # Create a canvas widget for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Return the canvas
        return frame


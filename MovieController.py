import matplotlib as plt
from Database import MovieDB
plt.use("TkAgg")
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure



class StorytellingGraph:
    """
    Class for creating storytelling graphs.
    """

    def __init__(self, parent):
        super().__init__()
        self.db = MovieDB()
        self.df = self.db.get_orig_df()
        self._selected_language = None
        self.parent = parent

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
        text_widget = tk.Text(root, height=10, width=50, font=('Arial', 14))
        text_widget.insert(tk.END, formatted_string)
        text_widget['state'] = 'disabled'
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
        text_widget = tk.Text(frame, height=4, width=50, font=('Arial', 14))
        text_widget.insert(tk.END, formatted_string)
        text_widget['state'] = 'disabled'
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
        sns.histplot(self.df_by_lang['revenue'], bins=20, color='skyblue', edgecolor='black', ax=ax1)
        ax1.set_title('Histogram of Revenue')
        ax1.set_xlabel('Revenue')
        ax1.set_ylabel('Frequency')
        ax1.grid(True)

        # Add second subplot for the budget histogram
        ax2 = fig.add_subplot(122)
        sns.histplot(self.df_by_lang['budget'], bins=20, color='salmon', edgecolor='black', ax=ax2)
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
        sns.barplot(x='genres', y='revenue', data=avg_metrics_by_genre, color='skyblue', ax=ax, label='Revenue')
        sns.barplot(x='genres', y='budget', data=avg_metrics_by_genre, color='salmon', ax=ax, label='Budget')

        if len(ax.get_xticks()) > 9:
            ax.tick_params(axis='x', rotation=30, labelsize=8)

        ax.set_xlabel('Genre')
        ax.set_ylabel('Average')
        ax.set_title('Average Revenue, Budget by Genre')

        # Add legend
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
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # self.df_by_lang.loc[:, 'year'] = self.df_by_lang['release_date'].dt.year

        # Plot line plot
        sns.lineplot(x='release_year', y='revenue', data=self.df_by_lang, color='skyblue', ax=ax)
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


class ExplorationGraph:
    """
    Class for creating exploration graphs.
    """
    def __init__(self, parent):
        super().__init__()
        self.db = MovieDB()
        self.df = self.db.get_orig_df()
        self.df_sep_genres = self.db.get_separated_genres(self.df)
        self.parent = parent

    def group_data(self, x_attribute, x_sub_var, y_attribute):
        if x_attribute == 'genres' and isinstance(x_sub_var, list) and len(x_sub_var) > 0:
            # Filter the dataframe to include only the selected genres
            grouped_data = self.df_sep_genres[self.df_sep_genres['genres'].isin(x_sub_var)]
        elif x_attribute == 'genres' and isinstance(x_sub_var, str):
            # Filter the dataframe to include only the selected genre
            grouped_data = self.df_sep_genres[self.df_sep_genres['genres'] == x_sub_var]
        elif x_attribute == 'genres':
            # Plot all genres
            grouped_data = self.df_sep_genres
        elif x_attribute == 'original_language' and isinstance(x_sub_var, list) and len(x_sub_var) > 0:
            # Filter the dataframe to include only the selected original languages
            grouped_data = self.df_sep_genres[self.df_sep_genres['original_language'].isin(x_sub_var)]
        elif x_attribute == 'original_language' and isinstance(x_sub_var, str):
            # Filter the dataframe to include only the selected original language
            grouped_data = self.df_sep_genres[self.df_sep_genres['original_language'] == x_sub_var]
        elif x_attribute == 'release_year' and isinstance(x_sub_var, list) and len(x_sub_var) > 0:
            # Convert list elements to integers
            x_sub_var = [int(year) for year in x_sub_var]
            # Filter the dataframe to include only the selected years
            grouped_data = self.df[self.df['release_year'].isin(x_sub_var)]
        elif x_attribute == 'release_year' and isinstance(x_sub_var, str):
            # Filter the dataframe to include only the selected year
            grouped_data = self.df[self.df['release_year'] == int(x_sub_var)]
        else:
            # Group by the x_attribute and calculate the mean of the y_attribute
            grouped_data = self.df.groupby(x_attribute)[y_attribute].mean().reset_index()

        return grouped_data

    def plot_bar_graph(self, root, x_attribute, x_sub_var, y_attribute):
        # Create a new figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        grouped_data = self.group_data(x_attribute, x_sub_var, y_attribute)


        # Plot the bar graph
        sns.barplot(x=x_attribute, y=y_attribute, data=grouped_data, ax=ax)
        ax.set_xlabel(x_attribute.capitalize())
        ax.set_ylabel(y_attribute.capitalize())
        ax.set_title(f'Average {y_attribute.capitalize()} by {x_attribute.capitalize()}')
        ax.grid(True)

        # Rotate x-axis labels if there are fewer than 15 ticks
        if len(ax.get_xticks()) > 9:
            ax.tick_params(axis='x', rotation=30, labelsize=8)

        # Create a canvas widget for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()

        return canvas_widget

    def plot_line_plot(self, root, x_attribute, x_sub_var, y_attribute):
        # Create a new figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        # Group the data based on the x_attribute and x_sub_var
        grouped_data = self.group_data(x_attribute, x_sub_var, y_attribute)

        # Plot the line plot
        sns.lineplot(x='release_year', y=y_attribute, hue='genres', palette='tab10', data=grouped_data, ax=ax)
        ax.set_xlabel('Release Year')
        ax.set_ylabel(y_attribute.capitalize())
        ax.set_title(f'Line Plot of {y_attribute.capitalize()} by {x_attribute.capitalize()}')
        ax.grid(True)
        if len(ax.get_xticks()) > 9:
            ax.tick_params(axis='x', rotation=30, labelsize=8)

        # Create a canvas widget for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()

        return canvas_widget

    def plot_scatter_plot(self, root, x_attribute, y_attribute, transparency=0.5):
        # Create a new figure
        fig = Figure(figsize=(12, 8))  # Increase the figure size for better readability
        ax = fig.add_subplot(111)

        # Plot each genre separately with a different color
        genres = self.df_sep_genres['genres'].unique()
        colors = plt.cm.tab20.colors  # Get a list of colors from the 'tab20' colormap
        for i, genre in enumerate(genres):
            genre_df = self.df_sep_genres[self.df_sep_genres['genres'] == genre]
            ax.scatter(genre_df[x_attribute], genre_df[y_attribute], label=genre, alpha=transparency,
                       color=colors[i % len(colors)])

        ax.set_xlabel(x_attribute.capitalize())
        ax.set_ylabel(y_attribute.capitalize())
        ax.set_title(f'Scatter Plot of {y_attribute.capitalize()} vs {x_attribute.capitalize()}')
        ax.legend(title='Genre', bbox_to_anchor=(1, 1), loc='upper left')  # Adjust legend position
        ax.grid(True)

        # Create a canvas widget for displaying the plot
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()

        return canvas_widget
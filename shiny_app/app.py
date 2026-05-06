# app.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, ui, render

# loading democracy dataset from csv
df = pd.read_csv("merged_clean.csv")


class DataLoader:
    """loading and validating the democracy dataset."""

    # class variable — storing column display names shared across all instances
    VARIABLE_LABELS = {
        "econ_percep": "Economic Perception",
        "log_gdp": "Log GDP per Capita",
        "unemp_mean": "Unemployment Rate",
        "democracy": "Democracy Score"
    }

    def __init__(self, dataframe):
        # storing dataframe as private instance variable
        self._df = dataframe

    @property
    def df(self):
        # exposing dataframe as read-only property
        return self._df

    def get_columns(self):
        # returning only columns that actually exist in the dataset
        return {k: v for k, v in self.VARIABLE_LABELS.items() if k in self._df.columns}


class Visualizer:
    """handling all plot rendering with configurable style."""

    # class-level defaults shared across all Visualizer instances
    DEFAULT_COLOR = "steelblue"
    DEFAULT_ALPHA = 0.6

    def __init__(self, color=None, alpha=None):
        # storing plot configuration as private instance variables
        self._color = color or self.DEFAULT_COLOR
        self._alpha = alpha or self.DEFAULT_ALPHA

    def scatter(self, df, x_col, y_col, x_label, y_label):
        """rendering scatter plot with trend line."""
        fig, ax = plt.subplots(figsize=(8, 5))

        # plotting scatter points
        ax.scatter(df[x_col], df[y_col],
                   color=self._color,
                   alpha=self._alpha,
                   s=60)

        # adding trend line using numpy polyfit
        z = df[[x_col, y_col]].dropna()
        if len(z) > 1:
            m, b = np.polyfit(z[x_col], z[y_col], 1)
            ax.plot(z[x_col], m * z[x_col] + b,
                    color="navy", linewidth=1.5)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"{x_label} vs Satisfaction with Democracy")
        ax.grid(True, alpha=0.3)
        return fig

    def histogram(self, df, col, label):
        """rendering histogram for a single variable."""
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df[col].dropna(), bins=20,
                color=self._color,
                alpha=self._alpha,
                edgecolor="white")
        ax.set_xlabel(label)
        ax.set_ylabel("Count")
        ax.set_title(f"Distribution of {label}")
        ax.grid(True, alpha=0.3)
        return fig


# initializing data loader 
loader = DataLoader(df)
available_vars = loader.get_columns()

#UI
app_ui = ui.page_fluid(
    ui.h2("Democracy & Economic Perception Explorer"),
    ui.p("Explore how economic indicators relate to satisfaction with democracy across countries."),
    ui.row(
        ui.column(4,
            ui.input_select(
                "x_var",
                "Select variable",
                choices=available_vars,
                selected="econ_percep"
            ),
            ui.input_select(
                "plot_type",
                "Plot type",
                choices={
                    "scatter": "Scatter vs Satisfaction",
                    "histogram": "Distribution"
                },
                selected="scatter"
            ),
            ui.input_select(
                "color",
                "Color",
                choices={
                    "steelblue": "Blue",
                    "tomato": "Red",
                    "seagreen": "Green",
                    "mediumpurple": "Purple"
                },
                selected="steelblue"
            ),
        ),
        ui.column(8,
            ui.output_plot("plot")
        )
    )
)

# Server 
def server(input, output, session):
    @output
    @render.plot
    def plot():
        x_col = input.x_var()
        color = input.color()
        x_label = available_vars[x_col]

        # creating Visualizer with selected color
        viz = Visualizer(color=color)

        if input.plot_type() == "scatter":
            # rendering scatter plot against satisfaction with democracy
            return viz.scatter(loader.df, x_col, "satdem",
                             x_label, "Satisfaction with Democracy")
        else:
            # rendering distribution histogram
            return viz.histogram(loader.df, x_col, x_label)


app = App(app_ui, server)
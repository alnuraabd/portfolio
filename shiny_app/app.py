# app.py
from shiny import App, ui, render
import matplotlib.pyplot as plt


class DataProcessor:
    """Generates data for a given number of points."""

    def __init__(self, n, mode="square"):
        # storing n and mode via setters so validation runs immediately
        self.n = n
        self.mode = mode

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        # ensuring n is a valid integer >= 2
        if not isinstance(value, int) or value < 2:
            raise ValueError("n must be an integer >= 2")
        self._n = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        # restricting mode to known function types only
        allowed = ("square", "linear", "cubic")
        if value not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        self._mode = value

    def generate_data(self):
        """Generate x and y based on the selected mode."""
        # computing y values differently depending on selected mode (polymorphic behaviour)
        x = list(range(self._n))
        if self._mode == "square":
            y = [i ** 2 for i in x]
        elif self._mode == "linear":
            y = [i * 2 for i in x]
        elif self._mode == "cubic":
            y = [i ** 3 for i in x]
        return x, y


class Visualizer:
    """Handles all plot rendering with configurable style."""

    # defining class-level defaults shared across all Visualizer instances
    DEFAULT_COLOR = "steelblue"
    DEFAULT_LINEWIDTH = 2

    def __init__(self, title="Plot", xlabel="X", ylabel="Y",
                 color=None, linewidth=None):
        # storing plot configuration as private instance variables
        self._title = title
        self._xlabel = xlabel
        self._ylabel = ylabel
        # falling back to class-level defaults if no value is passed
        self._color = color or self.DEFAULT_COLOR
        self._linewidth = linewidth or self.DEFAULT_LINEWIDTH

    @property
    def title(self):
        # exposing private attribute as read-only property
        return self._title

    @property
    def xlabel(self):
        return self._xlabel

    @property
    def ylabel(self):
        return self._ylabel

    def plot(self, x, y):
        """Render the plot using stored configuration."""
        # using stored instance state to configure the plot
        fig, ax = plt.subplots()
        ax.plot(x, y,
                color=self._color,
                linewidth=self._linewidth)
        ax.set_xlabel(self._xlabel)
        ax.set_ylabel(self._ylabel)
        ax.set_title(self._title)
        ax.grid(True, alpha=0.3)
        return fig


# mapping mode keys to display labels and y-axis titles
MODE_CONFIG = {
    "square": {"label": "Square (Y = X²)", "ylabel": "Y = X²"},
    "linear": {"label": "Linear (Y = 2X)",  "ylabel": "Y = 2X"},
    "cubic":  {"label": "Cubic (Y = X³)",   "ylabel": "Y = X³"},
}


app_ui = ui.page_fluid(
    ui.h2("Interactive Data Explorer"),
    ui.p("Use the controls below to explore different mathematical relationships."),
    ui.row(
        ui.column(4,
            ui.input_slider("n", "Number of points", min=10, max=200, value=50),
            ui.input_select(
                "mode",
                "Function type",
                # building choices dynamically from MODE_CONFIG
                choices={k: v["label"] for k, v in MODE_CONFIG.items()},
                selected="square"
            ),
            ui.input_select(
                "color",
                "Line color",
                choices={"steelblue": "Blue", "tomato": "Red", "seagreen": "Green"},
                selected="steelblue"
            ),
        ),
        ui.column(8,
            ui.output_plot("plot")
        )
    )
)



def server(input, output, session):
    @output
    @render.plot
    def plot():
        mode = input.mode()
        color = input.color()

        # creating a new DataProcessor on each render with current input values
        processor = DataProcessor(n=input.n(), mode=mode)
        x, y = processor.generate_data()

        # creating a Visualizer with config pulled from MODE_CONFIG
        viz = Visualizer(
            title=MODE_CONFIG[mode]["label"],
            xlabel="X",
            ylabel=MODE_CONFIG[mode]["ylabel"],
            color=color,
            linewidth=2
        )
        return viz.plot(x, y)


app = App(app_ui, server)
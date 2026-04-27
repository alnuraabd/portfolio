from shiny import App, ui, render
import matplotlib.pyplot as plt

# OOP
class DataProcessor:
    def __init__(self, n):
        self.n = n

    def generate_data(self):
        x = list(range(self.n))
        y = [i**2 for i in x]
        return x, y

class Visualizer:
    def plot(self, x, y):
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("X")
        plt.ylabel("Y = X^2")
        plt.title("Simple Interactive Plot")

# UI
app_ui = ui.page_fluid(
    ui.h2("Interactive Data App"),
    ui.input_slider("n", "Number of points", 10, 100, 50),
    ui.output_plot("plot")
)

# Server
def server(input, output, session):
    @output
    @render.plot
    def plot():
        processor = DataProcessor(input.n())
        x, y = processor.generate_data()

        viz = Visualizer()
        viz.plot(x, y)


app = App(app_ui, server)
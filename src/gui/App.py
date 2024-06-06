import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.service.ActualPredictedAverageMonthlyPrecipitation import ActualPredictedAverageMonthlyPrecipitation


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rainfall Data Visualization")
        self.geometry("600x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.pages = []

        self.create_page("Location 1", 50.01, 20.98)
        self.create_page("Location 2", 40.71, -74.01)  # New York coordinates

    def create_page(self, name, latitude, longitude):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        self.pages.append((name, latitude, longitude, frame))
        self.create_widgets(name, frame)

    def create_widgets(self, name, frame):
        label = ttk.Label(frame, text=f"Select the period for {name}:")
        label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        start_date_label = ttk.Label(frame, text="Start Date:")
        start_date_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.start_date_entry = ttk.Entry(frame)
        self.start_date_entry.grid(row=1, column=1, pady=5, padx=10)

        end_date_label = ttk.Label(frame, text="End Date:")
        end_date_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.end_date_entry = ttk.Entry(frame)
        self.end_date_entry.grid(row=2, column=1, pady=5, padx=10)

        generate_button = ttk.Button(frame, text="Generate Plot", command=lambda: self.generate_plot(name))
        generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.canvas = FigureCanvasTkAgg(plt.figure(), master=frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def generate_plot(self, name):
        try:
            latitude, longitude, frame = next(filter(lambda x: x[0] == name, self.pages))[1:]
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()

            plotter = ActualPredictedAverageMonthlyPrecipitation(latitude, longitude, start_date, end_date)
            plt = plotter.plot_rainfall_histogram()

            self.canvas.get_tk_widget().destroy()  # Destroy previous canvas
            self.canvas = FigureCanvasTkAgg(plt.figure(), master=frame)
            self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
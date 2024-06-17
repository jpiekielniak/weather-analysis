import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.ActualPredictedAverageMonthlyPrecipitation import ActualPredictedAverageMonthlyPrecipitation
from services.ActualPredictedAverageMonthlyTemperature import ActualPredictedAverageMonthlyTemperature
from services.ActualPredictedAverageMonthlyHumidity import ActualPredictedAverageMonthlyHumidity
from services.ActualPredictedAverageMonthlyWindSpeed import ActualPredictedAverageMonthlyWindSpeed


def create_action_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command)
    button.pack(fill=tk.X, pady=5)


def create_input_field(parent, label_text, default_value, row):
    tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='e')
    entry = tk.Entry(parent)
    entry.grid(row=row, column=1)
    entry.insert(0, default_value)
    return entry


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Visualization")
        self.root.geometry("1024x768")
        self.default_latitude = 50.01
        self.default_longitude = 20.98
        self.default_start_date = '2023-01-01'
        self.default_end_date = '2023-12-31'

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.input_frame = tk.LabelFrame(self.top_frame, text="Input Data", padx=10, pady=10)
        self.input_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.entry_latitude = create_input_field(self.input_frame, "Latitude:", self.default_latitude, 0)
        self.entry_longitude = create_input_field(self.input_frame, "Longitude:", self.default_longitude, 1)
        self.entry_start_date = create_input_field(self.input_frame, "Start Date (YYYY-MM-DD):", self.default_start_date, 2)
        self.entry_end_date = create_input_field(self.input_frame, "End Date (YYYY-MM-DD):", self.default_end_date, 3)

        self.button_frame = tk.LabelFrame(self.top_frame, text="Actions", padx=10, pady=10)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        create_action_button(self.button_frame, "Show Precipitation Plot", self.show_precipitation_plot)
        create_action_button(self.button_frame, "Show Temperature Plot", self.show_temperature_plot)
        create_action_button(self.button_frame, "Show Humidity Plot", self.show_humidity_plot)
        create_action_button(self.button_frame, "Show Wind Speed Plot", self.show_wind_speed_plot)

        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

    def show_precipitation_plot(self):
        self.show_plot(ActualPredictedAverageMonthlyPrecipitation, "plot_rainfall_histogram")

    def show_temperature_plot(self):
        self.show_plot(ActualPredictedAverageMonthlyTemperature, "plot_temperature")

    def show_humidity_plot(self):
        self.show_plot(ActualPredictedAverageMonthlyHumidity, "plot_humidity_histogram")

    def show_wind_speed_plot(self):
        self.show_plot(ActualPredictedAverageMonthlyWindSpeed, "plot_wind_speed_histogram")

    def show_plot(self, plotter_class, plot_method):
        try:
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()

            plotter = plotter_class(latitude, longitude, start_date, end_date)
            plot_func = getattr(plotter, plot_method)
            figure = plot_func()
            self.display_plot(figure)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_plot(self, figure):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

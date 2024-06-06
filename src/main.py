import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from service.ActualPredictedAverageMonthlyPrecipitation import ActualPredictedAverageMonthlyPrecipitation
from service.ActualPredictedAverageMonthlyTemperature import ActualPredictedAverageMonthlyTemperature


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Data Visualization")

        # Prefill dane
        self.default_latitude = 50.01
        self.default_longitude = 20.98
        self.default_start_date = '2023-01-01'
        self.default_end_date = '2023-12-31'

        # Kontener na górne elementy
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Kontener na pola wejściowe
        self.input_frame = tk.Frame(self.top_frame)
        self.input_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

        # Pola do wprowadzania danych
        tk.Label(self.input_frame, text="Latitude:").grid(row=0, column=0, sticky='e')
        self.entry_latitude = tk.Entry(self.input_frame)
        self.entry_latitude.grid(row=0, column=1)
        self.entry_latitude.insert(0, self.default_latitude)

        tk.Label(self.input_frame, text="Longitude:").grid(row=1, column=0, sticky='e')
        self.entry_longitude = tk.Entry(self.input_frame)
        self.entry_longitude.grid(row=1, column=1)
        self.entry_longitude.insert(0, self.default_longitude)

        tk.Label(self.input_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.entry_start_date = tk.Entry(self.input_frame)
        self.entry_start_date.grid(row=2, column=1)
        self.entry_start_date.insert(0, self.default_start_date)

        tk.Label(self.input_frame, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, sticky='e')
        self.entry_end_date = tk.Entry(self.input_frame)
        self.entry_end_date.grid(row=3, column=1)
        self.entry_end_date.insert(0, self.default_end_date)

        # Kontener na przyciski
        self.button_frame = tk.Frame(self.top_frame)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

        # Przyciski do wyświetlania wykresów
        self.button_precipitation = tk.Button(self.button_frame, text="Show Precipitation Plot",
                                              command=self.show_precipitation_plot)
        self.button_precipitation.pack(fill=tk.X, pady=5)

        self.button_temperature = tk.Button(self.button_frame, text="Show Temperature Plot",
                                            command=self.show_temperature_plot)
        self.button_temperature.pack(fill=tk.X, pady=5)

        # Placeholder for matplotlib plots
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

    def show_precipitation_plot(self):
        try:
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()

            plotter = ActualPredictedAverageMonthlyPrecipitation(latitude, longitude, start_date, end_date)
            figure = plotter.plot_rainfall_histogram()
            self.display_plot(figure)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_temperature_plot(self):
        try:
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()

            plotter = ActualPredictedAverageMonthlyTemperature(latitude, longitude, start_date, end_date)
            figure = plotter.plot_temperature()
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
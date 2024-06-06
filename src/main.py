import tkinter as tk
from tkinter import messagebox
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

        # Pola do wprowadzania danych
        tk.Label(root, text="Latitude:").grid(row=0, column=0)
        self.entry_latitude = tk.Entry(root)
        self.entry_latitude.grid(row=0, column=1)
        self.entry_latitude.insert(0, self.default_latitude)

        tk.Label(root, text="Longitude:").grid(row=1, column=0)
        self.entry_longitude = tk.Entry(root)
        self.entry_longitude.grid(row=1, column=1)
        self.entry_longitude.insert(0, self.default_longitude)

        tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.entry_start_date = tk.Entry(root)
        self.entry_start_date.grid(row=2, column=1)
        self.entry_start_date.insert(0, self.default_start_date)

        tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=3, column=0)
        self.entry_end_date = tk.Entry(root)
        self.entry_end_date.grid(row=3, column=1)
        self.entry_end_date.insert(0, self.default_end_date)

        # Przyciski do wyświetlania wykresów
        self.button_precipitation = tk.Button(root, text="Show Precipitation Plot",
                                              command=self.show_precipitation_plot)
        self.button_precipitation.grid(row=4, column=0, pady=10)

        self.button_temperature = tk.Button(root, text="Show Temperature Plot", command=self.show_temperature_plot)
        self.button_temperature.grid(row=4, column=1, pady=10)

    def show_precipitation_plot(self):
        try:
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()

            plotter = ActualPredictedAverageMonthlyPrecipitation(latitude, longitude, start_date, end_date)
            plotter.plot_rainfall_histogram()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_temperature_plot(self):
        try:
            latitude = float(self.entry_latitude.get())
            longitude = float(self.entry_longitude.get())
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()

            plotter = ActualPredictedAverageMonthlyTemperature(latitude, longitude, start_date, end_date)
            plotter.plot_temperature()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
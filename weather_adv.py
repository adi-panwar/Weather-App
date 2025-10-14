import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime, timedelta
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panfar Weather Forecast App")
        self.root.geometry("900x700")
        self.root.configure(bg="#909ff1")
        
        
        self.API_KEY = "your api enter here"  
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/"
        
        
        self.temp_unit = tk.StringVar(value="metric")
        
       
        self.weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️"
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        
        main_frame = tk.Frame(self.root, bg="#909ff1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="🌤️ Panfar Weather Forecast", 
                               font=("Arial", 28, "bold"), 
                               bg="#909ff1", fg="white")
        title_label.pack(pady=(0, 20))
        
        search_frame = tk.Frame(main_frame, bg="#909ff1")
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(search_frame, text="Location:", font=("Arial", 12), 
                bg="#909ff1", fg="white").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.location_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.location_entry.pack(side=tk.LEFT, padx=5, pady=10)
        self.location_entry.bind("<Return>", lambda e: self.get_weather())
        
        search_btn = tk.Button(search_frame, text="🔍 Search", 
                              command=self.get_weather,
                              font=("Arial", 11, "bold"),
                              bg="#4299e1", fg="white",
                              cursor="hand2", relief=tk.FLAT,
                              padx=15, pady=5)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        gps_btn = tk.Button(search_frame, text="📍 Use My Location", 
                           command=self.get_location_by_ip,
                           font=("Arial", 11, "bold"),
                           bg="#48bb78", fg="white",
                           cursor="hand2", relief=tk.FLAT,
                           padx=15, pady=5)
        gps_btn.pack(side=tk.LEFT, padx=5)
        
        unit_frame = tk.Frame(search_frame, bg="#428ce6")
        unit_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Radiobutton(unit_frame, text="°C", variable=self.temp_unit, 
                      value="metric", font=("Arial", 10),
                      bg="#7285f0", fg="white", selectcolor="#5f1e20",
                      command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(unit_frame, text="°F", variable=self.temp_unit, 
                      value="imperial", font=("Arial", 10),
                      bg="#7258f0", fg="white", selectcolor="#1e5f39",
                      command=self.refresh_display).pack(side=tk.LEFT)
        
      
        canvas = tk.Canvas(main_frame, bg="#1e3a5f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1e3a5f")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
       
        current_section = tk.Frame(self.scrollable_frame, bg="#1e3a5f")
        current_section.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        current_header_frame = tk.Frame(current_section, bg="#2c5282", relief=tk.RAISED, bd=1)
        current_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        current_header = tk.Label(current_header_frame, text="📍 Current Weather",
                                 font=("Arial", 20, "bold"), bg="#2c5282", 
                                 fg="white", anchor="center")
        current_header.pack(fill=tk.X, pady=12)
        
        self.current_frame = tk.Frame(current_section, bg="#2c5282", relief=tk.RAISED, bd=2)
        self.current_frame.pack(fill=tk.X)
        
        
        hourly_section = tk.Frame(self.scrollable_frame, bg="#1e3a5f")
        hourly_section.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        hourly_header_frame = tk.Frame(hourly_section, bg="#2c5282", relief=tk.RAISED, bd=1)
        hourly_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        hourly_header = tk.Label(hourly_header_frame, text="⏰ Hourly Forecast",
                                font=("Arial", 20, "bold"), bg="#2c5282", 
                                fg="white", anchor="center")
        hourly_header.pack(fill=tk.X, pady=12)
        
        self.hourly_frame = tk.Frame(hourly_section, bg="#2c5282", relief=tk.RAISED, bd=2)
        self.hourly_frame.pack(fill=tk.X)
        
        
        daily_section = tk.Frame(self.scrollable_frame, bg="#1e3a5f")
        daily_section.pack(fill=tk.BOTH, expand=True, padx=10)
        
        daily_header_frame = tk.Frame(daily_section, bg="#2c5282", relief=tk.RAISED, bd=1)
        daily_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        daily_header = tk.Label(daily_header_frame, text="📅 5-Day Forecast",
                               font=("Arial", 20, "bold"), bg="#2c5282", 
                               fg="white", anchor="center")
        daily_header.pack(fill=tk.X, pady=12)
        
        self.daily_frame = tk.Frame(daily_section, bg="#2c5282", relief=tk.RAISED, bd=2)
        self.daily_frame.pack(fill=tk.BOTH, expand=True)
        
        
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder text in empty frames"""
        placeholder_text = "🔍 Search for a location to view weather data"
        
        current_placeholder = tk.Label(self.current_frame, 
                                      text=placeholder_text,
                                      font=("Arial", 12), bg="#2c5282", 
                                      fg="#a0aec0", pady=30)
        current_placeholder.pack()
        
        hourly_placeholder = tk.Label(self.hourly_frame, 
                                     text=placeholder_text,
                                     font=("Arial", 12), bg="#2c5282", 
                                     fg="#a0aec0", pady=30)
        hourly_placeholder.pack()
        
        daily_placeholder = tk.Label(self.daily_frame, 
                                    text=placeholder_text,
                                    font=("Arial", 12), bg="#2c5282", 
                                    fg="#a0aec0", pady=30)
        daily_placeholder.pack()
        
    def get_weather(self):
        location = self.location_entry.get().strip()
        
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location!")
            return
        
       
        self.clear_frames()
        loading = tk.Label(self.current_frame, text="Loading weather data...",
                          font=("Arial", 14), bg="#2c5282", fg="white", pady=40)
        loading.pack()
        
       
        thread = threading.Thread(target=self.fetch_weather_data, args=(location,))
        thread.daemon = True
        thread.start()
        
    def fetch_weather_data(self, location):
        try:
           
            current_url = f"{self.BASE_URL}weather?q={location}&appid={self.API_KEY}&units={self.temp_unit.get()}"
            current_response = requests.get(current_url, timeout=10)
            
            if current_response.status_code == 401:
                self.root.after(0, lambda: messagebox.showerror(
                    "API Error", 
                    "Invalid API Key. Please get your free API key from:\nhttps://openweathermap.org/api"))
                self.root.after(0, self.show_placeholder)
                return
            
            if current_response.status_code == 404:
                self.root.after(0, lambda: messagebox.showerror(
                    "Location Error", 
                    f"Location '{location}' not found. Please check spelling."))
                self.root.after(0, self.show_placeholder)
                return
                
            current_response.raise_for_status()
            self.current_data = current_response.json()
            
            
            lat = self.current_data['coord']['lat']
            lon = self.current_data['coord']['lon']
            
            
            forecast_url = f"{self.BASE_URL}forecast?lat={lat}&lon={lon}&appid={self.API_KEY}&units={self.temp_unit.get()}"
            forecast_response = requests.get(forecast_url, timeout=10)
            forecast_response.raise_for_status()
            self.forecast_data = forecast_response.json()
            
            
            self.root.after(0, self.display_weather)
            
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: messagebox.showerror(
                "Connection Error", 
                "Request timed out. Please check your internet connection."))
            self.root.after(0, self.show_placeholder)
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", 
                f"Failed to fetch weather data:\n{str(e)}"))
            self.root.after(0, self.show_placeholder)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", 
                f"An unexpected error occurred:\n{str(e)}"))
            self.root.after(0, self.show_welcome_message)
    
    def get_location_by_ip(self):
        """Detect location using IP address"""
        self.clear_frames()
        loading = tk.Label(self.current_frame, text="Detecting your location...",
                          font=("Arial", 14), bg="#2c5282", fg="white", pady=40)
        loading.pack()
        
        thread = threading.Thread(target=self.fetch_location_by_ip)
        thread.daemon = True
        thread.start()
    
    def fetch_location_by_ip(self):
        try:
            
            response = requests.get("https://ipapi.co/json/", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            city = data.get('city', '')
            country = data.get('country_name', '')
            location = f"{city}, {country}" if city else country
            
            if location:
                self.root.after(0, lambda: self.location_entry.delete(0, tk.END))
                self.root.after(0, lambda: self.location_entry.insert(0, location))
                self.root.after(0, lambda: self.fetch_weather_data(location))
            else:
                raise Exception("Could not determine location")
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "GPS Error", 
                f"Could not detect location:\n{str(e)}\nPlease enter location manually."))
            self.root.after(0, self.show_welcome_message)
    
    def display_weather(self):
        self.clear_frames()
        
        
        self.display_current_weather()
        
        
        self.display_hourly_forecast()
        
        
        self.display_daily_forecast()
    
    def display_current_weather(self):
        data = self.current_data
        
        
        location = f"{data['name']}, {data['sys']['country']}"
        header = tk.Label(self.current_frame, text=location,
                         font=("Arial", 22, "bold"), bg="#2c5282", fg="white")
        header.pack(pady=(15, 5))
        
        
        dt_obj = datetime.fromtimestamp(data['dt'])
        date_str = dt_obj.strftime("%A, %B %d, %Y - %I:%M %p")
        date_label = tk.Label(self.current_frame, text=date_str,
                             font=("Arial", 11), bg="#2c5282", fg="#a0aec0")
        date_label.pack(pady=(0, 15))
        
        
        main_container = tk.Frame(self.current_frame, bg="#2c5282")
        main_container.pack(pady=10)
        
        
        weather_main = data['weather'][0]['main']
        icon = self.weather_icons.get(weather_main, "🌡️")
        
        icon_label = tk.Label(main_container, text=icon, 
                             font=("Arial", 80), bg="#2c5282")
        icon_label.pack(side=tk.LEFT, padx=20)
        
       
        temp_frame = tk.Frame(main_container, bg="#2c5282")
        temp_frame.pack(side=tk.LEFT, padx=20)
        
        temp = data['main']['temp']
        unit = "°C" if self.temp_unit.get() == "metric" else "°F"
        temp_label = tk.Label(temp_frame, text=f"{temp:.1f}{unit}",
                             font=("Arial", 48, "bold"), bg="#2c5282", fg="white")
        temp_label.pack()
        
        desc = data['weather'][0]['description'].title()
        desc_label = tk.Label(temp_frame, text=desc,
                             font=("Arial", 16), bg="#2c5282", fg="#a0aec0")
        desc_label.pack()
        
        feels_like = data['main']['feels_like']
        feels_label = tk.Label(temp_frame, text=f"Feels like {feels_like:.1f}{unit}",
                              font=("Arial", 12), bg="#2c5282", fg="#a0aec0")
        feels_label.pack(pady=(5, 0))
        
        
        details_frame = tk.Frame(self.current_frame, bg="#2c5282")
        details_frame.pack(pady=15, padx=20, fill=tk.X)
        
        details = [
            ("💧 Humidity", f"{data['main']['humidity']}%"),
            ("💨 Wind Speed", f"{data['wind']['speed']} {'m/s' if self.temp_unit.get() == 'metric' else 'mph'}"),
            ("🌡️ Pressure", f"{data['main']['pressure']} hPa"),
            ("👁️ Visibility", f"{data.get('visibility', 0) / 1000:.1f} km"),
            ("🌅 Sunrise", datetime.fromtimestamp(data['sys']['sunrise']).strftime("%I:%M %p")),
            ("🌇 Sunset", datetime.fromtimestamp(data['sys']['sunset']).strftime("%I:%M %p"))
        ]
        
        for i, (label, value) in enumerate(details):
            detail_frame = tk.Frame(details_frame, bg="#1e3a5f", relief=tk.RAISED, bd=1)
            detail_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
            details_frame.grid_columnconfigure(i%3, weight=1)
            
            tk.Label(detail_frame, text=label, font=("Arial", 10), 
                    bg="#1e3a5f", fg="#a0aec0").pack(pady=(8, 2))
            tk.Label(detail_frame, text=value, font=("Arial", 12, "bold"), 
                    bg="#1e3a5f", fg="white").pack(pady=(2, 8))
    
    def display_hourly_forecast(self):
        
        hourly_container = tk.Frame(self.hourly_frame, bg="#2c5282")
        hourly_container.pack(pady=15, padx=10)
        
       
        forecast_list = self.forecast_data['list'][:8]
        
        for i, forecast in enumerate(forecast_list):
            hour_frame = tk.Frame(hourly_container, bg="#1e3a5f", relief=tk.RAISED, bd=1)
            hour_frame.grid(row=0, column=i, padx=5, pady=5, sticky="n")
            
           
            dt_obj = datetime.fromtimestamp(forecast['dt'])
            time_str = dt_obj.strftime("%I:%M %p")
            tk.Label(hour_frame, text=time_str, font=("Arial", 10), 
                    bg="#1e3a5f", fg="#a0aec0").pack(pady=(10, 5))
            
            
            weather_main = forecast['weather'][0]['main']
            icon = self.weather_icons.get(weather_main, "🌡️")
            tk.Label(hour_frame, text=icon, font=("Arial", 30), 
                    bg="#1e3a5f").pack(pady=5)
            
            #
            temp = forecast['main']['temp']
            unit = "°C" if self.temp_unit.get() == "metric" else "°F"
            tk.Label(hour_frame, text=f"{temp:.0f}{unit}", 
                    font=("Arial", 12, "bold"), bg="#1e3a5f", fg="white").pack(pady=5)
            
            
            if 'pop' in forecast:
                pop = forecast['pop'] * 100
                tk.Label(hour_frame, text=f"💧 {pop:.0f}%", 
                        font=("Arial", 9), bg="#1e3a5f", fg="#a0aec0").pack(pady=(0, 10))
    
    def display_daily_forecast(self):
       
        daily_forecasts = {}
        for forecast in self.forecast_data['list']:
            dt_obj = datetime.fromtimestamp(forecast['dt'])
            date_key = dt_obj.strftime("%Y-%m-%d")
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = []
            daily_forecasts[date_key].append(forecast)
        
        
        for i, (date_key, forecasts) in enumerate(list(daily_forecasts.items())[:5]):
           
            temps = [f['main']['temp'] for f in forecasts]
            max_temp = max(temps)
            min_temp = min(temps)
            
           
            weather_conditions = [f['weather'][0]['main'] for f in forecasts]
            main_weather = max(set(weather_conditions), key=weather_conditions.count)
            
          
            day_frame = tk.Frame(self.daily_frame, bg="#1e3a5f", relief=tk.RAISED, bd=1)
            day_frame.pack(fill=tk.X, padx=20, pady=5)
            
           
            dt_obj = datetime.strptime(date_key, "%Y-%m-%d")
            day_name = dt_obj.strftime("%A, %b %d")
            tk.Label(day_frame, text=day_name, font=("Arial", 12, "bold"),
                    bg="#1e3a5f", fg="white", width=20, anchor="w").pack(side=tk.LEFT, padx=15, pady=15)
            
            
            icon = self.weather_icons.get(main_weather, "🌡️")
            tk.Label(day_frame, text=icon, font=("Arial", 30),
                    bg="#1e3a5f").pack(side=tk.LEFT, padx=15)
            
           
            desc = forecasts[len(forecasts)//2]['weather'][0]['description'].title()
            tk.Label(day_frame, text=desc, font=("Arial", 11),
                    bg="#1e3a5f", fg="#a0aec0", width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            
          
            unit = "°C" if self.temp_unit.get() == "metric" else "°F"
            temp_text = f"{max_temp:.0f}{unit} / {min_temp:.0f}{unit}"
            tk.Label(day_frame, text=temp_text, font=("Arial", 12, "bold"),
                    bg="#1e3a5f", fg="white").pack(side=tk.RIGHT, padx=15)
    
    def clear_frames(self):
        """Clear all content frames"""
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        for widget in self.daily_frame.winfo_children():
            widget.destroy()
    
    def refresh_display(self):
        """Refresh display when units are changed"""
        if hasattr(self, 'current_data') and hasattr(self, 'forecast_data'):
            location = self.location_entry.get()
            if location:
                self.get_weather()

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":

    main()

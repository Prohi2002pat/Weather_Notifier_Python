import time
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
from plyer import notification

# Function to get notification of weather report
def getNotification():
    cityName = place.get().strip()  # getting input of name of the place from user
    if not cityName:
        mb.showerror('Error', 'Please enter a city name')
        return
    
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"  # base url from where we extract weather report
    api_key = 'd850f7f52bf19300a9eb4b0aa6b80f0d'  # your API key here

    units = 'metric' if unit_var.get() == 'Celsius' else 'imperial'

    try:
        # This is the complete url to get weather conditions of a city
        complete_url = baseUrl + "appid=" + api_key + "&q=" + cityName + "&units=" + units
        response = requests.get(complete_url)  # requesting for the content of the url
        x = response.json()  # converting it into json 

        if x["cod"] != "404":
            y = x["main"]  # getting the "main" key from the json object

            # getting the "temp" key of y
            temp = y["temp"]

            # storing the value of the "pressure" key of y
            pres = y["pressure"]

            # getting the value of the "humidity" key of y
            hum = y["humidity"]

            # getting the value of "weather" key in variable z
            z = x["weather"]

            # getting the corresponding "description"
            weather_desc = z[0]["description"]

            # combining the above values as a string 
            info = f"Weather in {cityName}:\nTemperature = {temp}°{unit_var.get()[0]}\nPressure = {pres} hPa\nHumidity = {hum}%\nDescription = {weather_desc}"

            # showing the notification 
            notification.notify(
                title="Weather Report",
                message=info,
                timeout=10  # increased timeout to ensure the user has time to read the notification
            )
        else:
            mb.showerror('Error', 'City Not Found')

    except requests.exceptions.RequestException as e:
        mb.showerror('Error', 'Network error, please try again')
    except Exception as e:
        mb.showerror('Error', str(e))  # show pop up message if any error occurred

# creating the window
wn = Tk()
wn.title("Rohit Satish Patil Weather Desktop Notifier")
wn.geometry('700x250')
wn.config(bg='light green')

# Heading label
Label(wn, text="Weather Desktop Notifier", font=('Courier', 15), fg='grey19', bg='light green').place(x=150, y=15)

# Getting the place name 
Label(wn, text='Enter Location:', font=("Courier", 13), bg='light green').place(relx=0.05, rely=0.3)

place = StringVar(wn)
place_entry = Entry(wn, width=50, textvariable=place)
place_entry.place(relx=0.5, rely=0.3)

# Unit selection
Label(wn, text='Select Unit:', font=("Courier", 13), bg='light green').place(relx=0.05, rely=0.45)

unit_var = StringVar(value='Celsius')
units = ttk.Combobox(wn, textvariable=unit_var, values=['Celsius', 'Fahrenheit'])
units.place(relx=0.5, rely=0.45)

# Button to get notification
btn = Button(wn, text='Get Notification', font=7, fg='grey19', command=getNotification)
btn.place(relx=0.4, rely=0.75)

# run the window till closed by user
wn.mainloop()

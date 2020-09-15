import PySimpleGUI as sg
import requests, json
from sys import exit
from datetime import datetime
import os

appdata_path = os.getenv('APPDATA')
final_path = appdata_path + '\\Pyweather\\config.json'

api_key = "b83bab83e668b70cbfc0b9cc6ebadc86"

base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_data(x):
    x = response.json()
    if x['cod'] != "404":
        c_sunrise = str(datetime.fromtimestamp(int(x['sys']['sunrise'])).time())
        c_sunset = str(datetime.fromtimestamp(int(x['sys']['sunset']) - 43200).time())

        c_y = x["main"]

        c_description = x["weather"][0]['description'].capitalize()

        c_temp = round(int(c_y["temp"]) - 273.15)
        c_feels_like = round(int(c_y['feels_like']) - 273.15, 2)

        c_pressure = c_y["pressure"]

        c_wind = x['wind']['speed']

        c_humidity = c_y["humidity"]
        c_icon = x['weather'][0]['icon']
        c_time = datetime.now().strftime("%B %d  %I:%M %p")
        return c_sunrise, c_sunset, c_description, c_temp, c_feels_like, c_pressure, c_wind, c_humidity, c_icon, c_time
    else:
        return "404"

def save_settings(city_name,new_temp,new_feels_like,new_pressure,new_humidity,new_wind,new_sunrise,new_sunset,new_icon,new_description,time):
    new_file = open(final_path, 'w')
    new_settings = {
        "city": city_name,
        "temp": new_temp,
        "feels_like": new_feels_like,
        "pressure": new_pressure,
        "humidity": new_humidity,
        "wind": new_wind,
        "sun_rise": new_sunrise,
        "sun_set": new_sunset,
        "icon": new_icon,
        "description": new_description,
        "current_time": time
    }
    json.dump(new_settings, new_file, indent=4)
    new_file.close()

def update(gui,s_city, s_temp, s_feels_like, s_pressure, s_humidity, s_wind, s_sunrise, s_sunset, s_icon, s_description, s_current_time):
    gui['-sunrise-'].update(s_sunrise+'AM')
    gui['-sunset-'].update(s_sunset+'PM')
    gui['-description-'].update(s_description)
    gui['-temp-'].update(str(s_temp)+'°C')
    gui['-feels_like-'].update(str(s_feels_like)+'°C')
    gui['-pressure-'].update(str(s_pressure)+'hap')
    gui['-wind-'].update(str(s_wind)+'m/h')
    gui['-humidity-'].update(str(s_humidity)+'%')
    gui['-city-'].update(s_city)
    gui['-icon-'].update('icon\\'+s_icon+'.png')
    gui['-current_time-'].update(s_current_time)

try:
    file = open(final_path, 'r')
    settings = json.load(file)
    city = settings['city']
    do_res = True


except FileNotFoundError:
    city = sg.popup_get_text('Please enter the name of your city:', '', 'Gopalganj', no_titlebar=True)
    if city is None:
        exit()
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?appid=b83bab83e668b70cbfc0b9cc6ebadc86&q=' + city
        response = requests.get(url)
        x = response.json()
        if x['cod'] != "404":
            sunrise, sunset, description, temp, feels_like, pressure, wind, humidity,icon,current_time = get_data(x)
        else:
            sg.popup('City not Found! Please check the spelling!')

    except requests.exceptions.ConnectionError:
        sg.popup('', 'Please check your internet connection!')
        exit()

    if x['cod'] != '404':
        with open(final_path, 'w') as file:
            default_settings = {
                "city":city,
                "temp":temp,
                "feels_like":feels_like,
                "pressure":pressure,
                "humidity":humidity,
                "wind":wind,
                "sun_rise":sunrise,
                "sun_set":sunset,
                "icon":icon,
                "description":description,
                "current_time":current_time
            }
            json.dump(default_settings, file, indent=4)
            file.close()
    else:
        sg.popup('City not Found! Please check the spelling!')
    do_res = False


if do_res:
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    try:
        response = requests.get(complete_url)
        x = response.json()
        sunrise, sunset, description, temp, feels_like, pressure, wind, humidity, icon, current_time = get_data(x)
        save_settings(city, temp,feels_like,pressure,humidity,wind,sunrise,sunset,icon,description,current_time)
    except requests.exceptions.ConnectionError:
        temp = settings['temp']
        feels_like = settings['feels_like']
        pressure = settings['pressure']
        humidity = settings['humidity']
        wind = settings['wind']
        sunrise = settings['sun_rise']
        sunset = settings['sun_set']
        icon = settings['icon']
        description = settings['description']
        current_time = settings['current_time']


info_font_reg = ('Times New Roman', '12')
info_font_bold = ('Times New Roman', '12', 'bold')
change_city_button_font = ('', '10', 'italic')
description_font = ('', '12', 'italic')


city_font = ('Times New Roman', '25')
column_info_layout = [
    [sg.Text(city, font=city_font, background_color='#195240', text_color='#bbc9bb', key='-city-')],
    [sg.Text(description,font=description_font, background_color='#195240', text_color='#bbc9bb', key='-description-')]
]

column_image = [
    [sg.B('close', button_color=('#ff6161','#195240'), border_width=0, use_ttk_buttons=True, disabled_button_color=('#bbc9bb','#195240'), font=change_city_button_font)],
    [sg.Image('icon\\'+icon+'.png', background_color='#99ccff', size=(175,175), key='-icon-')]
]

temp_font = ('Times New Roman', '75')
column_temp = [
    [sg.T(str(temp)+'°C', text_color='#195240', font = temp_font, background_color='#bbc9bb', border_width=0, key='-temp-')]
]

column_info = [
    [sg.T('Feels like', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')],
    [sg.T('Humidity', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')],
    [sg.T('Pressure', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')],
    [sg.T('Wind', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')],
    [sg.T('Sun rise', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')],
    [sg.T('Sun set', font=info_font_reg, text_color='#195240', background_color='#bbc9bb')]
]

column_info_bold = [
    [sg.T(str(feels_like)+'°C', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-feels_like-')],
    [sg.T(str(humidity)+'%', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-humidity-')],
    [sg.T(str(pressure)+'hap', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-pressure-')],
    [sg.T(str(wind)+'m/h', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-wind-')],
    [sg.T(str(sunrise)+'AM', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-sunrise-')],
    [sg.T(str(sunset)+'PM', font=info_font_bold, text_color='#195240', background_color='#bbc9bb', key='-sunset-')]
]

frame1 = [
    [sg.Column(column_info_layout, background_color='#195240',size=(422,100)), sg.Col(column_image,background_color='#195240',size=(175,200))]
]

frame2 = [
    [sg.Column(column_temp, background_color='#bbc9bb',size=(350,200)), sg.Col(column_info, background_color='#bbc9bb'), sg.Col(column_info_bold, background_color='#bbc9bb',pad=((10,25),(0,0)))]
]

frame3 = [
    [
        sg.T('Updated', background_color='#195240', text_color='#bbc9bb'),
        sg.Text(current_time, background_color='#195240', text_color='#bbc9bb',size=(36,1), key='-current_time-'),
        sg.B('Click here to change city', enable_events=True, font=change_city_button_font,button_color=('#bbc9bb','#195240'), border_width=0, use_ttk_buttons=True, disabled_button_color=('#bbc9bb','#195240'))
    ]
]

layout = [
    [sg.Frame('', frame1, border_width=0, background_color='#195240', pad=((0,0), (0,0)))],
    [sg.Frame('', frame2, border_width=0, background_color='#bbc9bb', pad=((0,0), (0,0)))],
    [sg.Frame('', frame3, border_width=0, background_color='#195240', pad=((0,0), (0,0)))]
]

window = sg.Window('Update-man', layout, no_titlebar=True, background_color='#78b5a2', margins=(0,0), grab_anywhere=True)

while True:                             # The Event Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'close':
        break

    if event == 'Click here to change city':
        window.hide()
        city = sg.popup_get_text('Please enter the city name: ', '', 'Gopalganj', no_titlebar=True)
        try:
            response = requests.get(base_url + "appid=" + api_key + "&q=" + city)
            x = response.json()
            if x['cod'] != '404':
                sunrise, sunset, description, temp, feels_like, pressure, wind, humidity, icon, current_time = get_data(x)
                save_settings(city, temp,feels_like,pressure,humidity,wind,sunrise,sunset,icon,description,current_time)
                update(window,city, temp, feels_like, pressure, humidity, wind, sunrise, sunset, icon, description, current_time)
            else:
                sg.popup('City not found!\nPlease Check your spelling!')
                city = sg.popup_get_text('Please enter the city name: ', '', 'Gopalganj', no_titlebar=True)

        except requests.exceptions.ConnectionError:
            sg.popup('Please Check Your Internet Connection and then try again!')
        window.un_hide()

    try:
        response = requests.get(base_url + "appid=" + api_key + "&q=" + city)
        x = response.json()
        if x['cod'] != '404':
            sunrise, sunset, description, temp, feels_like, pressure, wind, humidity, icon, current_time = get_data(x)
            save_settings(city, temp, feels_like, pressure, humidity, wind, sunrise, sunset, icon,
                          description, current_time)
            update(window, city, temp, feels_like, pressure, humidity, wind, sunrise, sunset, icon, description,
                   current_time)
        print("I am in try")
    except requests.exceptions.ConnectionError:
        print("I am in except")
        pass




window.close()
file.close()
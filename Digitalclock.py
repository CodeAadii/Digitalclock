import tkinter as tk
import time
from datetime import datetime
from tkinter import messagebox
import re
import pytz

root = tk.Tk()
root.title("Digital Clock")
root.iconbitmap("clock.ico")
root.geometry("750x770")

current_time = tk.StringVar()
current_time.set(time.strftime('%I:%M:%S %p'))

stopwatch_running = False
stopwatch_start_time = 0
stopwatch_elapsed_time = 0

alarm_time = tk.StringVar()
time_format = tk.StringVar()
timer_time = tk.StringVar()
timer_countdown = tk.StringVar()
timer_countdown.set("00:00")

alarm_triggered = False
timer_triggered = False

world_clock_cities = {
    "Grand_Turk": "America/Grand_Turk",
    "Madrid": "Europe/Madrid",
    "Aden": "Asia/Aden",
    "Brisbane": "Australia/Brisbane"
}

world_clock_labels = []

def create_widgets():
    global stopwatch_label, stopwatch_start_button, stopwatch_pause_button, stopwatch_reset_button, alarm_set_button, timer_button, lbl_alarm_status,timer_pause_button,timer_restart_button,time_format_menu
    clock_label = tk.Label(root, font=("Arial", 65), textvariable=current_time, bg="black", fg="white")
    clock_label.place(x="125", y="20")

    stopwatch_label = tk.Label(root, font=('Arial', 35), text='Stopwatch: 00:00:00')
    stopwatch_label.place(x="10", y="160")

    stopwatch_start_button = tk.Button(root, text="Start", font=("Arial", 16), command=start_stopwatch)
    stopwatch_start_button.place(x="10", y="230")

    stopwatch_pause_button = tk.Button(root, text="Pause", font=("Arial", 16), command=pause_stopwatch, state="disabled")
    stopwatch_pause_button.place(x="75", y="230")

    stopwatch_reset_button = tk.Button(root, text="Reset", font=("Arial", 16), command=reset_stopwatch, state="disabled")
    stopwatch_reset_button.place(x="155", y="230")

    alarm_label = tk.Label(root, font=("Arial", 32), text="Alarm Time:")
    alarm_label.place(x="10", y="300")

    alarm_entry = tk.Entry(root, textvariable=alarm_time, font=("Arial", 32), width="8")
    alarm_entry.place(x="270", y="300")

    time_format.set("AM")  # Set the default value

    time_format_menu = tk.OptionMenu(root, time_format, "AM", "PM")
    time_format_menu.config(width=3,font=("Arial", 26))
    time_format_menu.place(x="460", y="300")

    alarm_set_button = tk.Button(root, text="Set Alarm", font=('Arial', 16), command=set_alarm)
    alarm_set_button.place(x="10", y="370")

    timer_label = tk.Label(root, font=("Arial", 32), text="Timer:")
    timer_label.place(x="10", y="440")

    timer_entry = tk.Entry(root, textvariable=timer_time, font=("Arial", 32), width="10")
    timer_entry.place(x="160", y="440")

    timer_button = tk.Button(root, text="Start Timer", command=start_timer, font=("Arial", 16))
    timer_button.place(x="10", y="510")

    timer_pause_button = tk.Button(root, text="Pause Timer", command=pause_timer, font=("Arial", 16), state="disabled")
    timer_pause_button.place(x="150", y="510")

    timer_restart_button = tk.Button(root, text="Restart Timer", command=restart_timer, font=("Arial", 16), state="disabled")
    timer_restart_button.place(x="300", y="510")

    timer_countdown_label = tk.Label(root, font=("Arial", 32, "bold"), textvariable=timer_countdown)
    timer_countdown_label.place(x="430", y="440")

    timer_label = tk.Label(root, font=("Arial", 28, "bold"), text="World Clock")
    timer_label.place(x="250", y="565")

    lbl_alarm_status = tk.Label(root, text="", font=('Arial', 20))
    lbl_alarm_status.place(x="160", y="372")


def update_clock():
    current_time.set(time.strftime('%I:%M:%S %p'))
    root.after(1000, update_clock)


def start_stopwatch():
    global stopwatch_running, stopwatch_start_time, stopwatch_elapsed_time
    if not stopwatch_running:
        stopwatch_start_time = time.time() - stopwatch_elapsed_time
        stopwatch_running = True
        stopwatch_start_button.config(state='disabled')
        stopwatch_pause_button.config(state='normal')
        stopwatch_reset_button.config(state='normal')
        update_stopwatch()


def pause_stopwatch():
    global stopwatch_running
    if stopwatch_running:
        stopwatch_running = False
        stopwatch_start_button.config(state='normal')
        stopwatch_pause_button.config(state='disabled')


def reset_stopwatch():
    global stopwatch_running, stopwatch_elapsed_time
    if not stopwatch_running:
        stopwatch_elapsed_time = 0
        stopwatch_label.config(text='Stopwatch: 00:00:00')
        stopwatch_reset_button.config(state='disabled')


def update_stopwatch():
    global stopwatch_running, stopwatch_elapsed_time, stopwatch_label
    if stopwatch_running:
        elapsed_time = time.time() - stopwatch_start_time + stopwatch_elapsed_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        stopwatch_time = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        stopwatch_label.config(text='Stopwatch: ' + stopwatch_time)
    root.after(1000, update_stopwatch)


def set_alarm():
    global alarm_triggered
    alarm_time_str = alarm_time.get()
    alarm_time_format = time_format.get()
    lbl_alarm_status.config(text=f"(Alarm set for {alarm_time_str} {alarm_time_format})")

    if not re.match(r'^[0-9:]+$', alarm_time_str):
        messagebox.showwarning("Invalid Input", "Please enter a valid alarm time.")
        return

    if not alarm_time_str.strip():
        messagebox.showwarning("Invalid Input", "Please enter a valid alarm time.")
        return

    if ' ' in alarm_time_str:
        messagebox.showwarning("Invalid Input", "Please remove any blank spaces.")
        return

    alarm_hours, alarm_minutes = map(int, alarm_time_str.split(':'))
    current_hours = int(time.strftime('%I'))
    current_minutes = int(time.strftime('%M'))
    if alarm_hours < 0 or alarm_hours > 24 or alarm_minutes < 0 or alarm_minutes > 59:
        messagebox.showwarning('Invalid Input', 'Invalid alarm time.')
        return
    if alarm_hours < current_hours or (alarm_hours == current_hours and alarm_minutes <= current_minutes):
        messagebox.showwarning('Invalid Input', 'Alarm time should be in the future')
        return
    else:
        messagebox.showinfo('Success', 'Alarm set successfully')
    alarm_triggered = False
    check_alarm()



def check_alarm():
    global alarm_triggered
    current_time_str = time.strftime('%I:%M')
    alarm_time_str = alarm_time.get()
    alarm_time_format = time_format.get()
    if not alarm_triggered and current_time_str == alarm_time_str and alarm_time_format == time.strftime('%p'):
        messagebox.showinfo('Alarm', 'Alarm Reminder!')
        alarm_triggered = True
    root.after(200, check_alarm)


def start_timer():
    global timer_triggered, timer_pause_button, timer_restart_button
    timer_time_str = timer_time.get()
    if not timer_time_str.strip():
        messagebox.showwarning("Invalid Input", "Please enter a valid timer duration.")
        return
    if ' ' in timer_time_str:
        messagebox.showwarning("Invalid Input", "Please remove any blank spaces.")
        return

    try:
        timer_min, timer_sec = map(int, timer_time_str.split(":"))
        if timer_min < 0 or timer_sec < 0 or timer_sec > 59:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid timer duration in MM:SS format.")
        return

    timer_seconds = timer_min * 60 + timer_sec
    timer_countdown.set("{:02d}:{:02d}".format(timer_min, timer_sec))
    timer_pause_button.config(state="normal")
    timer_restart_button.config(state="normal")
    timer_triggered = True
    root.after(1000, update_timer_countdown, timer_seconds)


def pause_timer():
    global timer_triggered
    timer_triggered = False


def restart_timer():
    global timer_triggered
    timer_triggered = False
    start_timer()


def update_timer_countdown(seconds):
    global timer_triggered
    if seconds > 0 and timer_triggered:
        minutes = seconds // 60
        seconds %= 60
        timer_countdown.set("{:02d}:{:02d}".format(minutes, seconds))
        root.after(1000, update_timer_countdown, seconds - 1)
    elif seconds <= 0 and timer_triggered:
        timer_countdown.set("00:00")
        messagebox.showinfo("Timer", "Time's up!")
        timer_restart_button.config(state="disabled")
        timer_pause_button.config(state="disabled")
        timer_triggered = False


def update_world_clock():
    global world_clock_labels
    world_clock_labels = []

    y_position = 630
    for city, timezone in world_clock_cities.items():
        city_label = tk.Label(root, font=("Arial", 16), text=city + ":")
        city_label.place(x="10", y=y_position)
        time_label = tk.Label(root, font=("Arial", 16), text=get_world_time(timezone))
        time_label.place(x="140", y=y_position)
        world_clock_labels.append(city_label)
        world_clock_labels.append(time_label)
        y_position += 30

    root.after(1000, update_world_clock)


def get_world_time(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime('%I:%M:%S %p')


create_widgets()
update_clock()
update_world_clock()

root.mainloop()

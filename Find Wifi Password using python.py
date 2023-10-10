import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def show_loading_screen():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_label = tk.Label(loading_window, text="Loading, please wait...")
    loading_label.pack(padx=20, pady=20)
    loading_window.update()
    return loading_window

def hide_loading_screen(loading_window):
    loading_window.destroy()

def get_network_info():
    loading_window = show_loading_screen()
    root.update_idletasks() 

    try:
        devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
        devices = devices.decode('ascii').replace("\r", "")
        nearby = [x[x.find(':') + 1:].replace('\r', '').strip() for x in devices.split('\n') if "SSID" in x]

        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
        data = meta_data.decode('utf-8', errors="backslashreplace")
        data = data.split('\n')

        profiles = []

        for i in data:
            if "All User Profile" in i:
                i = i.split(":")[1][1:-1]
                profiles.append(i)

        result_text.delete(1.0, tk.END) 
        result_text.insert(tk.END, "{:<30}| {:<30} | {:<20}\n".format("Wi-Fi Name", "Password", "Nearby Network"))
        result_text.insert(tk.END, "-" * 80 + "\n")

        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
                results = results.decode('utf-8', errors="backslashreplace").split('\n')

                password = ""
                for b in results:
                    if "Key Content" in b:
                        password = b.split(":")[1].strip()
                        break

                nearbyFlag = i in nearby
                result_text.insert(tk.END, "{:<30}| {:<30} | {:<20}\n".format(i, password, "Y" if nearbyFlag else "N"))

            except subprocess.CalledProcessError:
                result_text.insert(tk.END, "{:<30}| {:<}\n".format(i, ""))

    except Exception as e:
        result_text.insert(tk.END, "Error: {}\n".format(e))
    
    hide_loading_screen(loading_window)


root = tk.Tk()
root.title("Wi-Fi Network Info")


result_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
result_text.pack(padx=10, pady=10)


get_info_button = ttk.Button(root, text="Get Network Info", command=get_network_info)
get_info_button.pack()

root.mainloop()

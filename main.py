import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from webcam_library import WebcamTk

window = tk.Tk()
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
window_width, window_height = 500, 300
bg_color = "white"
style = ttk.Style()
style.theme_use("clam")
window.geometry(f"{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}")
window.minsize(window_width, window_height)
window.title("Webcam")
window.iconbitmap("icons/favicon.ico")  # For Windows Only
window.iconphoto(True, tk.PhotoImage(file="icons/webcam.png"))
window.config(bg=bg_color)

camera = WebcamTk()

style.configure("Text.TLabel", foreground="black", background=bg_color, font=("Arial", int(window_width/50), "bold"))

style.configure("Radio.TRadiobutton", background="#99d8ff", foreground="#000000", font=("Arial", int(window_width/40), "bold"), padding=5)
style.map(
    "Radio.TRadiobutton",
    background=[("selected", "#0008ff"), ("active", "#0467e8"), ("disabled", "#cccccc")],
    foreground=[("selected", "#ffffff"), ("active", "#FFFFFF"), ("disabled", "#000000")])
style.configure("Arrow.TButton", background="#fe8929", foreground="#000000", width=int(window_width/200), borderwidth=0, padding=5)
style.map(
    "Arrow.TButton",
    background=[("pressed", "#0008ff"), ("active", "#ff5e00"), ("disabled", "#cccccc")],
    foreground=[("pressed", "#ffffff"), ("active", "#FFFFFF"), ("disabled", "#000000")])

style.configure("StartButton.TButton", background="#00ff00", foreground="#000000", width=10, font=("Arial", 20, "bold"), borderwidth=0, padding=5)
style.map(
    "StartButton.TButton",
    background=[("pressed", "#005800"), ("active", "#009000"), ("disabled", "#005800")],
    foreground=[("pressed", "#ffffff"), ("active", "#FFFFFF"), ("disabled", "#FFFFFF")])

style.configure("StopButton.TButton", background="#ff0000", foreground="#FFFFFF", width=10, font=("Arial", 20, "bold"), borderwidth=0, padding=5)
style.map(
    "StopButton.TButton",
    background=[("pressed", "#670000"), ("active", "#9c0000"), ("disabled", "#670000")],
    foreground=[("pressed", "#ffffff"), ("active", "#FFFFFF"), ("disabled", "#FFFFFF")])

style.configure("DisabledButton.TButton", width=20, font=("Arial", 15, "bold"), borderwidth=0, padding=5)
style.map(
    "DisabledButton.TButton",
    background=[("disabled", "#cccccc")],
    foreground=[("disabled", "#000000")])

mode_selected = tk.IntVar(value=1)
shape_selected = tk.IntVar(value=1)
size = camera.size
border_radius = camera.corner_radius

showing = False

def change_mode():
    if mode_selected.get() == 1:
        camera.set_flipped(True)
    elif mode_selected.get() == 2:
        camera.set_flipped(False)

def change_shape():
    if shape_selected.get() == 1:
        camera.set_rectangular()
    if shape_selected.get() == 2:
        camera.set_circular()

def change_size(change_size):
    global size
    if (size <= 0.1 and change_size < 0):
        return
    elif (size >= 0.9 and change_size > 0):
        return
    size = round(size + change_size, 1)
    camera.set_size(size)
    size_label.config(text=f"{size:.1f}x")
    if (size <= 0.1):
        size_decrement_button.config(state="disabled")
    else:
        size_decrement_button.config(state="normal")
    if (size >= 0.9):
        size_increament_button.config(state="disabled")
    else:
        size_increament_button.config(state="normal")

def change_border_radius(change_border_radius):
    global border_radius
    if (border_radius <= 0 and change_border_radius < 0):
        return
    elif (border_radius >= 50 and change_border_radius > 0):
        return
    border_radius = border_radius + change_border_radius
    camera.set_border_radius(border_radius)
    border_radius_label.config(text=f"{border_radius}px")
    if (border_radius <= 0):
        border_radius_decrement_button.config(state="disabled")
    else:
        border_radius_decrement_button.config(state="normal")
    if (border_radius >= 50):
        border_radius_increament_button.config(state="disabled")
    else:
        border_radius_increament_button.config(state="normal")

def camera_toggle():
    global showing
    camera_button.config(state="disabled", cursor="arrow")
    showing = not showing
    if showing:
        camera.startWebcam()
        camera_button.config(text="Stop", style="StopButton.TButton")
    else:
        camera.stopWebcam()
        camera_button.config(text="Start", style="StartButton.TButton")
    camera_button.config(state="normal", cursor="hand2")


settings_section = tk.Frame(window, background=bg_color)
settings_section.pack(anchor="center", pady=20)
settings_section.grid_columnconfigure(0, weight=1)

ttk.Label(settings_section, text="Camera Mode", style="Text.TLabel").grid(row=0, column=0, sticky="nsew")
ttk.Label(settings_section, text=":", style="Text.TLabel").grid(row=0, column=1, padx=(5, 20))
mode_frame_options = tk.Frame(settings_section, bg=bg_color, width=250, height=32)
mode_frame_options.grid_propagate(False)
mode_frame_options.grid(row=0, column=2)
mode_frame_options.grid_columnconfigure(0, minsize=100, uniform="group1", weight=1)
mode_frame_options.grid_columnconfigure(1, minsize=100, uniform="group1", weight=1)
ttk.Radiobutton(mode_frame_options, text="Flipped", style="Radio.TRadiobutton", cursor="hand2", variable=mode_selected, value=1, command=change_mode).grid(row=0, column=0, sticky="nsew", padx=(0, 5))
ttk.Radiobutton(mode_frame_options, text="Mirrored", style="Radio.TRadiobutton", cursor="hand2", variable=mode_selected, value=2, command=change_mode).grid(row=0, column=1, sticky="nsew")

ttk.Label(settings_section, text="Camera Shape", style="Text.TLabel").grid(row=1, column=0, sticky="nsew")
ttk.Label(settings_section, text=":", style="Text.TLabel").grid(row=1, column=1, padx=(5, 20))
shape_frame_options = tk.Frame(settings_section, bg=bg_color, width=250, height=32)
shape_frame_options.grid_propagate(False)
shape_frame_options.grid(row=1, column=2, pady=10)
shape_frame_options.grid_columnconfigure(0, minsize=100, uniform="group1", weight=1)
shape_frame_options.grid_columnconfigure(1, minsize=100, uniform="group1", weight=1)
ttk.Radiobutton(shape_frame_options, text="Rectangular", style="Radio.TRadiobutton", cursor="hand2", variable=shape_selected, value=1, command=change_shape).grid(row=0, column=0, sticky="nsew", padx=(0, 5))
ttk.Radiobutton(shape_frame_options, text="Circular", style="Radio.TRadiobutton", cursor="hand2", variable=shape_selected, value=2, command=change_shape).grid(row=0, column=1, sticky="nsew")

ttk.Label(settings_section, text="Camera Size", style="Text.TLabel").grid(row=2, column=0, sticky="nsew")
ttk.Label(settings_section, text=":", style="Text.TLabel").grid(row=2, column=1, padx=(5, 20))
size_change_frame = tk.Frame(settings_section, bg=bg_color)
size_change_frame.grid(row=2, column=2)
size_change_frame.grid_columnconfigure(0, weight=1)
size_decrement_button = ttk.Button(size_change_frame, text="\u25C0", style="Arrow.TButton", cursor="hand2", command=lambda: change_size(-0.1))
size_decrement_button.grid(row=0, column=0)
size_label = ttk.Label(size_change_frame, text=f"{size:.1f}x", width=5, anchor="center", style="Text.TLabel")
size_label.grid(row=0, column=1, padx=10)
size_increament_button = ttk.Button(size_change_frame, text="\u25B6", style="Arrow.TButton", cursor="hand2", command=lambda: change_size(0.1))
size_increament_button.grid(row=0, column=2)

ttk.Label(settings_section, text="Corner Radius", style="Text.TLabel").grid(row=3, column=0, sticky="nsew")
ttk.Label(settings_section, text=":", style="Text.TLabel").grid(row=3, column=1, padx=(5, 20))
border_radius_change_frame = tk.Frame(settings_section, bg=bg_color)
border_radius_change_frame.grid(row=3, column=2)
border_radius_change_frame.grid_columnconfigure(0, weight=1)
border_radius_decrement_button = ttk.Button(border_radius_change_frame, text="\u25C0", style="Arrow.TButton", cursor="hand2", command=lambda: change_border_radius(-1))
border_radius_decrement_button.grid(row=0, column=0)
border_radius_label = ttk.Label(border_radius_change_frame, text=f"{border_radius}px", width=5, anchor="center", style="Text.TLabel")
border_radius_label.grid(row=0, column=1, padx=10)
border_radius_increament_button = ttk.Button(border_radius_change_frame, text="\u25B6", style="Arrow.TButton", cursor="hand2", command=lambda: change_border_radius(1))
border_radius_increament_button.grid(row=0, column=2)

camera_button = ttk.Button(window, text="Start", style="StartButton.TButton", cursor="hand2", command=lambda: threading.Thread(target=camera_toggle, daemon=True).start())
camera_button.pack(anchor="center", pady=(20, 0))

def resize_widget(event):
    if event.widget is not window:
        return
    window_width = event.width
    window_height = event.height
    if (window_width<=window_height):
        style.configure("Text.TLabel", font=("Arial", int(window_width/50), "bold"))
        style.configure("Arrow.TButton", width=int(window_width/200))
    else :
        style.configure("Text.TLabel", font=("Arial", int(window_height/20), "bold"))
        style.configure("Arrow.TButton", width=int(window_height/100))

window.bind("<Configure>", resize_widget)

if not camera.exist:
    messagebox.showerror("Error", "Camera Not Found.")
    camera_button.config(style="DisabledButton.TButton", cursor="arrow", text="Camera Not Found", state="disabled")

window.mainloop()
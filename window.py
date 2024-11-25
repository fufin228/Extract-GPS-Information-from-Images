import tkinter as tk
from tkinter import filedialog
from tkintermapview import TkinterMapView
from PIL import Image, ExifTags, ImageTk, ImageFont
from tkinter import font

marker = None

def extract_exif(file_path):
    img = Image.open(file_path)
    exif_data = img._getexif()

    if exif_data:
        exif = {ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS}
    else:
        exif = {}

    basic_info = {
        "Make": exif.get("Make"),
        "Model": exif.get("Model"),
        "DateTime": exif.get("DateTime"),
        "ExposureTime": exif.get("ExposureTime"),
        "FNumber": exif.get("FNumber"),
    }

    gps_info = ""
    if "GPSInfo" in exif:
        gps_info = gps_info_to_string(exif["GPSInfo"])

    return basic_info, gps_info

def gps_info_to_string(gps_info):
    lat_degrees, lat_minutes, lat_seconds = gps_info[2]
    lat_direction = gps_info[1]

    lon_degrees, lon_minutes, lon_seconds = gps_info[4]
    lon_direction = gps_info[3]

    latitude_str = f"{int(lat_degrees)}°{int(lat_minutes)}'{float(lat_seconds):.2f}\" {lat_direction}"
    longitude_str = f"{int(lon_degrees)}°{int(lon_minutes)}'{float(lon_seconds):.2f}\" {lon_direction}"

    return f"{latitude_str}, {longitude_str}"

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("JPG изображения", "*.jpg;*.jpeg"), ("Все файлы", "*.*"))
    )
    
    if file_path:
        selected_file.set(file_path)
        display_image(file_path)
        show_exif()

def display_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk)
    image_label.image = img_tk

def show_exif():
    file_path = selected_file.get()
    
    if file_path:
        basic_info, gps_info = extract_exif(file_path)
        
        exif_text = "Basic EXIF Information:\n"
        for key, value in basic_info.items():
            if value is not None:
                exif_text += f"{key}: {value}\n"
        
        if gps_info:
            exif_text += f"GPS Information: {gps_info}"
            latitude, longitude = extract_coordinates(gps_info)
            add_marker(latitude, longitude)
        else:
            exif_text += "GPS Information: Not found"
            clear_markers()
        
        data_area.config(text=exif_text)

def extract_coordinates(gps_info):
    gps_parts = gps_info.split(",")
    latitude_str = gps_parts[0].strip()
    longitude_str = gps_parts[1].strip()

    latitude = float(latitude_str.split("°")[0]) + float(latitude_str.split("°")[1].split("'")[0]) / 60 + float(latitude_str.split("'")[1].split("\"")[0]) / 3600
    if "S" in latitude_str:
        latitude = -latitude

    longitude = float(longitude_str.split("°")[0]) + float(longitude_str.split("°")[1].split("'")[0]) / 60 + float(longitude_str.split("'")[1].split("\"")[0]) / 3600
    if "W" in longitude_str:
        longitude = -longitude

    return latitude, longitude

def add_marker(latitude, longitude):
    clear_markers()

    global marker
    marker = map_widget.set_marker(latitude, longitude, text="Photo Location")

    map_widget.set_position(latitude, longitude)
    map_widget.set_zoom(12)

def clear_markers():
    global marker
    if marker:
        map_widget.delete_all_marker()
        marker = None

window = tk.Tk()
window.title("Extract GPS Information from Images")
window_width = 1280
window_height = 720

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = (screen_width - window_width) // 2
center_y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
window.config(bg="black")

map_width = window_width // 2.5
map_height = window_height // 2.5

map_widget = TkinterMapView(window, width=map_width, height=map_height, corner_radius=0, 
                            bg_color="black")

map_widget.place(x=window_width - map_width - 30, y=window_height - map_height - 30)

map_widget.set_position(0.0, 0.0)
map_widget.set_zoom(2)

selected_file = tk.StringVar()

image_frame = tk.Frame(window, bg="green", bd=3)
image_frame.place(x=window_width // 4 - 150, y=(window_height - 300) // 2, width=320, height=320)

image_label = tk.Label(image_frame, bg="black")
image_label.pack(fill="both", expand=True)

data_area_width = map_width
data_area_height = map_height

data_area_frame = tk.Frame(window, bg="green", bd=3)
data_area_frame.place(x=window_width - map_width - 30, y=window_height - map_height - data_area_height - 80, 
                    width=map_width, height=map_height)

data_area = tk.Label(data_area_frame, bg="black", fg="white", font=("Arial", 14))
data_area.pack(fill="both", expand=True)

custom_font = font.Font(family="Helvetica", size=24, weight="bold")

title_label = tk.Label(window, text="GPS Information from Images", bg="black", fg="white", font=custom_font)
title_label.place(x=105, y=90)

button_width = 12

file_button = tk.Button(window, text="Select file", command=select_file, width=button_width)
file_button.place(x=275, y=window_height - 150)

window.mainloop()

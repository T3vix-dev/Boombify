#import all necessary libraries
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
# App setup
ctk.set_appearance_mode("dark") # Dark mode for modern look
ctk.set_default_color_theme("green")#Spotify-like green
app= ctk.CTk()
app.title("Boombify🎵")
app.geometry("1100*650")

# Bottom Player Bar

bottom_bar = ctk.CTKFrame(app, height=80)
bottom_bar.pack(side"bottom", fill="x")
play_button = ctk.CTKButton(bottom_bar, text="▶ Play", width=100)
pause_buttton =ctk.CTKButton(bottom_bar, text="⏸ Pause", width=100)
play_button.pack(side="left", padx=20, pady=20)
pause_button.pack(side="left", padx=10, pady=20)
bass_button.pack(side="right", padx=20, pady=20)

#Placeholder for song list
song_frame=ctk.CTKScrollableFrame(main_frame,label_text="All Songs")
song_frame.pack(fill="both",expand=True,padx=10,pady=10)

#Example song buttons
for i in range(1,11):
    ctkCTKButton(song_frame,text=f"Song{i}-Artist{i}",corner_radius=8).pack(pady=5,fill="x")


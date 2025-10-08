#import all necessary libraries
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import os 

#Initialize pygame mixer
pygame.mixer.init()

# App setup
ctk.set_appearance_mode("dark") # Dark mode for modern look
ctk.set_default_color_theme("green")#Spotify-like green
app = ctk.CTk()
app.title("Boombify🎵")
app.geometry("1100*650")

# Functionality
    def load_songs():
    """Load songs from 'songs' folder."""
    songs = []
    music_folder = "songs"
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)
    for file in os.listdir(music_folder):
        if file.endswith(".mp3"):
            songs.append(file)
    return songs

def play_song(song_name=None):
    """Play selected song."""
    global current_song, is_paused
    try:
        if song_name:
            song_path = os.path.join("songs", song_name)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            current_song = song_name
            is_paused = False
            now_playing_label.configure(text=f"🎵 Now Playing: {song_name}")
            update_album_art(song_name)
        elif is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
    except Exception as e:
        print(f"Error playing song: {e}")

def pause_song():
    """Pause current song."""
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def stop_song():
    """Stop playback."""
    pygame.mixer.music.stop()
    now_playing_label.configure(text="🎵 Now Playing: None")

def set_volume(value):
    """Adjust volume."""
    volume = float(value)
    pygame.mixer.music.set_volume(volume)

def update_album_art(song_name):
    """Display album art (placeholder for now)."""
    try:
        img = Image.open("album_placeholder.png")  # Add your own image file
    except:
        img = Image.new("RGB", (200, 200), color="gray")
    img = img.resize((180, 180))
    photo = ImageTk.PhotoImage(img)
    album_art_label.configure(image=photo)
    album_art_label.image = photo


# Sidebar
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(sidebar, text="🎧 Boombify", font=ctk.CTkFont(size=22, weight="bold"))
logo_label.pack(pady=(30, 20))

buttons = ["Home", "Playlists", "Genres", "Mood", "Settings"]
for btn in buttons:
    b = ctk.CTkButton(sidebar, text=btn, width=160, corner_radius=10)
    b.pack(pady=10)



#Topbar (Search) 
topbar = ctk.CTkFrame(app, height=60)
topbar.pack(side="top", fill="x")

search_entry = ctk.CTkEntry(topbar, placeholder_text="Search artist or genre...", width=400)
search_entry.pack(side="left", padx=20, pady=10)

search_button = ctk.CTkButton(topbar, text="Search", width=100)
search_button.pack(side="left", padx=10)

# Main content
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

song_list_label = ctk.CTkLabel(main_frame, text="🎵 Your Songs", font=ctk.CTkFont(size=18, weight="bold"))
song_list_label.pack(anchor="w", pady=10, padx=10)

song_frame = ctk.CTkScrollableFrame(main_frame, label_text="All Songs")
song_frame.pack(fill="both", expand=True, padx=10, pady=10)

songs = load_songs()
for song in songs:
    song_button = ctk.CTkButton(song_frame, text=song, corner_radius=8,
                                command=lambda s=song: play_song(s))
    song_button.pack(pady=5, fill="x")

    # Bottom Player bar
    bottom_bar = ctk.CTkFrame(app, height=80)
bottom_bar.pack(side="bottom", fill="x")

play_button = ctk.CTkButton(bottom_bar, text="▶ Play", width=100, command=lambda: play_song(current_song))
pause_button = ctk.CTkButton(bottom_bar, text="⏸ Pause", width=100, command=pause_song)
stop_button = ctk.CTkButton(bottom_bar, text="⏹ Stop", width=100, command=stop_song)

play_button.pack(side="left", padx=20, pady=20)
pause_button.pack(side="left", padx=10, pady=20)
stop_button.pack(side="left", padx=10, pady=20)

now_playing_label = ctk.CTkLabel(bottom_bar, text="Now Playing: None", font=ctk.CTkFont(size=14))
now_playing_label.pack(side="right", padx=20)

# Run app
app.mainloop()


    

      

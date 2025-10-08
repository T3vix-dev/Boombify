#import all necessary libraries
import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk

# App setup
ctk.set_appearance_mode("dark") # Dark mode for modern look
ctk.set_default_color_theme("green")#Spotify-like green
app = ctk.CTk()
app.title("Boombify🎵")
app.geometry("1100*650")

# Sidebar
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(sidebar, text="🎧 Boombify", font=ctk.CTkFont(size=20, weight="bold"))
logo_label.pack(pady=(30, 20))

# Sidebar buttons
buttons = ["Home", "Playlists", "Genres", "Mood", "Settings"]
for btn in buttons:
    ctk.CTkButton(sidebar, text=btn, width=160, corner_radius=10).pack(pady=10)



#Topbar (Search) 
topbar = ctk.CTkFrame(app, height=60)
topbar.pack(side="top", fill="x")

search_entry = ctk.CTkEntry(topbar, placeholder_text="Search artist or genre...", width=400)
search_entry.pack(side="left", padx=20, pady=10)

search_button = ctk.CTkButton(topbar, text="Search", width=100)
search_button.pack(side="left", padx=10)
#Functionality
def load_songs():
    """Load songs from 'songs' folder."""
    songs =[]
    music_folder ="songs"
    if not
    os.path.exists(music_folder):
        os.makedirs(music_folder)
        for life in os.listdir(music_folder):
            if file.endswith(".mp3"):
                songs.append(file)
                return songs

# Main content
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

song_list_label = ctk.CTkLabel(main_frame, text="🎵 Trending Songs", font=ctk.CTkFont(size=18, weight="bold"))
song_list_label.pack(anchor="w", pady=10, padx=10)

#Placeholder for song list
song_frame = ctk.CTkScrollableFrame(main_frame,label_text="All Songs")
song_frame.pack(fill="both", expand=True, padx=10 ,pady=10)

#Example song buttons
for i in range(1,11):
    ctk.CTKButton(song_frame, text=f"Song {i} -Artist {i} ", corner_radius=8).pack(pady=5, fill="x")

# Bottom Player Bar

bottom_bar = ctk.CTkFrame(app, height=80)
bottom_bar.pack(side"bottom", fill="x")
play_button = ctk.CTkButton(bottom_bar, text="▶ Play", width=100)
pause_buttton = ctk.CTkButton(bottom_bar, text="⏸ Pause", width=100)
play_button.pack(side="left", padx=20, pady=20)
pause_button.pack(side="left", padx=10, pady=20)
bass_button.pack(side="right", padx=20, pady=20)

# Run App
app.mainloop()

def pause_song():
    """Pause current song."""
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True


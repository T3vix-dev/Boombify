#import all necesarry libraries

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pygame
import os
import json

# ---------------------- Setup ---------------------- #
pygame.mixer.init()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Boombify 🎧")
app.geometry("1150x700")
app.minsize(950, 600)

# ---------------------- Data Stores ---------------------- #
# Define your songs folder path here 👇
SONG_FOLDER = r"C:\Users\tevin\OneDrive\Documents\songs"

playlist = []
for file in os.listdir(SONG_FOLDER):
    if file.endswith(".mp3"):
        playlist.append(os.path.join(SONG_FOLDER, file))


song_genres = {}              # path -> genre string
playlists = {}                # "Playlist Name" -> [paths]
settings = {
    "theme": "dark",
    "volume": 0.8
}
SETTINGS_FILE = "boombify_settings.json"

# Predefined genres
GENRES = ["Afrobeat", "Pop", "Hip-Hop", "RnB", "Reggae", "Gospel",
          "Country", "Rock", "Jazz", "Amapiano", "EDM", "Classical"]

# ---------------------- Helpers ---------------------- #
def load_settings():
    global settings
    try:
        with open(SETTINGS_FILE, "r") as f:
            s = json.load(f)
            settings.update(s)
    except FileNotFoundError:
        pass
    except Exception:
        pass
    # apply theme & volume
    appearance = settings.get("theme", "dark")
    if appearance in ("dark", "light", "system"):
        ctk.set_appearance_mode(appearance)
    pygame.mixer.music.set_volume(settings.get("volume", 0.8))

def save_settings():
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
        status_label.configure(text="Settings saved ✅")
    except Exception as e:
        messagebox.showerror("Save Settings", f"Could not save settings: {e}")

def auto_assign_genre_by_filename(path):
    """Try to guess a genre by looking for a keyword in filename."""
    name = os.path.basename(path).lower()
    for g in GENRES:
        if g.lower() in name:
            song_genres[path] = g
            return g
    # no guess
    return None

def refresh_home_listbox():
    home_listbox.delete(0, tk.END)
    for p in playlist:
        display = os.path.basename(p)
        genre = song_genres.get(p)
        if genre:
            display += f"   [{genre}]"
        home_listbox.insert(tk.END, display)

def refresh_genre_song_list(selected_genre=None):
    genre_listbox.delete(0, tk.END)
    songs_listbox_genre.delete(0, tk.END)
    # populate genres listbox
    for g in GENRES:
        genre_listbox.insert(tk.END, g)
    if selected_genre:
        # populate songs for that genre
        for p in playlist:
            if song_genres.get(p, "").lower() == selected_genre.lower():
                songs_listbox_genre.insert(tk.END, os.path.basename(p))

def refresh_playlists_listbox():
    playlists_listbox.delete(0, tk.END)
    for name in playlists.keys():
        playlists_listbox.insert(tk.END, name)

def refresh_playlist_contents_view(selected_playlist):
    playlist_contents_box.delete(0, tk.END)
    for p in playlists.get(selected_playlist, []):
        playlist_contents_box.insert(tk.END, os.path.basename(p))

def get_selected_home_path():
    sel = home_listbox.curselection()
    if not sel:
        return None
    idx = sel[0]
    if idx < len(playlist):
        return playlist[idx]
    return None

def get_selected_genre():
    sel = genre_listbox.curselection()
    return genre_listbox.get(sel) if sel else None

def get_selected_genre_song_path():
    sel = songs_listbox_genre.curselection()
    if not sel:
        return None
    filename = songs_listbox_genre.get(sel)
    # find path by basename
    for p in playlist:
        if os.path.basename(p) == filename:
            return p
    return None

def get_selected_playlist_name():
    sel = playlists_listbox.curselection()
    return playlists_listbox.get(sel) if sel else None

def get_selected_playlist_content_path():
    sel = playlist_contents_box.curselection()
    if not sel:
        return None
    filename = playlist_contents_box.get(sel)
    for p in playlist:
        if os.path.basename(p) == filename:
            return p
    return None

# ---------------------- Audio Controls ---------------------- #
current_song = None
paused = False
bass_boost_enabled = False

def add_songs():
    files = filedialog.askopenfilenames(title="Select Songs",
                                        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.m4a")])
    added = 0
    for f in files:
        if f not in playlist:
            playlist.append(f)
            # try auto-genre
            auto_assign_genre_by_filename(f)
            added += 1
    refresh_home_listbox()
    refresh_genre_song_list()
    status_label.configure(text=f"Added {added} file(s)")

def play_song_from_home(event=None):
    global current_song, paused
    path = get_selected_home_path()
    if not path:
        messagebox.showinfo("Play", "Select a song in Home playlist.")
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        current_song = path
        paused = False
        status_label.configure(text=f"▶ Now playing: {os.path.basename(path)}")
    except Exception as e:
        messagebox.showerror("Play Error", f"Could not play file: {e}")

def pause_song():
    global paused
    try:
        pygame.mixer.music.pause()
        paused = True
        status_label.configure(text="⏸ Paused")
    except:
        pass

def stop_song():
    global paused
    try:
        pygame.mixer.music.stop()
        paused = False
        status_label.configure(text="⏹ Stopped")
    except:
        pass

def toggle_bass_switch():
    global bass_boost_enabled
    bass_boost_enabled = bass_switch.get()
    status_label.configure(text=f"🎚 Bass Boost {'ON' if bass_boost_enabled else 'OFF'}")
    # NOTE: actual DSP can be added later; this currently toggles state only.

def search_song_topbar():
    q = top_search_entry.get().strip().lower()
    if not q:
        refresh_home_listbox()
        return
    home_listbox.delete(0, tk.END)
    for p in playlist:
        if q in os.path.basename(p).lower():
            display = os.path.basename(p)
            genre = song_genres.get(p)
            if genre:
                display += f"   [{genre}]"
            home_listbox.insert(tk.END, display)

# ---------------------- Genres View Actions ---------------------- #
def on_genre_selected(event=None):
    sel = genre_listbox.curselection()
    if not sel:
        return
    genre = genre_listbox.get(sel)
    songs_listbox_genre.delete(0, tk.END)
    for p in playlist:
        if song_genres.get(p, "").lower() == genre.lower():
            songs_listbox_genre.insert(tk.END, os.path.basename(p))

def assign_genre_to_selected_song():
    # Assign selected genre from dropdown to the selected song in home list
    path = get_selected_home_path()
    if not path:
        messagebox.showinfo("Assign Genre", "Select a song in Home to assign a genre.")
        return
    # pick via simple dialog (choice)
    genre = simpledialog.askstring("Assign Genre", f"Enter genre for {os.path.basename(path)}:\nOptions: {', '.join(GENRES)}")
    if genre:
        song_genres[path] = genre
        refresh_home_listbox()
        refresh_genre_song_list()
        status_label.configure(text=f"Assigned genre '{genre}' to {os.path.basename(path)}")

# ---------------------- Playlists View Actions ---------------------- #
def create_playlist_prompt():
    name = simpledialog.askstring("Create Playlist", "Enter playlist name:")
    if not name:
        return
    if name in playlists:
        messagebox.showinfo("Create Playlist", "A playlist with that name already exists.")
        return
    playlists[name] = []
    refresh_playlists_listbox()
    status_label.configure(text=f"Playlist '{name}' created")

def delete_selected_playlist():
    name = get_selected_playlist_name()
    if not name:
        messagebox.showinfo("Playlists", "Select a playlist first.")
        return
    if messagebox.askyesno("Delete Playlist", f"Delete playlist '{name}'?"):
        playlists.pop(name, None)
        refresh_playlists_listbox()
        playlist_contents_box.delete(0, tk.END)
        status_label.configure(text=f"Playlist '{name}' deleted")

def add_selected_home_to_playlist():
    name = get_selected_playlist_name()
    if not name:
        messagebox.showinfo("Playlists", "Select a playlist to add songs to.")
        return
    path = get_selected_home_path()
    if not path:
        messagebox.showinfo("Playlists", "Select a song in Home to add.")
        return
    if path in playlists[name]:
        messagebox.showinfo("Playlists", "Song already in playlist.")
        return
    playlists[name].append(path)
    refresh_playlist_contents_view(name)
    status_label.configure(text=f"Added {os.path.basename(path)} to '{name}'")

def remove_selected_from_playlist():
    name = get_selected_playlist_name()
    if not name:
        messagebox.showinfo("Playlists", "Select a playlist first.")
        return
    path = get_selected_playlist_content_path()
    if not path:
        messagebox.showinfo("Playlists", "Select a song inside playlist to remove.")
        return
    try:
        playlists[name].remove(path)
        refresh_playlist_contents_view(name)
        status_label.configure(text=f"Removed {os.path.basename(path)} from '{name}'")
    except ValueError:
        pass

def play_selected_from_playlist_contents(event=None):
    path = get_selected_playlist_content_path()
    if not path:
        messagebox.showinfo("Playlists", "Select a song in playlist contents.")
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        status_label.configure(text=f"▶ Playing: {os.path.basename(path)}")
    except Exception as e:
        messagebox.showerror("Play Error", str(e))

def on_playlist_selected(event=None):
    name = get_selected_playlist_name()
    if not name:
        return
    refresh_playlist_contents_view(name)

# ---------------------- Mood View ---------------------- #
mood_songs = {
    "happy": ["Dance Again – Jennifer Lopez", "Happy – Pharrell Williams", "Good Life – Kanye West"],
    "sad": ["Someone Like You – Adele", "Let Her Go – Passenger", "Fix You – Coldplay"],
    "energetic": ["Stronger – Kanye West", "Can’t Hold Us – Macklemore", "Thunderstruck – AC/DC"],
    "chill": ["Sunflower – Post Malone", "Location – Khalid", "Let’s Chill – Guy"],
    "romantic": ["Perfect – Ed Sheeran", "All of Me – John Legend", "My Love – Justin Timberlake"]
}

def analyze_mood_user_input():
    mood = mood_entry.get().strip().lower()
    for w in mood_song_frame.winfo_children():
        w.destroy()
    if mood in mood_songs:
        ctk.CTkLabel(mood_song_frame, text=f"🎧 Songs for '{mood}' mood:",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        for s in mood_songs[mood]:
            ctk.CTkButton(mood_song_frame, text=s, corner_radius=8).pack(pady=4, fill="x")
    else:
        messagebox.showinfo("Mood Analyzer", "Try: happy, sad, energetic, chill, romantic.")

# ---------------------- Settings Actions ---------------------- #
def set_theme(value):
    # value expected: "dark" / "light" / "system"
    settings["theme"] = value
    ctk.set_appearance_mode(value)
    status_label.configure(text=f"Theme: {value}")

def set_volume(val):
    try:
        v = float(val)
        settings["volume"] = v
        pygame.mixer.music.set_volume(v)
        status_label.configure(text=f"Volume: {int(v*100)}%")
    except:
        pass

# ---------------------- Views (Frames) ---------------------- #
# Sidebar
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(sidebar, text="🎵 Boombify", font=ctk.CTkFont(size=22, weight="bold"))
logo_label.pack(pady=(18, 10))

# Buttons with linked views
btn_home = ctk.CTkButton(sidebar, text="Home", width=160, command=lambda: show_view("home"))
btn_home.pack(pady=6)
btn_playlists = ctk.CTkButton(sidebar, text="Playlists", width=160, command=lambda: show_view("playlists"))
btn_playlists.pack(pady=6)
btn_genres = ctk.CTkButton(sidebar, text="Genres", width=160, command=lambda: show_view("genres"))
btn_genres.pack(pady=6)
btn_mood = ctk.CTkButton(sidebar, text="Mood", width=160, command=lambda: show_view("mood"))
btn_mood.pack(pady=6)
btn_settings = ctk.CTkButton(sidebar, text="Settings", width=160, command=lambda: show_view("settings"))
btn_settings.pack(pady=6)

# Topbar
topbar = ctk.CTkFrame(app, height=60)
topbar.pack(side="top", fill="x")
top_search_entry = ctk.CTkEntry(topbar, placeholder_text="Search songs...", width=420)
top_search_entry.pack(side="left", padx=16, pady=10)
top_search_btn = ctk.CTkButton(topbar, text="Search", command=search_song_topbar)
top_search_btn.pack(side="left", padx=8)
add_button = ctk.CTkButton(topbar, text="➕ Add Songs", command=add_songs)
add_button.pack(side="right", padx=16)

# Main content area (we swap frames here)
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=12, pady=12)

# --- Home Frame ---
home_frame = ctk.CTkFrame(main_frame)
home_header = ctk.CTkLabel(home_frame, text="🎶 Playlist", font=ctk.CTkFont(size=18, weight="bold"))
home_header.pack(anchor="nw", pady=(6,8))

# listbox for home playlist
home_listbox_frame = ctk.CTkFrame(home_frame)
home_listbox_frame.pack(fill="both", expand=True)
home_scroll = ctk.CTkScrollbar(home_listbox_frame, orientation="vertical")
home_scroll.pack(side="right", fill="y", padx=(0,6))
home_listbox = tk.Listbox(home_listbox_frame, bg="#111", fg="#fff", selectbackground="#1DB954", font=("Arial", 12))
home_listbox.pack(side="left", fill="both", expand=True)
home_listbox.config(yscrollcommand=lambda f,l: home_scroll.set(f,l))
home_scroll.configure(command=home_listbox.yview)

home_listbox.bind("<Double-Button-1>", play_song_from_home)

# Playback controls
controls = ctk.CTkFrame(home_frame)
controls.pack(pady=8)
ctk.CTkButton(controls, text="▶ Play", width=100, command=play_song_from_home).grid(row=0, column=0, padx=6)
ctk.CTkButton(controls, text="⏸ Pause", width=100, command=pause_song).grid(row=0, column=1, padx=6)
ctk.CTkButton(controls, text="⏹ Stop", width=100, command=stop_song).grid(row=0, column=2, padx=6)
bass_switch = ctk.CTkSwitch(controls, text="Bass Boost", command=toggle_bass_switch)
bass_switch.grid(row=0, column=3, padx=16)

assign_genre_btn = ctk.CTkButton(controls, text="Assign Genre", command=assign_genre_to_selected_song)
assign_genre_btn.grid(row=0, column=4, padx=6)

# --- Genres Frame ---
genres_frame = ctk.CTkFrame(main_frame)
g_header = ctk.CTkLabel(genres_frame, text="🎷 Genres", font=ctk.CTkFont(size=18, weight="bold"))
g_header.pack(anchor="nw", pady=(6,8))

genres_content = ctk.CTkFrame(genres_frame)
genres_content.pack(fill="both", expand=True, pady=8)

left_genres = ctk.CTkFrame(genres_content, width=220)
left_genres.pack(side="left", fill="y", padx=(0,8), pady=6)
genre_listbox = tk.Listbox(left_genres, height=20, bg="#111", fg="#fff", selectbackground="#1DB954", font=("Arial", 12))
genre_listbox.pack(fill="both", expand=True)
genre_listbox.bind("<<ListboxSelect>>", on_genre_selected)

right_songs = ctk.CTkFrame(genres_content)
right_songs.pack(side="left", fill="both", expand=True)
ctk.CTkLabel(right_songs, text="Songs in Genre", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", pady=(0,8))
songs_listbox_genre = tk.Listbox(right_songs, bg="#111", fg="#fff", selectbackground="#1DB954", font=("Arial", 12))
songs_listbox_genre.pack(fill="both", expand=True, padx=(0,6))
ctk.CTkButton(genres_frame, text="Refresh Genres", command=lambda: refresh_genre_song_list()).pack(pady=6)

# --- Playlists Frame ---
playlists_frame = ctk.CTkFrame(main_frame)
pl_header = ctk.CTkLabel(playlists_frame, text="📁 Playlists", font=ctk.CTkFont(size=18, weight="bold"))
pl_header.pack(anchor="nw", pady=(6,8))

playlists_content = ctk.CTkFrame(playlists_frame)
playlists_content.pack(fill="both", expand=True)

left_pl = ctk.CTkFrame(playlists_content, width=260)
left_pl.pack(side="left", fill="y", padx=(0,8))
ctk.CTkLabel(left_pl, text="Your Playlists", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", pady=(6,6))
playlists_listbox = tk.Listbox(left_pl, bg="#111", fg="#fff", selectbackground="#1DB954", height=12)
playlists_listbox.pack(fill="both", expand=True, padx=6)
playlists_listbox.bind("<<ListboxSelect>>", on_playlist_selected)

pl_buttons = ctk.CTkFrame(left_pl)
pl_buttons.pack(pady=8)
ctk.CTkButton(pl_buttons, text="Create", command=create_playlist_prompt).grid(row=0, column=0, padx=6)
ctk.CTkButton(pl_buttons, text="Delete", command=delete_selected_playlist).grid(row=0, column=1, padx=6)
ctk.CTkButton(pl_buttons, text="Add Selected Song", command=add_selected_home_to_playlist).grid(row=1, column=0, columnspan=2, pady=6)

right_pl = ctk.CTkFrame(playlists_content)
right_pl.pack(side="left", fill="both", expand=True)
ctk.CTkLabel(right_pl, text="Playlist Contents", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", pady=(6,6))
playlist_contents_box = tk.Listbox(right_pl, bg="#111", fg="#fff", selectbackground="#1DB954")
playlist_contents_box.pack(fill="both", expand=True, padx=6)
playlist_contents_box.bind("<Double-Button-1>", play_selected_from_playlist_contents)
pl_right_buttons = ctk.CTkFrame(right_pl)
pl_right_buttons.pack(pady=8)
ctk.CTkButton(pl_right_buttons, text="Remove Selected", command=remove_selected_from_playlist).grid(row=0, column=0, padx=6)

# --- Mood Frame ---
mood_frame = ctk.CTkFrame(main_frame)
m_header = ctk.CTkLabel(mood_frame, text="💭 Mood Analyzer", font=ctk.CTkFont(size=18, weight="bold"))
m_header.pack(anchor="nw", pady=(6,8))
ctk.CTkLabel(mood_frame, text="How are you feeling today?", font=ctk.CTkFont(size=14)).pack(pady=(6,4))
mood_entry = ctk.CTkEntry(mood_frame, placeholder_text="Type mood (e.g., happy, sad, chill)...", width=420)
mood_entry.pack()
ctk.CTkButton(mood_frame, text="Analyze Mood 🎶", command=analyze_mood_user_input).pack(pady=8)
mood_song_frame = ctk.CTkScrollableFrame(mood_frame, label_text="Suggested Songs")
mood_song_frame.pack(fill="both", expand=True, padx=8, pady=6)

# --- Settings Frame ---
settings_frame = ctk.CTkFrame(main_frame)
s_header = ctk.CTkLabel(settings_frame, text="⚙ Settings", font=ctk.CTkFont(size=18, weight="bold"))
s_header.pack(anchor="nw", pady=(6,8))

ctk.CTkLabel(settings_frame, text="Appearance").pack(anchor="nw", padx=8, pady=(6,4))
appearance_menu = ctk.CTkOptionMenu(settings_frame, values=["dark", "light", "system"],
                                    command=set_theme)
appearance_menu.set(settings.get("theme", "dark"))
appearance_menu.pack(anchor="nw", padx=8)

ctk.CTkLabel(settings_frame, text="Volume").pack(anchor="nw", padx=8, pady=(8,4))
volume_slider = ctk.CTkSlider(settings_frame, from_=0.0, to=1.0, number_of_steps=100, command=set_volume)
volume_slider.set(settings.get("volume", 0.8))
volume_slider.pack(anchor="nw", padx=8, pady=(0,20))
ctk.CTkButton(settings_frame, text="Save Settings", command=save_settings).pack(padx=8)

ctk.CTkLabel(settings_frame, text=f"Version: 1.0").pack(anchor="se", side="bottom", padx=8, pady=12)

# Status bar
status_label = ctk.CTkLabel(app, text="Welcome to Boombify 🎧", anchor="w")
status_label.pack(side="bottom", fill="x", pady=5, padx=10)

# ---------------------- View Controller ---------------------- #
frames = {
    "home": home_frame,
    "genres": genres_frame,
    "playlists": playlists_frame,
    "mood": mood_frame,
    "settings": settings_frame
}

def hide_all_frames():
    for f in frames.values():
        f.pack_forget()

def show_view(name):
    hide_all_frames()
    frame = frames.get(name)
    if not frame:
        return
    frame.pack(fill="both", expand=True)
    # do per-view refresh actions
    if name == "home":
        refresh_home_listbox()
    elif name == "genres":
        refresh_genre_song_list()
    elif name == "playlists":
        refresh_playlists_listbox()
    elif name == "mood":
        # nothing special
        pass
    elif name == "settings":
        appearance_menu.set(settings.get("theme", "dark"))
        volume_slider.set(settings.get("volume", 0.8))

# default view
load_settings()
show_view("home")

# ---------------------- Bindings & Start ---------------------- #
# keyboard shortcuts
app.bind("<space>", lambda e: play_song_from_home())
app.bind("<Control-p>", lambda e: add_songs())

app.mainloop()

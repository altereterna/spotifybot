import tkinter as tk
from tkinter import messagebox
import os

def load_credentials():
    credentials = {}
    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as file:
            for line in file:
                if ' = ' in line:
                    key, value = line.strip().split(' = ', 1)
                    credentials[key] = value
    return credentials

def save_credentials():
    with open('credentials.txt', 'w') as file:
        file.write(f"SPOTIPY_CLIENT_ID = {spotify_client_id.get()}\n")
        file.write(f"SPOTIPY_CLIENT_SECRET = {spotify_client_secret.get()}\n")
        file.write(f"SPOTIPY_REDIRECT_URI = {spotify_redirect_uri.get()}\n")
        file.write(f"TWITCH_BOT_TOKEN = {twitch_bot_token.get()}\n")
        file.write(f"TWITCH_BOT_PREFIX = {twitch_bot_prefix.get()}\n")
        file.write(f"TWITCH_CHANNEL = {twitch_channel.get()}\n")
    messagebox.showinfo("Info", "Credentials saved successfully!")

def run_bot():
    save_credentials()
    root.destroy()
    os.system('python spoti.py')

def show_credits():
    messagebox.showinfo("Credits", "Made by @altereterna (altereterna@proton.me) and her AI, Ness")

credentials = load_credentials()

root = tk.Tk()
root.title("ness_spotifybot Configuration")

root.iconbitmap('icon.ico')  

font_label = ('Helvetica', 12)
font_entry = ('Helvetica', 12)
bg_color = '#f0f0f0'
entry_bg_color = '#e0e0e0'
entry_active_bg_color = '#ffffff'
fg_color = '#333333'
placeholder_color = '#999999'

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg=fg_color, bg=entry_active_bg_color)

def on_focus_out(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg=placeholder_color, bg=entry_bg_color)

# Spotipy Client ID
label_spotify_client_id = tk.Label(root, text="Spotify Client ID:", font=font_label)
label_spotify_client_id.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
spotify_client_id = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color)
spotify_client_id.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
spotify_client_id.insert(0, credentials.get('SPOTIPY_CLIENT_ID', 'Enter Spotify Client ID'))
spotify_client_id.bind('<FocusIn>', lambda event: on_entry_click(event, spotify_client_id, 'Enter Spotify Client ID'))
spotify_client_id.bind('<FocusOut>', lambda event: on_focus_out(event, spotify_client_id, 'Enter Spotify Client ID'))

# Spotify Client Secret
label_spotify_client_secret = tk.Label(root, text="Spotify Client Secret:", font=font_label)
label_spotify_client_secret.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
spotify_client_secret = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color, show='*')
spotify_client_secret.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
spotify_client_secret.insert(0, credentials.get('SPOTIPY_CLIENT_SECRET', 'Enter Spotify Client Secret'))
spotify_client_secret.bind('<FocusIn>', lambda event: on_entry_click(event, spotify_client_secret, 'Enter Spotify Client Secret'))
spotify_client_secret.bind('<FocusOut>', lambda event: on_focus_out(event, spotify_client_secret, 'Enter Spotify Client Secret'))

# Spotify Redirect URI
label_spotify_redirect_uri = tk.Label(root, text="Spotify Redirect URI:", font=font_label)
label_spotify_redirect_uri.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
spotify_redirect_uri = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color)
spotify_redirect_uri.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)
spotify_redirect_uri.insert(0, credentials.get('SPOTIPY_REDIRECT_URI', 'Enter Spotify Redirect URI'))
spotify_redirect_uri.bind('<FocusIn>', lambda event: on_entry_click(event, spotify_redirect_uri, 'Enter Spotify Redirect URI'))
spotify_redirect_uri.bind('<FocusOut>', lambda event: on_focus_out(event, spotify_redirect_uri, 'Enter Spotify Redirect URI'))

# Twitch Bot Token
label_twitch_bot_token = tk.Label(root, text="Twitch Bot Token:", font=font_label)
label_twitch_bot_token.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
twitch_bot_token = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color, show='*')
twitch_bot_token.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)
twitch_bot_token.insert(0, credentials.get('TWITCH_BOT_TOKEN', 'Enter Twitch Bot Token'))
twitch_bot_token.bind('<FocusIn>', lambda event: on_entry_click(event, twitch_bot_token, 'Enter Twitch Bot Token'))
twitch_bot_token.bind('<FocusOut>', lambda event: on_focus_out(event, twitch_bot_token, 'Enter Twitch Bot Token'))

# Twitch Bot Prefix
label_twitch_bot_prefix = tk.Label(root, text="Twitch Bot Prefix:", font=font_label)
label_twitch_bot_prefix.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
twitch_bot_prefix = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color)
twitch_bot_prefix.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)
twitch_bot_prefix.insert(0, credentials.get('TWITCH_BOT_PREFIX', 'Enter Twitch Bot Prefix'))
twitch_bot_prefix.bind('<FocusIn>', lambda event: on_entry_click(event, twitch_bot_prefix, 'Enter Twitch Bot Prefix'))
twitch_bot_prefix.bind('<FocusOut>', lambda event: on_focus_out(event, twitch_bot_prefix, 'Enter Twitch Bot Prefix'))

# Twitch Channel
label_twitch_channel = tk.Label(root, text="Twitch Channel:", font=font_label)
label_twitch_channel.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
twitch_channel = tk.Entry(root, font=font_entry, bg=entry_bg_color, fg=placeholder_color)
twitch_channel.grid(row=5, column=1, padx=10, pady=5, sticky=tk.EW)
twitch_channel.insert(0, credentials.get('TWITCH_CHANNEL', 'Enter Twitch Channel'))
twitch_channel.bind('<FocusIn>', lambda event: on_entry_click(event, twitch_channel, 'Enter Twitch Channel'))
twitch_channel.bind('<FocusOut>', lambda event: on_focus_out(event, twitch_channel, 'Enter Twitch Channel'))

button_save = tk.Button(root, text="💾 Save", font=font_label, command=save_credentials)
button_save.grid(row=6, column=0, padx=10, pady=10, sticky=tk.EW)

button_run = tk.Button(root, text="▶️ Run", font=font_label, command=run_bot)
button_run.grid(row=6, column=1, padx=10, pady=10, sticky=tk.EW)

button_credits = tk.Button(root, text="❓", font=font_label, command=show_credits)
button_credits.grid(row=6, column=2, padx=10, pady=10, sticky=tk.EW)

root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.mainloop()

import re
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
import requests.exceptions
import logging
from datetime import datetime
import psutil
import sys

logging.basicConfig(level=logging.INFO)

def load_credentials():
    credentials = {}
    with open('credentials.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            credentials[key] = value
    return credentials

credentials = load_credentials()

SPOTIPY_CLIENT_ID = credentials.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = credentials.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = credentials.get('SPOTIPY_REDIRECT_URI')
TWITCH_BOT_TOKEN = credentials.get('TWITCH_BOT_TOKEN')
TWITCH_BOT_PREFIX = credentials.get('TWITCH_BOT_PREFIX')
TWITCH_CHANNEL = credentials.get('TWITCH_CHANNEL')

PROGRAM_NAME = "ness_spotifybot for twitch made by eterna @altereterna & her ness <3"

MIN_VOLUME = 30
MAX_VOLUME = 50

scope = "user-modify-playback-state,user-read-playback-state"
spotify_auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=scope)
sp = spotipy.Spotify(auth_manager=spotify_auth_manager, requests_timeout=30)  # Set a 30-second timeout

def load_allowed_users():
    try:
        with open('exceptions.txt', 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        print("exceptions.txt file not found. No users will be allowed.")
        return set()

allowed_users = load_allowed_users()

def retry_on_timeout(max_retries=3):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, spotipy.exceptions.SpotifyException) as e:
                    retries += 1
                    elapsed_time = datetime.now() - start_time
                    if retries >= max_retries:
                        print(f"Error in {func.__name__}: {str(e)}. Retried {retries} times.")
                        break
                    else:
                        print(f"Error in {func.__name__} on attempt {retries}: {str(e)}. Retrying...")
                        await asyncio.sleep(2 ** retries)  # Exponential backoff
                except Exception as e:
                    if "object Channel can't be used in 'await' expression" in str(e):
                        # Ignore specific error
                        continue
                    print(f"Unexpected error in {func.__name__}: {str(e)}")
                    break
            print(f"Failed to complete {func.__name__} after {max_retries} attempts.")
            return None
        return wrapper
    return decorator

async def monitor_network_usage():
    previous_net_io = psutil.net_io_counters()
    while True:
        await asyncio.sleep(5)
        current_net_io = psutil.net_io_counters()
        bytes_sent = current_net_io.bytes_sent - previous_net_io.bytes_sent
        bytes_recv = current_net_io.bytes_recv - previous_net_io.bytes_recv
        print(f"\rNetwork usage - Sent: {bytes_sent / 1024:.2f} KB/s, Received: {bytes_recv / 1024:.2f} KB/s", end='')

async def check_api_connectivity():
    while True:
        await asyncio.sleep(10)
        twitch_connected = await check_twitch_connectivity()
        spotify_connected = await check_spotify_connectivity()
        print(f"\rTwitch API Connected: {twitch_connected}, Spotify API Connected: {spotify_connected}", end='')

async def check_twitch_connectivity():
    try:
        response = await bot.get_channel(TWITCH_CHANNEL)
        return response is not None
    except Exception as e:
        if "object Channel can't be used in 'await' expression" not in str(e):
            print(f"Twitch API connection error: {str(e)}")
        return False

async def check_spotify_connectivity():
    try:
        sp.current_playback()
        return True
    except Exception as e:
        print(f"Spotify API connection error: {str(e)}")
        return False

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TWITCH_BOT_TOKEN, prefix=TWITCH_BOT_PREFIX, initial_channels=[TWITCH_CHANNEL])
        self.song_queue = []
        self.is_playing = False  # Flag to track if bot is currently playing a song
        self.allow_all_users = False  # Flag to allow all users to use commands
        self.admin_only = False  # Flag to allow only admins to use commands

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        print(f'{PROGRAM_NAME}')
        # Start network and API monitoring tasks
        asyncio.create_task(monitor_network_usage())
        asyncio.create_task(check_api_connectivity())

    def is_user_allowed(self, user):
        if self.admin_only:
            return user.is_mod or user.is_broadcaster
        return self.allow_all_users or user.name in allowed_users

    @commands.command(name='np')
    async def current_song_command(self, ctx):
        await ctx.send("Fetching current song...")
        current_track_info = self.get_current_track()
        if current_track_info:
            await ctx.send(f"Currently playing: {current_track_info}")
        else:
            await ctx.send("No song is currently playing.")

    @commands.command(name='sr')
    async def queue_song_command(self, ctx):
        if self.is_user_allowed(ctx.author):
            await ctx.send("Queuing song...")
            content = ctx.message.content
            url_match = re.search(r'%sr\s+(https?://open.spotify.com/track/[^\s]+)', content)
            if url_match:
                url = url_match.group(1)  # Use group(1) to get the URL from the match
                track_info = self.get_track_info(url)
                if track_info:
                    self.song_queue.append(track_info)
                    await ctx.send(f"Song queued: {track_info} (#{len(self.song_queue)})")
                    await self.queue_song(url)
                else:
                    await ctx.send('Failed to queue the song.')
            else:
                # If not a Spotify URL, try to extract song and artist names
                song_info_match = re.search(r'%sr\s+(.+?)\s+by\s+(.+)', content)
                if song_info_match:
                    song_name = song_info_match.group(1)
                    artist_name = song_info_match.group(2)
                    url = self.search_and_queue(song_name, artist_name)
                    if url:
                        await ctx.send(f"Song queued: {song_name} by {artist_name} (#{len(self.song_queue)})")
                    else:
                        await ctx.send(f"Could not find '{song_name}' by '{artist_name}' on Spotify.")
                else:
                    await ctx.send('Invalid command format. Use %sr <Spotify URL> or %sr <song> by <artist>.')

        else:
            await ctx.send("You are not allowed to use this command.")

    def search_and_queue(self, song_name, artist_name):
        try:
            results = sp.search(q=f"track:{song_name} artist:{artist_name}", type='track', limit=1)
            if results and results['tracks'] and results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']
                sp.add_to_queue(uri=f'spotify:track:{track_id}')
                self.song_queue.append(f"{song_name} by {artist_name}")
                return results['tracks']['items'][0]['external_urls']['spotify']
            else:
                return None
        except Exception as e:
            print(f"Error searching and queuing song: {str(e)}")
            return None

    @commands.command(name='skip')
    async def skip_song_command(self, ctx):
        if self.is_user_allowed(ctx.author):
            await self.skip_song()
            await ctx.send("Skipping current song.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='vol')
    async def set_volume_command(self, ctx):
        if self.is_user_allowed(ctx.author):
            try:
                volume = int(ctx.message.content.split()[1])
                if volume < MIN_VOLUME:
                    await ctx.send("Would you like to listen to the Voice of the Void?")
                elif volume > MAX_VOLUME:
                    await ctx.send("Listening to such loudness isn't healthy. Please keep it down a bit.")
                else:
                    await self.set_volume(volume)
                    await ctx.send(f"Volume set to {volume}%")
            except (IndexError, ValueError):
                await ctx.send("Please specify a valid volume level.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='play')
    async def play_command(self, ctx):
        if self.is_user_allowed(ctx.author):
            await self.play_song()
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='pause')
    async def pause_command(self, ctx):
        if self.is_user_allowed(ctx.author):
            await self.pause_song()
            await ctx.send("Playback paused.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='allowall')
    async def allow_all_command(self, ctx):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            self.allow_all_users = True
            self.admin_only = False
            await ctx.send("All users are now allowed to use the bot commands.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='adminonly')
    async def admin_only_command(self, ctx):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            self.admin_only = True
            self.allow_all_users = False
            await ctx.send("Only admins are now allowed to use the bot commands.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command(name='exceptions')
    async def exceptions_command(self, ctx):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            await ctx.send(f"Exceptions: {', '.join(allowed_users) if allowed_users else 'None'}")
        else:
            await ctx.send("You are not allowed to use this command.")

    @retry_on_timeout()
    async def play_song(self, url=None):
        try:
            if url:
                track_id = url.split('/')[-1].split('?')[0]
                sp.start_playback(uris=[f'spotify:track:{track_id}'])
            else:
                sp.start_playback()
            self.is_playing = True
            print(f"Playing song: {url if url else 'current track'}")
        except Exception as e:
            print(f"Error playing song: {str(e)}")

    @retry_on_timeout()
    async def pause_song(self):
        try:
            sp.pause_playback()
            self.is_playing = False
            print("Playback paused.")
        except Exception as e:
            print(f"Error pausing playback: {str(e)}")

    @retry_on_timeout()
    async def queue_song(self, url):
        try:
            track_id = url.split('/')[-1].split('?')[0]
            sp.add_to_queue(uri=f'spotify:track:{track_id}')
            print(f"Song queued: {url}")
        except Exception as e:
            print(f"Error queuing song: {str(e)}")

    @retry_on_timeout()
    async def skip_song(self):
        try:
            sp.next_track()
            self.is_playing = False  # The next track will be played automatically
            print("Current song skipped.")
        except Exception as e:
            print(f"Error skipping song: {str(e)}")

    @retry_on_timeout()
    async def set_volume(self, volume):
        try:
            sp.volume(volume)
            print(f"Volume set to {volume}%")
        except Exception as e:
            print(f"Error setting volume: {str(e)}")

    def get_current_track(self):
        try:
            current_track = sp.current_playback()
            if current_track and current_track['is_playing']:
                track = current_track['item']
                artists = ', '.join(artist['name'] for artist in track['artists'])
                track_info = f"{track['name']} by {artists}"
                return track_info
            else:
                return None
        except Exception as e:
            print(f"Error fetching current track: {str(e)}")
            return None

    def get_track_info(self, url):
        try:
            track_id = url.split('/')[-1].split('?')[0]
            track = sp.track(track_id)
            artists = ', '.join(artist['name'] for artist in track['artists'])
            track_info = f"{track['name']} by {artists}"
            return track_info
        except Exception as e:
            print(f"Error fetching track info: {str(e)}")
            return None

if __name__ == "__main__":
    bot = Bot()
    bot.run()

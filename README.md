# ness_spotifybot Setup Guide

## Installation

### Prerequisites

- **Python:** Ensure Python is installed on your system (I used 3.10).
- **Dependencies:** Dependencies are automatically installed as part of the setup process.

## Installation Steps

1. **Run Installer Script:**

   Execute `install & run.bat`. This script checks for Python installation, creates a virtual environment, installs dependencies, and launches the configuration UI. It will also automatically run the `config_ui.py`.

2. **Configure Bot:**

   Open `config_ui.py` to configure Spotify and Twitch credentials. Save the credentials to `credentials.txt` using the UI.

3. **Start the Bot:**

   Once configured, run `spoti.py` or `install & run.bat` to start the bot and connect it to Twitch and Spotify.

## Usage

- Customize `exceptions.txt` to add users allowed to use your bot (include your name too/no capslock needed).

- Use Twitch chat commands (`%np`, `%sr`, `%skip`, `%vol`, etc.) to interact with the bot during live streams.

Here are the commands:

**%np** - Displays the currently playing song  
**%sr [song name or URL]** - Requests the specified song to be added to the queue  
**%skip** - Skips the currently playing song  
**%vol [volume level]** - Sets the playback volume to the specified level  
**%allowall** - Allows all users to interact with the bot's commands

## Additional Notes

- **spotify redirect URI:**
   - I used `http://localhost:8888/callback`, it is is essentially a placeholder URL that points to a callback endpoint on your local machine, used in scenarios where OAuth flows need to redirect back to your application after user interaction.

- **API Credentials:**
  - To create the Spotify API and get the Spotify Client ID and Client Secret, head to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
  - To get your Twitch Bot Token, you can use [Twitch Token Generator](https://twitchtokengenerator.com/) or refer to the [Twitch OAuth documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/).
  - Your Twitch channel name should be the name, not the URL (e.g., "altereterna", not "https://www.twitch.tv/altereterna").
  - You can choose your own prefix for Twitch bot commands; the default is `%`.
  - Please don't share your credentials with anyone, including me.

## Credits

Made by [@altereterna](https://altereterna.wordpress.com) and her AI, Ness.

## Support

For issues or questions, feel free to contact me :D

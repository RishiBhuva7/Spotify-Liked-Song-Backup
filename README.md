# Spotify Liked Songs Backup

A Python script that backs up your Spotify liked songs by copying them into a custom playlist, avoiding duplicates, and keeping your favorites organized.

## Features

- **Fetch Liked Songs**: Retrieve all your saved (liked) songs from Spotify.
- **Create Backup Playlist**: Automatically creates a backup playlist if it doesn’t exist.
- **Avoid Duplicates**: Adds only new liked songs that are not already in the backup playlist.
- **Private Playlist by Default**: Creates the backup playlist as private (configurable).
- **Handles Pagination**: Supports large libraries by fetching songs in batches.

## Tech Stack

- **Language**: Python 3.7+
- **Spotify API Wrapper**: [Spotipy](https://spotipy.readthedocs.io/)
- **Environment Variables**: [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv 

# Activate it
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Spotify Developer Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Log in and click **"Create an App"**.
3. Set the **Redirect URI** to:  
   ```
   http://127.0.0.1:8888/callback
   ```
   (You can change it, but make sure it matches the one in your `.env` file.)

### 4. Configure environment variables

Copy your **Client ID** and **Client Secret** and paste them into a `.env` file like this:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 5. Run the script

```bash
python main.py
```
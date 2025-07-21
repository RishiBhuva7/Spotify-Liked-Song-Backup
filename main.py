import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

sp=spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-modify-private playlist-modify-public playlist-read-private"
))

# Get all liked songs
def get_liked_tracks():
    liked_tracks=[]
    results=sp.current_user_saved_tracks(limit=50)
    liked_tracks.extend(results["items"])

    while results["next"]:
        results=sp.next(results)
        liked_tracks.extend(results["items"])

    print(f"Found {len(liked_tracks)} liked songs.")
    return liked_tracks

# Create a new playlist
def get_or_create_playlist(name):
    user_id=sp.me()["id"]
    playlists=[]
    results=sp.current_user_playlists(limit=50)
    playlists.extend(results["items"])

    while results["next"]:
        results=sp.next(results)
        playlists.extend(results["items"])

    # Search for existing playlist by name    
    for playlist in playlists:
        print(f"Checking playlist: '{playlist["name"]}'")
        if playlist["name"].strip().lower()==name.strip().lower():
            print("Found existing playlist.")
            return playlist["id"]
        
    # If not found, create new one
    playlist=sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False
    )
    print(f"Created playlist: {name}")
    return playlist["id"]

# Add tracks to new playlist
def add_tracks_to_playlist(playlist_id, track_ids):
    # Spotify only allows 100 tracks per request
    for i in range(0,len(track_ids),100):
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])
    print(f"Added {len(track_ids)} songs to new playlist.")

def get_tracks_in_playlist(playlist_id):
    track_ids=[]
    results=sp.playlist_tracks(playlist_id)
    track_ids.extend([item["track"]["id"] for item in results["items"] if item["track"]])

    while results["next"]:
        results=sp.next(results)
        track_ids.extend([item["track"]["id"] for item in results["items"] if item["track"]])

    return track_ids


# Full process
def transfer_liked_to_playlist(playlist_name):
    liked_tracks=get_liked_tracks()
    track_ids=[]

    for i in liked_tracks:
        if i["track"] and i["track"]["id"]:
            track_ids.append(i["track"]["id"])
    
    playlist_id=get_or_create_playlist(playlist_name) # Handles existing playlists too
    existing_ids=get_tracks_in_playlist(playlist_id)

    # Only keep new tracks not already in playlist
    new_track_ids=[]
    for i in track_ids:
        if i not in existing_ids:
            new_track_ids.append(i)

    print(f"Adding {len(new_track_ids)} new tracks to playlist.")
    add_tracks_to_playlist(playlist_id,new_track_ids)

# Run the transfer
if __name__=="__main__":
    transfer_liked_to_playlist("My Liked Songs Backup")
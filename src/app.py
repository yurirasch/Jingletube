import gradio as gr
import os
import json
import datetime
from pathlib import Path
import tempfile
import shutil

# Initialize data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
SONGS_FILE = DATA_DIR / "songs.json"
RECORDINGS_FILE = DATA_DIR / "recordings.json"
RANKINGS_FILE = DATA_DIR / "rankings.json"

# Initialize data files if they don't exist
for file_path in [USERS_FILE, SONGS_FILE, RECORDINGS_FILE, RANKINGS_FILE]:
    if not file_path.exists():
        with open(file_path, 'w') as f:
            json.dump({}, f)

def load_json(file_path):
    """Load JSON data from file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_json(file_path, data):
    """Save JSON data to file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def register_user(username, password, email):
    """Register a new user"""
    if not username or not password:
        return "Username and password are required!"
    
    users = load_json(USERS_FILE)
    
    if username in users:
        return "Username already exists!"
    
    users[username] = {
        "password": password,  # In production, use proper password hashing!
        "email": email,
        "created_at": str(datetime.datetime.now()),
        "recordings": [],
        "favorites": []
    }
    
    save_json(USERS_FILE, users)
    return f"User {username} registered successfully!"

def login_user(username, password):
    """Authenticate user"""
    users = load_json(USERS_FILE)
    
    if username not in users:
        return False, "User not found!"
    
    if users[username]["password"] != password:
        return False, "Invalid password!"
    
    return True, f"Welcome back, {username}!"

def add_song_to_library(title, artist, genre, lyrics, audio_file):
    """Add a new song to the library"""
    if not title or not artist:
        return "Title and artist are required!"
    
    songs = load_json(SONGS_FILE)
    song_id = f"song_{len(songs) + 1}_{datetime.datetime.now().timestamp()}"
    
    # Handle audio file upload
    audio_path = None
    if audio_file:
        audio_dir = DATA_DIR / "audio" / "songs"
        audio_dir.mkdir(parents=True, exist_ok=True)
        audio_path = f"data/audio/songs/{song_id}.mp3"
        shutil.copy(audio_file, audio_path)
    
    songs[song_id] = {
        "title": title,
        "artist": artist,
        "genre": genre,
        "lyrics": lyrics,
        "audio_path": audio_path,
        "added_at": str(datetime.datetime.now()),
        "play_count": 0
    }
    
    save_json(SONGS_FILE, songs)
    return f"Song '{title}' by {artist} added successfully!"

def get_song_list(genre_filter="All"):
    """Get list of songs, optionally filtered by genre"""
    songs = load_json(SONGS_FILE)
    
    if not songs:
        return [["No songs available", "", "", ""]]
    
    song_list = []
    for song_id, song_data in songs.items():
        if genre_filter == "All" or song_data.get("genre") == genre_filter:
            song_list.append([
                song_data["title"],
                song_data["artist"],
                song_data.get("genre", "Unknown"),
                song_id
            ])
    
    return song_list if song_list else [["No songs found", "", "", ""]]

def save_recording(username, song_id, recording_file, rating=None):
    """Save a user's recording"""
    if not recording_file:
        return "No recording file provided!"
    
    recordings = load_json(RECORDINGS_FILE)
    recording_id = f"rec_{username}_{song_id}_{datetime.datetime.now().timestamp()}"
    
    # Save recording file
    rec_dir = DATA_DIR / "audio" / "recordings"
    rec_dir.mkdir(parents=True, exist_ok=True)
    rec_path = f"data/audio/recordings/{recording_id}.mp3"
    shutil.copy(recording_file, rec_path)
    
    recordings[recording_id] = {
        "username": username,
        "song_id": song_id,
        "recording_path": rec_path,
        "timestamp": str(datetime.datetime.now()),
        "rating": rating,
        "likes": 0,
        "comments": []
    }
    
    save_json(RECORDINGS_FILE, recordings)
    
    # Update user's recordings
    users = load_json(USERS_FILE)
    if username in users:
        users[username]["recordings"].append(recording_id)
        save_json(USERS_FILE, users)
    
    # Update song play count
    songs = load_json(SONGS_FILE)
    if song_id in songs:
        songs[song_id]["play_count"] = songs[song_id].get("play_count", 0) + 1
        save_json(SONGS_FILE, songs)
    
    return f"Recording saved successfully! ID: {recording_id}"

def get_rankings(sort_by="likes"):
    """Get rankings of recordings"""
    recordings = load_json(RECORDINGS_FILE)
    songs = load_json(SONGS_FILE)
    
    if not recordings:
        return [["No recordings yet", "", "", "0"]]
    
    ranking_list = []
    for rec_id, rec_data in recordings.items():
        song_id = rec_data.get("song_id")
        song_title = songs.get(song_id, {}).get("title", "Unknown") if song_id in songs else "Unknown"
        
        ranking_list.append([
            rec_data["username"],
            song_title,
            rec_data.get("timestamp", "Unknown"),
            str(rec_data.get("likes", 0)),
            rec_id
        ])
    
    # Sort by likes (descending)
    if sort_by == "likes":
        ranking_list.sort(key=lambda x: int(x[3]), reverse=True)
    
    return ranking_list

def like_recording(recording_id):
    """Add a like to a recording"""
    recordings = load_json(RECORDINGS_FILE)
    
    if recording_id not in recordings:
        return "Recording not found!"
    
    recordings[recording_id]["likes"] = recordings[recording_id].get("likes", 0) + 1
    save_json(RECORDINGS_FILE, recordings)
    
    return f"Liked! Total likes: {recordings[recording_id]['likes']}"

def add_comment(recording_id, username, comment):
    """Add a comment to a recording"""
    if not comment:
        return "Comment cannot be empty!"
    
    recordings = load_json(RECORDINGS_FILE)
    
    if recording_id not in recordings:
        return "Recording not found!"
    
    comment_data = {
        "username": username,
        "comment": comment,
        "timestamp": str(datetime.datetime.now())
    }
    
    if "comments" not in recordings[recording_id]:
        recordings[recording_id]["comments"] = []
    
    recordings[recording_id]["comments"].append(comment_data)
    save_json(RECORDINGS_FILE, recordings)
    
    return "Comment added successfully!"

def get_user_stats(username):
    """Get statistics for a user"""
    users = load_json(USERS_FILE)
    recordings = load_json(RECORDINGS_FILE)
    
    if username not in users:
        return "User not found!"
    
    user_recordings = users[username].get("recordings", [])
    total_likes = sum(recordings.get(rec_id, {}).get("likes", 0) for rec_id in user_recordings)
    
    stats = f"""
    📊 Statistics for {username}
    
    Total Recordings: {len(user_recordings)}
    Total Likes Received: {total_likes}
    Member Since: {users[username].get('created_at', 'Unknown')}
    Favorite Songs: {len(users[username].get('favorites', []))}
    """
    
    return stats

# Create Gradio Interface
with gr.Blocks(title="🎵 JingleTube - Karaoke Social Platform", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🎵 JingleTube - Your Karaoke Social Platform
    ### Sing, Share, and Compete with Friends!
    """)
    
    # Session state
    current_user = gr.State(None)
    
    with gr.Tabs() as tabs:
        # Authentication Tab
        with gr.Tab("🔐 Login/Register"):
            gr.Markdown("## Welcome to JingleTube!")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🔓 Login")
                    login_username = gr.Textbox(label="Username", placeholder="Enter your username")
                    login_password = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
                    login_btn = gr.Button("Login", variant="primary")
                    login_output = gr.Textbox(label="Status", interactive=False)
                
                with gr.Column():
                    gr.Markdown("### 📝 Register")
                    reg_username = gr.Textbox(label="Username", placeholder="Choose a username")
                    reg_password = gr.Textbox(label="Password", type="password", placeholder="Choose a password")
                    reg_email = gr.Textbox(label="Email", placeholder="your@email.com")
                    register_btn = gr.Button("Register", variant="primary")
                    register_output = gr.Textbox(label="Status", interactive=False)
        
        # Song Library Tab
        with gr.Tab("📚 Song Library"):
            gr.Markdown("## Browse and Add Songs")
            
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Available Songs")
                    genre_filter = gr.Dropdown(
                        choices=["All", "Pop", "Rock", "Jazz", "Country", "R&B", "Hip-Hop", "Classical"],
                        value="All",
                        label="Filter by Genre"
                    )
                    song_table = gr.Dataframe(
                        headers=["Title", "Artist", "Genre", "Song ID"],
                        label="Song Library",
                        interactive=False
                    )
                    refresh_songs_btn = gr.Button("🔄 Refresh List")
                
                with gr.Column(scale=1):
                    gr.Markdown("### Add New Song")
                    new_song_title = gr.Textbox(label="Title")
                    new_song_artist = gr.Textbox(label="Artist")
                    new_song_genre = gr.Dropdown(
                        choices=["Pop", "Rock", "Jazz", "Country", "R&B", "Hip-Hop", "Classical"],
                        label="Genre"
                    )
                    new_song_lyrics = gr.TextArea(label="Lyrics (Optional)")
                    new_song_audio = gr.Audio(label="Upload Instrumental Track", type="filepath")
                    add_song_btn = gr.Button("➕ Add Song", variant="primary")
                    add_song_output = gr.Textbox(label="Status", interactive=False)
        
        # Singing Interface Tab
        with gr.Tab("🎤 Sing!"):
            gr.Markdown("## Record Your Performance")
            
            with gr.Row():
                with gr.Column():
                    selected_song_id = gr.Textbox(label="Song ID", placeholder="Copy from Song Library")
                    gr.Markdown("### 🎙️ Record Your Voice")
                    recording_input = gr.Audio(label="Record or Upload", type="filepath", sources=["microphone", "upload"])
                    self_rating = gr.Slider(minimum=1, maximum=10, step=1, label="Rate Your Performance", value=5)
                    save_recording_btn = gr.Button("💾 Save Recording", variant="primary")
                    recording_output = gr.Textbox(label="Status", interactive=False)
                
                with gr.Column():
                    gr.Markdown("### 📝 Song Lyrics")
                    display_lyrics = gr.TextArea(label="Lyrics will appear here", interactive=False, lines=15)
        
        # Rankings Tab
        with gr.Tab("🏆 Rankings"):
            gr.Markdown("## Top Performances")
            
            sort_option = gr.Radio(
                choices=["likes", "recent"],
                value="likes",
                label="Sort By"
            )
            
            rankings_table = gr.Dataframe(
                headers=["User", "Song", "Date", "Likes", "Recording ID"],
                label="Leaderboard",
                interactive=False
            )
            
            refresh_rankings_btn = gr.Button("🔄 Refresh Rankings")
            
            with gr.Row():
                with gr.Column():
                    like_recording_id = gr.Textbox(label="Recording ID to Like")
                    like_btn = gr.Button("👍 Like", variant="primary")
                    like_output = gr.Textbox(label="Status", interactive=False)
                
                with gr.Column():
                    comment_recording_id = gr.Textbox(label="Recording ID")
                    comment_text = gr.Textbox(label="Your Comment")
                    comment_btn = gr.Button("💬 Add Comment", variant="primary")
                    comment_output = gr.Textbox(label="Status", interactive=False)
        
        # Profile Tab
        with gr.Tab("👤 Profile"):
            gr.Markdown("## Your Profile")
            
            stats_username = gr.Textbox(label="Username", placeholder="Enter username to view stats")
            get_stats_btn = gr.Button("📊 Get Statistics", variant="primary")
            stats_output = gr.TextArea(label="User Statistics", interactive=False, lines=10)
    
    # Event Handlers
    def handle_login(username, password):
        success, message = login_user(username, password)
        return message, username if success else None
    
    login_btn.click(
        fn=handle_login,
        inputs=[login_username, login_password],
        outputs=[login_output, current_user]
    )
    
    register_btn.click(
        fn=register_user,
        inputs=[reg_username, reg_password, reg_email],
        outputs=register_output
    )
    
    add_song_btn.click(
        fn=add_song_to_library,
        inputs=[new_song_title, new_song_artist, new_song_genre, new_song_lyrics, new_song_audio],
        outputs=add_song_output
    )
    
    refresh_songs_btn.click(
        fn=get_song_list,
        inputs=[genre_filter],
        outputs=song_table
    )
    
    genre_filter.change(
        fn=get_song_list,
        inputs=[genre_filter],
        outputs=song_table
    )
    
    def handle_save_recording(username, song_id, recording, rating):
        if not username:
            return "Please login first!"
        return save_recording(username, song_id, recording, rating)
    
    save_recording_btn.click(
        fn=handle_save_recording,
        inputs=[current_user, selected_song_id, recording_input, self_rating],
        outputs=recording_output
    )
    
    refresh_rankings_btn.click(
        fn=get_rankings,
        inputs=[sort_option],
        outputs=rankings_table
    )
    
    like_btn.click(
        fn=like_recording,
        inputs=[like_recording_id],
        outputs=like_output
    )
    
    def handle_comment(rec_id, username, comment):
        if not username:
            return "Please login first!"
        return add_comment(rec_id, username, comment)
    
    comment_btn.click(
        fn=handle_comment,
        inputs=[comment_recording_id, current_user, comment_text],
        outputs=comment_output
    )
    
    get_stats_btn.click(
        fn=get_user_stats,
        inputs=[stats_username],
        outputs=stats_output
    )
    
    # Load initial data
    app.load(
        fn=get_song_list,
        inputs=[genre_filter],
        outputs=song_table
    )
    
    app.load(
        fn=get_rankings,
        inputs=[sort_option],
        outputs=rankings_table
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)

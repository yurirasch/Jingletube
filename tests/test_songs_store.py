"""Tests for songs store module."""

import tempfile
import os
from store.songs import SongsStore


def test_add_song():
    """Test adding a song to the store."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = SongsStore(temp_file)
        song_data = {
            "title": "Never Gonna Give You Up",
            "artist": "Rick Astley",
            "video_id": "dQw4w9WgXcQ",
            "duration": 213
        }
        
        song_id = store.add_song(song_data)
        assert song_id is not None
        assert isinstance(song_id, str)
        
        # Verify song was added
        all_songs = store.get_all_songs()
        assert len(all_songs) == 1
        assert all_songs[0]["title"] == "Never Gonna Give You Up"
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_add_duplicate_song():
    """Test handling of duplicate songs."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = SongsStore(temp_file)
        song_data = {
            "title": "Test Song",
            "artist": "Test Artist",
            "video_id": "test123",
            "duration": 180
        }
        
        song_id1 = store.add_song(song_data)
        song_id2 = store.add_song(song_data)
        
        # Either returns same ID or creates new one based on implementation
        assert song_id1 is not None
        assert song_id2 is not None
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_all_songs():
    """Test retrieving all songs from the store."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = SongsStore(temp_file)
        
        # Empty store
        assert len(store.get_all_songs()) == 0
        
        # Add multiple songs
        store.add_song({"title": "Song 1", "artist": "Artist 1", "video_id": "vid1"})
        store.add_song({"title": "Song 2", "artist": "Artist 2", "video_id": "vid2"})
        store.add_song({"title": "Song 3", "artist": "Artist 3", "video_id": "vid3"})
        
        all_songs = store.get_all_songs()
        assert len(all_songs) == 3
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_song_by_id():
    """Test finding a song by ID."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = SongsStore(temp_file)
        song_data = {
            "title": "Specific Song",
            "artist": "Specific Artist",
            "video_id": "specific123"
        }
        
        song_id = store.add_song(song_data)
        retrieved_song = store.get_song_by_id(song_id)
        
        assert retrieved_song is not None
        assert retrieved_song["title"] == "Specific Song"
        assert retrieved_song["artist"] == "Specific Artist"
        
        # Test non-existent ID
        non_existent = store.get_song_by_id("non_existent_id")
        assert non_existent is None
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_delete_song():
    """Test deleting a song from the store."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = SongsStore(temp_file)
        song_data = {"title": "To Delete", "artist": "Artist", "video_id": "del123"}
        
        song_id = store.add_song(song_data)
        assert len(store.get_all_songs()) == 1
        
        # Delete the song
        result = store.delete_song(song_id)
        assert result is True
        assert len(store.get_all_songs()) == 0
        
        # Try to delete non-existent song
        result = store.delete_song("non_existent")
        assert result is False
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

"""Tests for scores store module."""

import tempfile
import os
from store.scores import ScoresStore


def test_add_score():
    """Test adding a score to the store."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = ScoresStore(temp_file)
        score_data = {
            "song_id": "song123",
            "player_name": "Alice",
            "score": 9500,
            "accuracy": 95.5,
            "max_combo": 150
        }
        
        score_id = store.add_score(score_data)
        assert score_id is not None
        assert isinstance(score_id, str)
        
        # Verify score was added
        all_scores = store.get_all_scores()
        assert len(all_scores) == 1
        assert all_scores[0]["player_name"] == "Alice"
        assert all_scores[0]["score"] == 9500
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_all_scores():
    """Test retrieving all scores from the store."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = ScoresStore(temp_file)
        
        # Empty store
        assert len(store.get_all_scores()) == 0
        
        # Add multiple scores
        store.add_score({"song_id": "song1", "player_name": "Alice", "score": 9000})
        store.add_score({"song_id": "song1", "player_name": "Bob", "score": 8500})
        store.add_score({"song_id": "song2", "player_name": "Charlie", "score": 9500})
        
        all_scores = store.get_all_scores()
        assert len(all_scores) == 3
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_scores_by_song():
    """Test filtering scores by song ID."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = ScoresStore(temp_file)
        
        # Add scores for different songs
        store.add_score({"song_id": "song1", "player_name": "Alice", "score": 9000})
        store.add_score({"song_id": "song1", "player_name": "Bob", "score": 8500})
        store.add_score({"song_id": "song2", "player_name": "Charlie", "score": 9500})
        store.add_score({"song_id": "song1", "player_name": "Dave", "score": 7500})
        
        song1_scores = store.get_scores_by_song("song1")
        assert len(song1_scores) == 3
        
        song2_scores = store.get_scores_by_song("song2")
        assert len(song2_scores) == 1
        assert song2_scores[0]["player_name"] == "Charlie"
        
        # Non-existent song
        no_scores = store.get_scores_by_song("song999")
        assert len(no_scores) == 0
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_get_top_scores():
    """Test retrieving top scores."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = ScoresStore(temp_file)
        
        # Add scores with different values
        store.add_score({"song_id": "song1", "player_name": "Alice", "score": 9000})
        store.add_score({"song_id": "song1", "player_name": "Bob", "score": 8500})
        store.add_score({"song_id": "song1", "player_name": "Charlie", "score": 9500})
        store.add_score({"song_id": "song1", "player_name": "Dave", "score": 7500})
        store.add_score({"song_id": "song1", "player_name": "Eve", "score": 10000})
        
        # Get top 3 scores
        top_3 = store.get_top_scores("song1", limit=3)
        assert len(top_3) == 3
        assert top_3[0]["score"] == 10000
        assert top_3[1]["score"] == 9500
        assert top_3[2]["score"] == 9000
        
        # Get all scores (more than available)
        top_10 = store.get_top_scores("song1", limit=10)
        assert len(top_10) == 5
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_top_scores_ordering():
    """Test that top scores are properly ordered by score descending."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        store = ScoresStore(temp_file)
        
        # Add scores in random order
        scores = [5000, 9000, 3000, 10000, 7500, 8500]
        for i, score in enumerate(scores):
            store.add_score({
                "song_id": "test_song",
                "player_name": f"Player{i}",
                "score": score
            })
        
        top_scores = store.get_top_scores("test_song", limit=10)
        
        # Verify descending order
        for i in range(len(top_scores) - 1):
            assert top_scores[i]["score"] >= top_scores[i + 1]["score"]
        
        # Verify highest score is first
        assert top_scores[0]["score"] == 10000
        assert top_scores[-1]["score"] == 3000
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

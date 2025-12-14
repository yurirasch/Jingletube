"""Tests for YouTube URL parser module."""

from youtube.parser import extract_video_id, is_valid_youtube_url


def test_extract_video_id_standard():
    """Test extraction from standard YouTube URL."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_short():
    """Test extraction from short YouTube URL."""
    url = "https://youtu.be/dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_with_params():
    """Test extraction from URL with additional parameters."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_embed():
    """Test extraction from embed YouTube URL."""
    url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_mobile():
    """Test extraction from mobile YouTube URL."""
    url = "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_invalid():
    """Test extraction from invalid URL returns None."""
    url = "https://www.example.com/video"
    video_id = extract_video_id(url)
    assert video_id is None


def test_is_valid_youtube_url_valid():
    """Test validation of valid YouTube URLs."""
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
    for url in valid_urls:
        assert is_valid_youtube_url(url) is True


def test_is_valid_youtube_url_invalid():
    """Test validation of invalid YouTube URLs."""
    invalid_urls = [
        "https://www.example.com/video",
        "https://vimeo.com/123456",
        "not a url",
        "",
        "https://youtube.com"
    ]
    for url in invalid_urls:
        assert is_valid_youtube_url(url) is False

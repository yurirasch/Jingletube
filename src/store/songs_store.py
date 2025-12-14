"""
Gerenciamento de músicas
CRUD para o arquivo songs.json
"""
import json
import os
from datetime import datetime
import uuid

SONGS_FILE = "data/songs.json"

def _ensure_data_dir():
    """Garante que o diretório data/ existe"""
    os.makedirs("data", exist_ok=True)

def _load_songs():
    """Carrega músicas do arquivo JSON"""
    _ensure_data_dir()
    if not os.path.exists(SONGS_FILE):
        return []
    
    try:
        with open(SONGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def _save_songs(songs):
    """Salva músicas no arquivo JSON"""
    _ensure_data_dir()
    with open(SONGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(songs, f, indent=2, ensure_ascii=False)

def add_song(youtube_id, titulo=None):
    """
    Adiciona uma nova música
    
    Args:
        youtube_id (str): ID do vídeo do YouTube
        titulo (str): Título da música (opcional)
        
    Returns:
        dict: Música adicionada
    """
    songs = _load_songs()
    
    # Verifica se já existe
    for song in songs:
        if song['youtubeId'] == youtube_id:
            return song
    
    song = {
        "id": str(uuid.uuid4()),
        "youtubeId": youtube_id,
        "titulo": titulo or f"Música {len(songs) + 1}",
        "criadoEm": datetime.utcnow().isoformat() + "Z"
    }
    
    songs.append(song)
    _save_songs(songs)
    return song

def get_all_songs():
    """
    Retorna todas as músicas
    
    Returns:
        list: Lista de músicas
    """
    return _load_songs()

def get_song_by_id(song_id):
    """
    Busca uma música por ID
    
    Args:
        song_id (str): ID da música
        
    Returns:
        dict: Música encontrada ou None
    """
    songs = _load_songs()
    for song in songs:
        if song['id'] == song_id:
            return song
    return None

def delete_song(song_id):
    """
    Remove uma música
    
    Args:
        song_id (str): ID da música
        
    Returns:
        bool: True se removido com sucesso
    """
    songs = _load_songs()
    filtered = [s for s in songs if s['id'] != song_id]
    
    if len(filtered) < len(songs):
        _save_songs(filtered)
        return True
    return False

"""
Gerenciamento de pontuações
CRUD para o arquivo scores.json
"""
import json
import os
from datetime import datetime
import uuid

SCORES_FILE = "data/scores.json"

def _ensure_data_dir():
    """Garante que o diretório data/ existe"""
    os.makedirs("data", exist_ok=True)

def _load_scores():
    """Carrega pontuações do arquivo JSON"""
    _ensure_data_dir()
    if not os.path.exists(SCORES_FILE):
        return []
    
    try:
        with open(SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def _save_scores(scores):
    """Salva pontuações no arquivo JSON"""
    _ensure_data_dir()
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

def add_score(song_id, player_name, score, accuracy=None):
    """
    Adiciona uma nova pontuação
    
    Args:
        song_id (str): ID da música
        player_name (str): Nome do jogador
        score (int): Pontuação obtida
        accuracy (float): Precisão percentual (opcional)
        
    Returns:
        dict: Pontuação adicionada
    """
    scores = _load_scores()
    
    score_entry = {
        "id": str(uuid.uuid4()),
        "songId": song_id,
        "playerName": player_name,
        "score": score,
        "accuracy": accuracy,
        "criadoEm": datetime.utcnow().isoformat() + "Z"
    }
    
    scores.append(score_entry)
    _save_scores(scores)
    return score_entry

def get_all_scores():
    """
    Retorna todas as pontuações
    
    Returns:
        list: Lista de pontuações
    """
    return _load_scores()

def get_scores_by_song(song_id):
    """
    Busca pontuações por música
    
    Args:
        song_id (str): ID da música
        
    Returns:
        list: Lista de pontuações da música
    """
    scores = _load_scores()
    return [s for s in scores if s['songId'] == song_id]

def get_top_scores(song_id=None, limit=10):
    """
    Retorna as melhores pontuações
    
    Args:
        song_id (str): ID da música (opcional, None retorna de todas)
        limit (int): Número máximo de resultados
        
    Returns:
        list: Lista das melhores pontuações ordenadas
    """
    scores = _load_scores()
    
    if song_id:
        scores = [s for s in scores if s['songId'] == song_id]
    
    # Ordena por pontuação (decrescente)
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:limit]

def delete_score(score_id):
    """
    Remove uma pontuação
    
    Args:
        score_id (str): ID da pontuação
        
    Returns:
        bool: True se removido com sucesso
    """
    scores = _load_scores()
    filtered = [s for s in scores if s['id'] != score_id]
    
    if len(filtered) < len(scores):
        _save_scores(filtered)
        return True
    return False

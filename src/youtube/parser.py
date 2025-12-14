"""
YouTube URL Parser
Parseia URLs do YouTube para extrair IDs de vídeos
"""
import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """
    Extrai o ID do vídeo de uma URL do YouTube
    
    Args:
        url (str): URL do YouTube
        
    Returns:
        str: ID do vídeo ou None se não encontrado
    """
    if not url:
        return None
    
    # Padrões de URL do YouTube
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]+)',
        r'(?:youtu\.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)',
        r'(?:youtube\.com\/v\/)([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Tenta extrair da query string
    try:
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                return query_params['v'][0]
    except:
        pass
    
    return None

def is_valid_youtube_url(url):
    """
    Verifica se a URL é uma URL válida do YouTube
    
    Args:
        url (str): URL para validar
        
    Returns:
        bool: True se for uma URL válida do YouTube
    """
    return extract_video_id(url) is not None
"""
Autenticação via Hugging Face OAuth
"""
import os

def is_hf_oauth_enabled():
    """
    Verifica se as variáveis de ambiente OAuth do HF estão configuradas
    """
    return bool(os.getenv("OAUTH_CLIENT_ID") and os.getenv("OAUTH_CLIENT_SECRET"))

def get_hf_oauth_config():
    """
    Retorna a configuração do OAuth do Hugging Face
    """
    if not is_hf_oauth_enabled():
        return None
    
    return {
        "client_id": os.getenv("OAUTH_CLIENT_ID"),
        "client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
        "provider": "huggingface"
    }

def authenticate_hf(token):
    """
    Autentica um usuário via token do Hugging Face
    
    Args:
        token (str): Token de autenticação do HF
        
    Returns:
        dict: Informações do usuário autenticado
    """
    if not token:
        return None
    
    # TODO: Implementar validação real do token via API do HF
    # Por enquanto, retorna um mock
    return {
        "username": "hf_user",
        "provider": "huggingface",
        "authenticated": True,
        "token": token
    }
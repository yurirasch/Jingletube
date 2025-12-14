"""
Autenticação em modo DEV
Permite login manual digitando um nome de usuário
"""

def dev_login():
    """
    Modo de desenvolvimento: login manual
    Retorna o nome de usuário digitado
    """
    return {
        "enabled": True,
        "provider": "dev",
        "method": "manual_input"
    }

def authenticate_dev(username):
    """
    Autentica um usuário no modo DEV
    
    Args:
        username (str): Nome de usuário digitado
        
    Returns:
        dict: Informações do usuário autenticado
    """
    if not username or len(username.strip()) == 0:
        return None
    
    return {
        "username": username.strip(),
        "provider": "dev",
        "authenticated": True
    }

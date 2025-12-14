"""
Gerenciador de autenticação
Abstração que permite trocar providers facilmente
"""
from .dev_auth import authenticate_dev, dev_login
from .hf_oauth import is_hf_oauth_enabled, authenticate_hf

class AuthManager:
    """
    Gerenciador central de autenticação
    """
    
    def __init__(self):
        self.current_user = None
        self.provider = self._detect_provider()
    
    def _detect_provider(self):
        """
        Detecta qual provider de autenticação está disponível
        """
        if is_hf_oauth_enabled():
            return "huggingface"
        return "dev"
    
    def is_dev_mode(self):
        """
        Verifica se está em modo DEV
        """
        return self.provider == "dev"
    
    def login(self, username=None, token=None):
        """
        Realiza login com o provider apropriado
        
        Args:
            username (str): Nome de usuário (para modo DEV)
            token (str): Token OAuth (para HF)
            
        Returns:
            dict: Informações do usuário autenticado ou None
        """
        if self.provider == "dev" and username:
            self.current_user = authenticate_dev(username)
            return self.current_user
        
        if self.provider == "huggingface" and token:
            self.current_user = authenticate_hf(token)
            return self.current_user
        
        return None
    
    def logout(self):
        """
        Realiza logout do usuário atual
        """
        self.current_user = None
    
    def get_current_user(self):
        """
        Retorna o usuário atualmente autenticado
        """
        return self.current_user
    
    def is_authenticated(self):
        """
        Verifica se há um usuário autenticado
        """
        return self.current_user is not None
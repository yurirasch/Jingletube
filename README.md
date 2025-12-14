# 🎤 JingleTube

Um aplicativo web de karaokê com pontuação onde usuários cantam músicas do YouTube e recebem notas.

## 🎯 Sobre o Projeto

JingleTube é uma plataforma de karaokê online que permite:
- 🎵 Adicionar músicas de karaokê do YouTube
- 🎤 Cantar e receber pontuação
- 🏆 Competir nos rankings por música
- 📊 Acompanhar seu histórico de performances

## 🔧 Stack Técnica

- **Python 3.11**
- **Gradio** - Interface web
- **JSON** - Persistência de dados (MVP)
- **Hugging Face Spaces** - Hospedagem

## 🚀 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/yurirasch/Jingletube.git
cd Jingletube
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o app:
```bash
python src/app.py
```

5. Acesse no navegador: `http://localhost:7860`

## 🌐 Deploy no Hugging Face Spaces

1. Crie um novo Space em [huggingface.co/spaces](https://huggingface.co/new-space)
2. Escolha **Gradio** como SDK
3. Conecte este repositório GitHub
4. O Space será atualizado automaticamente a cada push

Para mais detalhes, veja: [docs/CUSTOM_DOMAIN_HF.md](docs/CUSTOM_DOMAIN_HF.md)

## 🔐 Autenticação

O JingleTube suporta múltiplos modos de autenticação:

### 1. Modo DEV (padrão local)
- Login manual digitando um nome de usuário
- Ativado quando variáveis OAuth não estão presentes

### 2. Hugging Face OAuth
- Login com conta do Hugging Face
- Configure as variáveis de ambiente no Space

### 3. Cloudflare Access (produção)
- Proteção externa via Cloudflare One
- Google como Identity Provider
- Veja instruções em: [docs/CLOUDFLARE_ACCESS_SETUP.md](docs/CLOUDFLARE_ACCESS_SETUP.md)

## 📁 Estrutura do Projeto

```
jingle-tube/
├─ src/
│  ├─ app.py                 # Entrypoint Gradio
│  ├─ auth/                  # Sistema de autenticação
│  │   ├─ dev_auth.py        # Login DEV
│  │   ├─ hf_oauth.py        # OAuth Hugging Face
│  │   └─ auth_manager.py    # Gerenciador de auth
│  ├─ youtube/               # Parser de URLs do YouTube
│  │   └─ parser.py
│  └─ store/                 # Persistência de dados
│      ├─ songs_store.py     # Gerenciamento de músicas
│      └─ scores_store.py    # Gerenciamento de pontuações
├─ data/                     # Dados persistidos (JSON)
│  ├─ songs.json
│  └─ scores.json
├─ tests/                    # Testes automatizados
├─ docs/                     # Documentação
└─ .github/workflows/        # CI/CD
```

## 🎵 Funcionalidades

### 📚 Biblioteca de Músicas
- Adicione músicas colando links do YouTube
- Suporte para múltiplos formatos de URL
- Visualize todas as músicas cadastradas

### 🎤 Cantar
- Selecione uma música da biblioteca
- Abra o vídeo do YouTube
- Registre sua pontuação

### 🏆 Rankings
- Rankings separados por música
- Top 10 melhores pontuações
- Destaque do seu melhor score

## 🧪 Testes

Execute os testes:
```bash
pytest
```

Execute com coverage:
```bash
pytest --cov=src tests/
```

## 🛠️ Desenvolvimento

O projeto usa GitHub Actions para CI/CD:
- ✅ Verificação de sintaxe Python
- ✅ Execução de testes
- ✅ Validação em cada push/PR

## 📋 Roadmap

- [x] ✅ Estrutura base do projeto
- [x] ✅ Sistema de autenticação
- [x] ✅ Biblioteca de músicas
- [x] ✅ Sistema de rankings
- [ ] 🎙️ Captura de áudio via microfone
- [ ] 🎯 Algoritmo de pontuação por áudio
- [ ] 📱 PWA para instalação como app
- [ ] 🎨 Melhorias de UX/UI
- [ ] 🗄️ Migração para banco de dados

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Yuri Rasch** - [@yurirasch](https://github.com/yurirasch)

---

**JingleTube** - Transformando karaokê em competição! 🎤🏆

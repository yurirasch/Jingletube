# Contribuindo para o JingleTube 🎤

Obrigado pelo interesse em contribuir! Este documento fornece diretrizes para contribuir com o projeto.

## 🚀 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
git clone https://github.com/seu-usuario/Jingletube.git
cd Jingletube
```

### 2. Crie um Branch

```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/meu-bugfix
```

### 3. Configuração do Ambiente

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
```

### 4. Faça suas Alterações

- Escreva código limpo e documentado
- Siga as convenções de estilo Python (PEP 8)
- Adicione testes para novas funcionalidades
- Atualize a documentação se necessário

### 5. Execute os Testes

```bash
# Execute todos os testes
pytest tests/ -v

# Verifique a cobertura
pytest tests/ --cov=src --cov-report=html
```

### 6. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
git push origin feature/minha-feature
```

### 7. Abra um Pull Request

- Descreva claramente o que foi alterado
- Referencie issues relacionadas
- Aguarde a revisão

## 📝 Convenções de Commit

Usamos Conventional Commits:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

## 🧪 Testes

- Adicione testes para novas funcionalidades
- Mantenha cobertura acima de 80%
- Teste em Python 3.9, 3.10 e 3.11

## 📚 Documentação

- Docstrings em todas as funções
- README atualizado
- Comentários em código complexo

## ❓ Dúvidas

Abra uma issue ou entre em contato!

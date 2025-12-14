# 🔐 Configuração do Cloudflare Access para JingleTube

Este guia mostra como configurar autenticação via Cloudflare Access para proteger seu JingleTube em produção.

## 📋 Pré-requisitos

- Domínio próprio configurado no Cloudflare
- Conta Cloudflare (gratuita ou paga)
- JingleTube deployado no Hugging Face Spaces
- Custom domain configurado (ver [CUSTOM_DOMAIN_HF.md](CUSTOM_DOMAIN_HF.md))

## 🚀 Passo a Passo

### 1. Acessar Cloudflare Zero Trust

1. Acesse [Cloudflare Dashboard](https://dash.cloudflare.com)
2. No menu lateral, clique em **Zero Trust**
3. Se for primeira vez, você precisará criar uma Team:
   - Escolha um nome único (ex: `jingletube-team`)
   - Isso criará um subdomínio: `jingletube-team.cloudflareaccess.com`

### 2. Configurar Identity Provider

O Cloudflare Access suporta múltiplos provedores de identidade. Vamos configurar os principais:

#### 2.1 Google OAuth (Recomendado)

1. No painel Zero Trust, vá em **Settings** → **Authentication**
2. Clique em **Add new** sob "Login methods"
3. Selecione **Google**
4. Configure:
   - **App ID**: Seu Google Client ID
   - **Client Secret**: Seu Google Client Secret

**Como obter credenciais do Google:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto (ou use existente)
3. Vá em **APIs & Services** → **Credentials**
4. Clique em **Create Credentials** → **OAuth client ID**
5. Tipo: **Web application**
6. **Authorized redirect URIs**: 
   ```
   https://jingletube-team.cloudflareaccess.com/cdn-cgi/access/callback
   ```
7. Copie o Client ID e Client Secret

#### 2.2 GitHub OAuth

1. No Zero Trust, adicione **GitHub** como provider
2. **Client ID** e **Client Secret** do GitHub OAuth App

**Como obter credenciais do GitHub:**
1. Acesse [GitHub Developer Settings](https://github.com/settings/developers)
2. Clique em **New OAuth App**
3. Preencha:
   - **Application name**: JingleTube Auth
   - **Homepage URL**: `https://seu-dominio.com`
   - **Authorization callback URL**: 
     ```
     https://jingletube-team.cloudflareaccess.com/cdn-cgi/access/callback
     ```
4. Copie o Client ID e gere um Client Secret

#### 2.3 Email OTP (One-Time Password)

1. Adicione **One-time PIN** como provider
2. Configure email domains permitidos (opcional)
3. Usuários receberão código via email

### 3. Criar Access Application

Agora vamos proteger sua aplicação JingleTube:

1. No Zero Trust, vá em **Access** → **Applications**
2. Clique em **Add an application**
3. Selecione **Self-hosted**
4. Configure:

**Application Configuration:**
```yaml
Name: JingleTube
Session Duration: 24 hours
Application Domain: 
  - jingletube.seu-dominio.com
```

**Application Appearance:**
```yaml
App Launcher visibility: Visible
Custom logo: (opcional - upload do logo JingleTube)
```

5. Clique em **Next**

### 4. Configurar Políticas de Acesso

#### 4.1 Política: Acesso Público com Autenticação

Para permitir que qualquer pessoa autenticada acesse:

```yaml
Policy name: Public Access
Action: Allow
Session duration: 24 hours

Include rules:
  - Selector: Emails
    Value: (deixar vazio para permitir todos)
    
  - OU Selector: Login Methods
    Value: Google, GitHub, One-time PIN
```

#### 4.2 Política: Acesso Restrito por Domínio

Para limitar a domínios específicos (ex: empresa, universidade):

```yaml
Policy name: Domain Restricted
Action: Allow

Include rules:
  - Selector: Emails ending in
    Value: @sua-empresa.com
```

#### 4.3 Política: Acesso por Lista de Emails

Para lista específica de usuários:

```yaml
Policy name: Whitelist
Action: Allow

Include rules:
  - Selector: Emails
    Value: 
      - usuario1@email.com
      - usuario2@email.com
      - usuario3@email.com
```

#### 4.4 Exemplo de Política Completa

```yaml
Name: JingleTube Access Policy
Action: Allow
Session Duration: 24 hours

Include:
  - Emails ending in: @empresa.com
  - OR Login Methods: Google, GitHub

Exclude:
  - Email: bloqueado@empresa.com

Require:
  - (opcional) Country: Brazil
```

6. Clique em **Next** e depois **Add application**

### 5. Configurar DNS

Agora você precisa apontar seu domínio para o Cloudflare Access:

1. No Cloudflare Dashboard, vá em **DNS**
2. Adicione ou edite o registro:

```
Type: CNAME
Name: jingletube (ou @ para domínio raiz)
Content: seu-space.hf.space
Proxy status: Proxied (nuvem laranja ativada) ✓
```

**IMPORTANTE:** O status "Proxied" deve estar ativado (nuvem laranja) para o Access funcionar!

### 6. Verificar Configuração

1. Acesse `https://jingletube.seu-dominio.com`
2. Você deve ser redirecionado para tela de login do Cloudflare Access
3. Faça login com um dos métodos configurados
4. Após autenticação, você será redirecionado para o JingleTube

### 7. Configuração Avançada

#### 7.1 Service Tokens (para APIs)

Se você precisa acesso programático:

1. Vá em **Access** → **Service Auth** → **Service Tokens**
2. Clique em **Create Service Token**
3. Nomeie: `JingleTube API Token`
4. Copie o Client ID e Client Secret (só aparecem uma vez!)
5. Use nos headers HTTP:
   ```
   CF-Access-Client-Id: <client-id>
   CF-Access-Client-Secret: <client-secret>
   ```

#### 7.2 Bypass para Caminhos Específicos

Se precisar que certas rotas sejam públicas (ex: `/health`, `/api/status`):

1. Crie uma nova Policy
2. Configure:
   ```yaml
   Name: Bypass Health Check
   Action: Bypass
   
   Include:
   - Path: /health
   ```

#### 7.3 Session Duration por Grupo

Configure durações diferentes:
- Usuários normais: 8 horas
- Admins: 24 horas

Use múltiplas policies com diferentes critérios.

### 8. Integração com Hugging Face Spaces

O Cloudflare Access funciona como proxy reverso, então:

1. Seu Space continua público em `seu-space.hf.space`
2. Mas o acesso via domínio customizado `jingletube.seu-dominio.com` é protegido
3. Configure no Space apenas o domínio customizado para forçar autenticação

**Variáveis de Ambiente no HF Space:**

```bash
# .env no Hugging Face Spaces
OAUTH_CLIENT_ID=cloudflare_access
OAUTH_CLIENT_SECRET=not_needed_with_cf_access
APP_URL=https://jingletube.seu-dominio.com
```

### 9. Headers de Autenticação

O Cloudflare Access adiciona headers com informações do usuário:

```python
# No seu código Python, você pode ler:
cf_access_authenticated_user_email = request.headers.get('Cf-Access-Authenticated-User-Email')
```

Headers disponíveis:
- `Cf-Access-Authenticated-User-Email`: Email do usuário
- `Cf-Access-Jwt-Assertion`: JWT token

### 10. Troubleshooting

#### Erro: "Access Denied"
- Verifique se sua política está configurada corretamente
- Confirme que o email/método de login está incluído nas regras

#### Erro: "Too Many Redirects"
- Verifique se o proxy está ativado no DNS (nuvem laranja)
- Limpe cookies e cache do navegador

#### Usuário não consegue fazer login
- Verifique se o Identity Provider está configurado corretamente
- Confirme as callback URLs no provider (Google/GitHub)

#### App não carrega após login
- Verifique se o domínio customizado está funcionando sem Access
- Teste diretamente em `seu-space.hf.space`

### 11. Monitoramento

1. Vá em **Logs** → **Access** para ver:
   - Logins bem-sucedidos
   - Tentativas bloqueadas
   - Usuários ativos

2. Configure alertas:
   - **Analytics** → **Notifications**
   - Alertas para acessos bloqueados excessivos

### 12. Melhores Práticas

✅ **Recomendado:**
- Use Google OAuth para usuários finais (fácil e confiável)
- Configure múltiplos providers como backup
- Session duration de 8-24h para melhor UX
- Monitore logs regularmente
- Use listas de email para controle granular

❌ **Evite:**
- Session duration muito curta (frustra usuários)
- Deixar políticas muito permissivas
- Usar apenas Email OTP (pode ir para spam)
- Expor diretamente o Space sem domínio customizado

### 13. Custos

- **Cloudflare Zero Trust Free:**
  - Até 50 usuários
  - Unlimited applications
  - Basic Identity Providers
  - Perfeito para MVP e projetos pequenos

- **Cloudflare Zero Trust Paid:**
  - A partir de $7/usuário/mês
  - Mais Identity Providers
  - Advanced features

### 14. Exemplo Completo

**Cenário:** JingleTube para empresa com 30 funcionários

1. **Identity Provider:** Google OAuth (domínio corporativo)
2. **Access Application:**
   - Domain: `karaoke.empresa.com`
   - Session: 24h
3. **Policy:**
   ```yaml
   Include:
   - Emails ending in: @empresa.com
   ```
4. **DNS:**
   ```
   CNAME: karaoke → seu-space.hf.space (Proxied ✓)
   ```

Resultado: Apenas funcionários com email `@empresa.com` conseguem acessar!

---

## 📚 Recursos Adicionais

- [Cloudflare Access Docs](https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/self-hosted-apps/)
- [Identity Providers](https://developers.cloudflare.com/cloudflare-one/identity/idp-integration/)
- [Access Policies](https://developers.cloudflare.com/cloudflare-one/policies/access/)

## 💡 Dúvidas?

Abra uma issue no repositório ou consulte a documentação oficial do Cloudflare Zero Trust.

---

**JingleTube** - Autenticação profissional para seu karaokê! 🎤🔐

# 🌐 Configurar Domínio Customizado no Hugging Face Spaces

Este guia mostra como configurar um domínio customizado para seu JingleTube no Hugging Face Spaces.

## 📋 Pré-requisitos

- Conta no Hugging Face (gratuita)
- JingleTube deployado em um Space
- Domínio próprio registrado (ex: GoDaddy, Namecheap, Cloudflare)
- Acesso ao painel de DNS do seu domínio

## 🎯 Visão Geral

Por padrão, seu Space tem URL: `https://seu-usuario-jingletube.hf.space`

Com domínio customizado, você terá: `https://jingletube.seu-dominio.com`

## 🚀 Passo a Passo

### 1. Verificar Espaço no Hugging Face

1. Acesse [Hugging Face Spaces](https://huggingface.co/spaces)
2. Entre no seu Space JingleTube
3. Confirme que está funcionando corretamente
4. Anote a URL do Space: `seu-usuario-jingletube.hf.space`

### 2. Configurar Domínio Customizado no HF

1. No seu Space, clique em **Settings** (⚙️)
2. Role até a seção **Custom Domain**
3. Clique em **Add a custom domain**
4. Digite seu domínio ou subdomínio:
   - Domínio completo: `jingletube.com`
   - Ou subdomínio: `karaoke.meusite.com`
5. Clique em **Add**

O Hugging Face mostrará as configurações de DNS necessárias.

### 3. Configurar DNS

Agora você precisa configurar o DNS do seu domínio. As instruções variam por provedor:

#### 3.1 Usando Cloudflare (Recomendado)

**Por que Cloudflare?**
- ✅ Gratuito
- ✅ Proxy/CDN incluído
- ✅ SSL/TLS automático
- ✅ Integração com Cloudflare Access para autenticação

**Passo a passo:**

1. Acesse [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Selecione seu domínio
3. Vá em **DNS** → **Records**
4. Clique em **Add record**
5. Configure:

```
Type: CNAME
Name: jingletube (ou @ para domínio raiz)
Target: seu-usuario-jingletube.hf.space
Proxy status: Proxied (nuvem laranja ✓)
TTL: Auto
```

6. Clique em **Save**

**Importante:** 
- Mantenha o Proxy **ativado** (nuvem laranja) para melhor performance
- Se quiser usar Cloudflare Access, o proxy é obrigatório

#### 3.2 Usando Namecheap

1. Acesse [Namecheap Dashboard](https://ap.www.namecheap.com)
2. Vá em **Domain List** → Clique em **Manage** no seu domínio
3. Vá em **Advanced DNS**
4. Clique em **Add New Record**
5. Configure:

```
Type: CNAME Record
Host: jingletube (ou @ para domínio raiz)
Value: seu-usuario-jingletube.hf.space
TTL: Automatic
```

6. Clique em **Save All Changes**

**Observação:** Namecheap pode levar até 48h para propagar, mas geralmente é mais rápido (30min-2h).

#### 3.3 Usando GoDaddy

1. Acesse [GoDaddy](https://dcc.godaddy.com/manage/dns)
2. Encontre seu domínio e clique em **DNS**
3. Role até **Records** e clique em **Add**
4. Selecione tipo **CNAME**
5. Configure:

```
Type: CNAME
Name: jingletube (ou @ para domínio raiz)
Data: seu-usuario-jingletube.hf.space
TTL: 1 Hour
```

6. Clique em **Save**

**Nota:** GoDaddy não permite CNAME em domínio raiz (@). Use subdomínio (ex: `karaoke.seudominio.com`) ou configure como A record apontando para IP do HF.

#### 3.4 Usando Google Domains

1. Acesse [Google Domains](https://domains.google.com/registrar)
2. Selecione seu domínio
3. Vá em **DNS** no menu lateral
4. Role até **Custom resource records**
5. Configure:

```
Name: jingletube (ou deixe vazio para domínio raiz)
Type: CNAME
TTL: 1H
Data: seu-usuario-jingletube.hf.space
```

6. Clique em **Add**

#### 3.5 Usando Route 53 (AWS)

1. Acesse [Route 53 Console](https://console.aws.amazon.com/route53)
2. Vá em **Hosted Zones**
3. Selecione seu domínio
4. Clique em **Create Record**
5. Configure:

```
Record name: jingletube
Record type: CNAME
Value: seu-usuario-jingletube.hf.space
TTL: 300
Routing policy: Simple routing
```

6. Clique em **Create records**

### 4. Aguardar Propagação DNS

- **Tempo médio:** 15 minutos a 2 horas
- **Tempo máximo:** 48 horas (raro)

**Verificar propagação:**

Método 1 - Online:
1. Acesse [DNS Checker](https://dnschecker.org)
2. Digite seu domínio: `jingletube.seu-dominio.com`
3. Tipo: CNAME
4. Verifique se aponta para `seu-usuario-jingletube.hf.space`

Método 2 - Terminal:
```bash
# Linux/Mac
dig jingletube.seu-dominio.com

# Windows
nslookup jingletube.seu-dominio.com

# Verificar especificamente CNAME
dig jingletube.seu-dominio.com CNAME
```

### 5. Verificar Domínio no Hugging Face

1. Volte ao seu Space → **Settings** → **Custom Domain**
2. O status deve mudar de "Pending" para "Active"
3. Se ainda estiver pending, clique em **Verify** ou aguarde mais alguns minutos

### 6. Configurar SSL/TLS (Automático)

O Hugging Face provisiona automaticamente certificados SSL via Let's Encrypt.

**Verificar SSL:**
1. Acesse `https://jingletube.seu-dominio.com`
2. Clique no cadeado 🔒 na barra de endereço
3. Verifique se o certificado é válido

**Se houver erro de SSL:**
- Aguarde 10-30 minutos (provisão pode demorar)
- Tente acessar via http primeiro: `http://jingletube.seu-dominio.com`
- Limpe cache do navegador (Ctrl+Shift+Delete)

### 7. Redirecionar Domínio Raiz (Opcional)

Se você quer que `seu-dominio.com` redirecione para `jingletube.seu-dominio.com`:

**No Cloudflare:**
1. Crie uma Page Rule:
   - URL: `seu-dominio.com/*`
   - Setting: Forwarding URL (301 Permanent Redirect)
   - Destination: `https://jingletube.seu-dominio.com/$1`

**No Namecheap:**
1. Vá em **Advanced DNS**
2. Adicione URL Redirect Record:
   ```
   Type: URL Redirect Record
   Host: @
   Value: https://jingletube.seu-dominio.com
   ```

### 8. Configurar Variáveis de Ambiente

Atualize o arquivo de configuração no seu Space:

1. No HF Space, vá em **Settings** → **Variables and secrets**
2. Adicione ou atualize:

```bash
APP_URL=https://jingletube.seu-dominio.com
```

Isso garante que links gerados pela aplicação usem o domínio correto.

### 9. Testar Tudo

Checklist de verificação:

- [ ] Domínio carrega corretamente
- [ ] SSL/HTTPS funcionando (cadeado verde)
- [ ] Redirecionamento HTTP → HTTPS automático
- [ ] Aplicação funciona normalmente
- [ ] Login/Logout funcionando
- [ ] Persistência de dados OK
- [ ] Performance adequada

### 10. Troubleshooting

#### Problema: "DNS_PROBE_FINISHED_NXDOMAIN"

**Causa:** DNS não propagou ou configuração incorreta

**Solução:**
1. Verifique o registro CNAME no painel DNS
2. Aguarde mais tempo (até 48h)
3. Limpe cache DNS local:
   ```bash
   # Windows
   ipconfig /flushdns
   
   # Mac
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemd-resolve --flush-caches
   ```

#### Problema: "ERR_SSL_VERSION_OR_CIPHER_MISMATCH"

**Causa:** Certificado SSL ainda não foi provisionado

**Solução:**
1. Aguarde 30 minutos
2. Verifique se o domínio está verificado no HF
3. Tente acessar via HTTP primeiro
4. Entre em contato com suporte do HF se persistir

#### Problema: "Too Many Redirects"

**Causa:** Loop de redirecionamento (comum com Cloudflare)

**Solução:**
1. No Cloudflare, vá em **SSL/TLS** → **Overview**
2. Mude para **Full** ou **Full (Strict)**
3. Aguarde alguns minutos

#### Problema: Domínio não verifica no HF

**Causa:** CNAME não aponta corretamente

**Solução:**
1. Use `dig` ou `nslookup` para verificar
2. Certifique-se de apontar para `seu-usuario-jingletube.hf.space` (não só `hf.space`)
3. Remove qualquer proxy/redirecionamento temporariamente
4. Tente clicar em "Verify" novamente no HF

#### Problema: Performance ruim

**Causa:** DNS sem CDN ou servidor distante

**Solução:**
1. Use Cloudflare com proxy ativado (CDN gratuito)
2. Configure cache headers no seu app
3. Considere Cloudflare Workers para otimização

### 11. Domínio Raiz vs Subdomínio

**Subdomínio (Recomendado):**
```
karaoke.meusite.com → CNAME fácil de configurar
jingletube.empresa.com → Mais flexível
app.meudominio.com → Separação clara
```

**Domínio Raiz:**
```
meudominio.com → Pode precisar de A record
jingletube.com → Alguns DNS não suportam CNAME raiz
```

**Recomendação:** Use subdomínio para evitar problemas técnicos.

### 12. Configuração Avançada

#### 12.1 Múltiplos Domínios

Você pode configurar vários domínios apontando para o mesmo Space:

```
jingletube.com → Space
karaoke.empresa.com → Space
sing.app.com → Space
```

Todos funcionam simultaneamente!

#### 12.2 Wildcard Subdomain

Para aceitar qualquer subdomínio (ex: user1.jingletube.com, user2.jingletube.com):

**No DNS:**
```
Type: CNAME
Name: *
Target: seu-usuario-jingletube.hf.space
```

**No HF:** Adicione `*.jingletube.com` como custom domain

#### 12.3 Cloudflare Workers

Para adicionar lógica antes do HF Space:

```javascript
// Cloudflare Worker
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Adicione lógica customizada aqui
  // Ex: analytics, rate limiting, A/B testing
  
  return fetch(request)
}
```

### 13. Segurança

#### 13.1 HTTPS Only

Force HTTPS no Cloudflare:
1. **SSL/TLS** → **Edge Certificates**
2. Ative **Always Use HTTPS**

#### 13.2 HSTS

Ative HTTP Strict Transport Security:
1. No Cloudflare: **SSL/TLS** → **Edge Certificates** → **HSTS**
2. Configure:
   ```
   Max Age: 12 months
   Include subdomains: Yes
   Preload: Yes
   ```

#### 13.3 CAA Records

Especifique quais CAs podem emitir certificados:

```
Type: CAA
Name: @
Value: 0 issue "letsencrypt.org"
```

### 14. Monitoramento

#### 14.1 Uptime Monitoring

Use serviços gratuitos:
- [UptimeRobot](https://uptimerobot.com)
- [Pingdom](https://www.pingdom.com)
- [StatusCake](https://www.statuscake.com)

Configure alertas por email/SMS se o site cair.

#### 14.2 Analytics

Adicione analytics ao seu domínio:
- Google Analytics
- Plausible (privacy-focused)
- Cloudflare Web Analytics (gratuito)

### 15. Custos

**Domínio:**
- .com: ~$10-15/ano
- .app: ~$15-20/ano
- .io: ~$30-40/ano

**DNS/CDN:**
- Cloudflare: **Gratuito**
- Route 53: ~$0.50/mês + queries
- Google Domains: Incluído

**Hugging Face:**
- Custom Domain: **Gratuito** ✓
- Space hosting: **Gratuito** (tier gratuito)

**Total mínimo:** ~$10-15/ano (apenas domínio)

### 16. Exemplo Completo - Cloudflare

**Cenário:** Você quer `karaoke.meusite.com` apontando para JingleTube

**1. HF Space Settings:**
```
Custom Domain: karaoke.meusite.com
```

**2. Cloudflare DNS:**
```
Type: CNAME
Name: karaoke
Content: seu-usuario-jingletube.hf.space
Proxy: Proxied ✓
```

**3. Cloudflare SSL:**
```
Mode: Full (Strict)
Always Use HTTPS: On
```

**4. Aguardar:**
- DNS: ~15 minutos
- SSL: ~30 minutos

**5. Testar:**
```bash
curl -I https://karaoke.meusite.com
# Deve retornar 200 OK com SSL válido
```

**Pronto!** 🎉

---

## 📚 Recursos Adicionais

- [HF Docs - Custom Domains](https://huggingface.co/docs/hub/spaces-custom-domains)
- [Cloudflare DNS Docs](https://developers.cloudflare.com/dns/)
- [DNS Propagation Checker](https://dnschecker.org)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)

## 💡 Dicas

✅ **Recomendado:**
- Use Cloudflare (gratuito e poderoso)
- Configure SSL/TLS em Full (Strict)
- Ative Always Use HTTPS
- Use subdomínio em vez de domínio raiz
- Configure monitoring
- Teste em diferentes dispositivos

❌ **Evite:**
- Mudar configurações de DNS frequentemente
- Desativar proxy do Cloudflare (perde CDN)
- Usar domínio raiz sem necessidade
- Esquecer de renovar domínio

---

## 🎯 Próximos Passos

Depois de configurar o domínio customizado:

1. Configure [Cloudflare Access](CLOUDFLARE_ACCESS_SETUP.md) para autenticação
2. Adicione analytics e monitoring
3. Configure backup dos dados
4. Otimize performance com cache

---

**JingleTube** - Seu karaokê com domínio profissional! 🎤🌐

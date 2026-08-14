# 🚀 Roadmap — DarkNet Tools

**Autor:** Matheus Iasin  
**Atualizado:** 2025

---

## ✅ Concluído

### v1.0 — 2024
- [x] Interface gráfica TemPad (tkinter)
- [x] Script de otimização (optimize.py)
- [x] Diagnóstico de rede (network_diagnosis.py)
- [x] Verificação de disco (disk_check.py)
- [x] Verificação de segurança (security_scan.py)
- [x] Menu de rede no terminal (DarkNet_Tools.bat)
- [x] Painel completo de suporte (painel_suporte.bat)
- [x] Relatório de ping em massa (ping_report.ps1)
- [x] Verificador de dependências (setup.py)

### v2.0 — 2025
- [x] setup.py atualizado para Python 3.14+
- [x] Self_Healing.py comentado e atualizado
- [x] Pasta docs/ criada
- [x] Documentação completa (Histórico, Relatório, Roadmap)

---

## 🔄 Em Andamento

- [ ] Corrigir caminhos hardcoded no `main.py`
- [ ] Log em tempo real na GUI sem bloquear interface
- [ ] Submenus por categoria no `painel_suporte.bat`
- [ ] Validação de entrada no `painel_suporte.bat`
- [ ] Limpeza do `Prefetch` no `optimize.py`

---

## 📋 Planejado — v3.0

### Melhorias nos Scripts
- [ ] Exportar relatório de ping em `.html` e `.csv`
- [ ] Lista de IPs configurável via arquivo externo
- [ ] Log de execução no `painel_suporte.bat`
- [ ] Expandir `network_diagnosis.py` com IP, MAC, DNS e flush

### Executável Unificado
- [ ] Unificar tudo em `.exe` via PyInstaller
- [ ] Sem necessidade de instalar Python na máquina
- [ ] Ícone personalizado (tema TVA/laranja)

### Self-Healing Avançado
- [ ] Rodar como serviço Windows via NSSM
- [ ] Notificação por e-mail quando ocorrer auto-cura
- [ ] Dashboard de eventos curados
- [ ] Configuração de thresholds via arquivo externo

---

## 🔭 Futuro — v4.0

### IA em Segundo Plano
- [ ] Monitoramento inteligente com detecção de padrões
- [ ] Agir antes do problema acontecer (preditivo)
- [ ] Aprendizado com histórico de eventos
- [ ] Integração com Python + SSH (Netmiko/Paramiko)

### Automação de Redes Cisco
- [ ] Conectar em switches e roteadores via SSH
- [ ] Executar comandos remotamente
- [ ] Gerar relatório de status dos equipamentos
- [ ] Integração com estudos CCNA

### Interface Web
- [ ] Versão web do painel (HTML/CSS/JS)
- [ ] Dashboard em tempo real
- [ ] Tema laranja/TVA responsivo

---

## 💡 Ideias Futuras

- Sistema de tickets integrado ao painel
- Integração com Active Directory
- Relatórios automáticos por e-mail
- Suporte a múltiplos sites/filiais
- App mobile para monitoramento remoto

---

## 🎯 Contexto

Projeto desenvolvido para suporte técnico em **ambiente de alta criticidade** (aeroporto). A evolução natural é de ferramenta manual para sistema autônomo inteligente.

```
HOJE          → Ferramenta manual (técnico escolhe a ação)
v3.0          → Semi-autônomo (age quando detecta problema)
v4.0          → Totalmente autônomo (aprende e age sozinho)
```

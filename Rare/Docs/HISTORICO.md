# 📋 Histórico de Versões — DarkNet Tools

**Projeto:** DarkNet Tools  
**Autor:** Matheus Iasin  
**Área:** Suporte técnico · Redes · Automação Windows

---

## v2.0 — 2025

### setup.py
- Adicionada verificação de versão do Python
- Suporte oficial ao Python 3.14+
- Type hints em todas as funções
- Resumo final de instalação com contagem de pacotes
- Separação entre pacotes pip e builtin (tkinter)
- Histórico de versões documentado no topo do arquivo

### self_healing_v2.py
- Código totalmente comentado
- Migração para `pathlib` (Path) no lugar de `os.path`
- Type hints em todas as funções e variáveis
- Configurações centralizadas no topo do arquivo
- Módulo de impressão incluído na lista de serviços críticos
- Exibe espaço em disco antes e depois da limpeza
- Verifica sucesso do reinício de serviços
- Função `main()` como ponto de entrada separado
- Instruções de instalação como serviço Windows (NSSM) documentadas

### Estrutura
- Criada pasta `docs/` para documentação
- Adicionados: `HISTORICO.md`, `RELATORIO_TECNICO.md`, `ROADMAP.md`

---

## v1.0 — 2024

### TemPad (main.py)
- Interface gráfica com tkinter
- Tema escuro com verde neon (#00ff00)
- Inspirado no TemPad da série Loki (Marvel/Disney+)
- 4 botões com ícones GIF animados
- Área de log com ScrolledText
- Chama scripts externos via subprocess

### setup.py
- Verificação de dependências via `importlib.metadata`
- Instalação automática via pip
- Pacotes: pygame, playsound, requests, Pillow, psutil
- Tratamento especial para tkinter (builtin)

### scripts/optimize.py
- Limpeza de `%TEMP%`
- Limpeza de `C:\Windows\Temp`
- Esvazia Lixeira via PowerShell

### scripts/network_diagnosis.py
- Ping para `8.8.8.8`
- Traceroute para `8.8.8.8`

### scripts/disk_check.py
- Estrutura orientada a objetos (OOP)
- Classes: `Cor`, `Logger`, `ManutencaoSistema`, `Menu`
- Verificação de permissão de administrador
- Executa chkdsk, SFC e DISM
- Verifica saúde do HD/SSD via WMIC
- Log com timestamp em `C:\manutencao_sistema.log`

### scripts/security_scan.py
- Executa `sfc /scannow`

### DarkNet_Tools.bat
- Menu interativo no terminal
- 9 opções de diagnóstico de rede
- ipconfig, ping, tracert, DNS flush, MAC, conexões ativas

### painel_suporte.bat
- Menu interativo completo
- 26 opções cobrindo todo o suporte técnico
- Categorias: Manutenção, Rede, Sistema, Administração
- Construído com uso real no ambiente de trabalho

### ping_report.ps1
- Lista de 51 IPs na subnet 10.3.40.x
- Ping em massa automatizado
- Gera `Relatorio_Ping.txt` no Desktop

---

## Linha do Tempo

```
2024 — v1.0
  └── TemPad GUI + scripts Python
  └── DarkNet_Tools.bat (9 opções)
  └── painel_suporte.bat (26 opções)
  └── ping_report.ps1

2025 — v2.0
  └── setup.py atualizado (Python 3.14+)
  └── self_healing_v2.py comentado
  └── Pasta docs/ criada
  └── Documentação completa
```

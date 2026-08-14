# 📊 Relatório Técnico — DarkNet Tools

**Autor:** Matheus Iasin  
**Início:** 2024  
**Versão atual:** 2.0  
**Status:** Pausado — base completa, pronto para evoluir

---

## 1. Visão Geral

Conjunto de ferramentas de suporte técnico desenvolvidas para automatizar tarefas repetitivas do dia a dia de TI, eliminando a necessidade de executar comandos manualmente.

### Inspiração
A interface gráfica foi inspirada no **TemPad da série Loki (Marvel/Disney+)** — um dispositivo compacto que executa ações poderosas com poucos cliques.

### Objetivo Final
Unificar todas as ferramentas em um executável único que qualquer técnico possa usar sem instalar nada.

---

## 2. Estrutura de Arquivos

```
DarkNet-Tools/
├── assets/
│   ├── hard-disk.gif
│   ├── network.gif
│   ├── optimization.gif
│   ├── safe.gif
│   └── task.gif
│
├── scripts/
│   ├── Self_Healing.py
│   ├── disk_check.py
│   ├── network_diagnosis.py
│   ├── optimize.py
│   └── security_scan.py
│
├── docs/
│   ├── HISTORICO.md
│   ├── RELATORIO_TECNICO.md
│   └── ROADMAP.md
│
├── main.py
├── setup.py
└── README.md
```

---

## 3. Detalhamento dos Arquivos

### main.py — Interface Gráfica
- GUI com tema laranja (TemPad/TVA)
- Botões com ícones GIF
- Log em tempo real

**Melhorias planejadas:**
- Caminhos hardcoded → `os.path.dirname(__file__)`
- Log em tempo real com `subprocess.Popen` + threads

---

### setup.py — Instalador de Dependências
- Verifica versão do Python (mínimo 3.10, recomendado 3.14+)
- Instala pacotes automaticamente via pip
- Exibe resumo de instalação
- Trata tkinter separadamente (builtin)

**Pacotes verificados:**
`psutil` · `Pillow` · `requests` · `pygame` · `playsound`

---

### scripts/Self_Healing.py — Auto-cura
Sistema autônomo que roda em segundo plano a cada 5 minutos:

| Módulo | Monitora | Ação |
|--------|----------|------|
| Impressão | Spooler parado | Limpa fila + reinicia |
| Disco | Acima de 90% | Limpa temp + prefetch + lixeira |
| Rede | Sem conectividade | Flush DNS + renova IP |
| Serviços | Serviço parado | Reinicia automaticamente |
| Memória | RAM acima de 90% | Lista top 5 processos no log |

---

### scripts/disk_check.py — Manutenção de Disco
- OOP com classes: `Cor`, `Logger`, `ManutencaoSistema`, `Menu`
- Verifica permissão de administrador
- Executa chkdsk, SFC e DISM
- Log com timestamp em `C:\manutencao_sistema.log`

---

### scripts/network_diagnosis.py — Diagnóstico de Rede
- Ping para `8.8.8.8`
- Traceroute para `8.8.8.8`

---

### scripts/optimize.py — Otimização
- Limpa `%TEMP%` e `C:\Windows\Temp`
- Esvazia Lixeira

---

### scripts/security_scan.py — Segurança
- Executa `sfc /scannow`

---

### DarkNet_Tools.bat — Diagnóstico de Rede
Menu com 9 opções: IP, DNS, Ping, Tracert, MAC, conexões ativas.

---

### painel_suporte.bat — Suporte Completo
Menu com 26 opções divididas em categorias:
- **Manutenção:** SFC, DISM, chkdsk, cleanmgr, reset Windows Update
- **Rede:** ipconfig, flush DNS, ping, velocidade
- **Sistema:** msinfo32, devmgmt, tasklist, serviços, USB, RAM
- **Administração:** GPO, logs, backup, PowerShell, impressora

---

### ping_report.ps1 — Ping em Massa
- 51 IPs na subnet 10.3.40.x
- Gera `Relatorio_Ping.txt` no Desktop

---

## 4. Tecnologias Utilizadas

| Tecnologia | Uso |
|-----------|-----|
| Python 3.14+ | Scripts de automação e GUI |
| tkinter | Interface gráfica |
| psutil | Disco, RAM, processos |
| subprocess | Execução de comandos |
| pathlib | Manipulação de caminhos |
| Batch (.bat) | Menus de terminal |
| PowerShell | Automação em massa |

---

## 5. Fluxo do Sistema

```
TÉCNICO ABRE O TEMPAD
        │
        ├── Executa setup.py ──────► Verifica Python + instala pacotes
        │
        └── Executa main.py ───────► Abre interface gráfica
                │
                ├── Verificar Disco ──► disk_check.py
                ├── Otimizar PC ──────► optimize.py
                ├── Diagnóstico Rede ► network_diagnosis.py
                └── Segurança ────────► security_scan.py

EM SEGUNDO PLANO (independente)
        └── Self_Healing.py ───────► Monitora e corrige automaticamente
```

---

## 6. Contexto de Uso

Desenvolvido para uso em **ambiente corporativo de alta criticidade** (aeroporto), onde:
- Impressoras de cartão de embarque não podem travar
- Rede precisa estar sempre disponível
- Técnico nem sempre está disponível imediatamente
- Agilidade no suporte é essencial

**Linguagens:** Python · Batch · PowerShell  
**Área:** Suporte técnico · Redes · Automação  
**Inspiração:** TemPad — Loki (Marvel/Disney+)

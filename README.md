# 🖥️ DarkNet Tools — Ferramentas de Suporte e Diagnóstico

**Criado por:** Matheus Iasin  
**Início:** 2024  
**Status:** Em evolução — base pronta, próxima etapa: unificar em executável

---

## 💡 Ideia Central

Um painel central que execute ações de suporte de TI de forma rápida e automatizada, sem precisar fazer tudo na mão.

O projeto nasceu como uma GUI em Python (TemPad), evoluiu para scripts de terminal ágeis em Batch e PowerShell, e no futuro será unificado em um executável profissional.

---

## 📁 Estrutura do Projeto

```
DarkNet-Tools/
├── assets/                    # Ícones da interface gráfica
│   ├── hard-disk.gif
│   ├── optimization.gif
│   ├── network.gif
│   └── safe.gif
│
├── scripts/                   # Scripts Python do TemPad
│   ├── optimize.py            # Limpeza de temporários e lixeira
│   ├── network_diagnosis.py   # Diagnóstico de rede (ping, tracert)
│   ├── disk_check.py          # Verificação e manutenção de disco
│   └── security_scan.py       # Verificação de arquivos (SFC)
│
├── tempad.py                  # Interface gráfica principal (tkinter)
├── DarkNet_Tools.bat          # Menu de diagnóstico de rede (9 opções)
├── painel_suporte.bat         # Painel completo de suporte (26 opções)
├── ping_report.ps1            # Relatório de ping em massa (PowerShell)
└── check_dependencies.py      # Verificador/instalador de dependências
```

---

## 🧩 Scripts — O que cada um faz

### 🖥️ tempad.py — Interface Gráfica Central
- GUI com tema laranja (inspirado no TemPad da série Loki/TVA)
- Botões com ícones para executar cada script
- Log em tempo real da execução

**⚠️ Melhorias planejadas:**
- Substituir caminhos hardcoded por `os.path.dirname(__file__)`
- Atualizar log em tempo real sem bloquear a GUI

---

### 🌐 DarkNet_Tools.bat — Diagnóstico de Rede no Terminal
Menu interativo com 9 opções:
1. Mostrar IP
2. Mostrar IP detalhado
3. Renovar IP
4. Limpar Cache DNS
5. Testar Ping
6. Traçar Rota
7. Conexões Ativas
8. Mostrar MAC Address
9. Diagnóstico Rápido

**Vantagem:** Roda em qualquer máquina Windows sem dependências.

---

### 🛠️ painel_suporte.bat — Painel Completo de Suporte (26 opções)
Menu interativo completo para suporte técnico no dia a dia:

**Manutenção do Sistema**
- Limpeza de arquivos temporários
- Limpeza de disco (cleanmgr)
- Verificação de arquivos do sistema (SFC)
- Reparo da imagem do Windows (DISM)
- Reset do Windows Update
- CHKDSK no disco C:

**Rede**
- Reset de configurações de rede
- Verificar ipconfig
- Testar conectividade com o Google
- Testar velocidade da internet (fast.com)

**Sistema e Informações**
- Informações do sistema (msinfo32)
- Gerenciador de dispositivos
- Ver adaptadores de rede
- Ver programas instalados
- Ver processos em execução
- Status dos principais serviços
- Verificar espaço em disco
- Verificar status do antivírus
- Visualizar dispositivos USB
- Ver uso de memória e CPU

**Administração**
- Atualização de políticas de grupo (GPO)
- Limpeza de logs de eventos
- Backup dos logs de eventos
- Abrir PowerShell
- Instalar impressora / Abrir driver

**Vantagem:** Construído com uso real no trabalho — cada opção resolve um problema do dia a dia de suporte.

---

### 📡 ping_report.ps1 — Relatório de Ping em Massa
- Recebe uma lista de IPs
- Faz ping em todos automaticamente
- Gera `Relatorio_Ping.txt` no Desktop

**⚠️ Melhorias planejadas:**
- Exportar em `.csv` ou `.html`
- Tornar a lista de IPs configurável via arquivo externo

---

### 💿 disk_check.py — Manutenção de Disco
- Estrutura orientada a objetos
- Verifica permissões de administrador
- Executa `chkdsk`, `SFC` e `DISM`
- Verifica saúde física do HD/SSD
- Gera log com timestamp

---

### 🌐 network_diagnosis.py — Diagnóstico de Rede
- Ping para `8.8.8.8`
- Traceroute para `8.8.8.8`

---

### ⚡ optimize.py — Otimização do Sistema
- Limpa pasta `%TEMP%`
- Limpa `C:\Windows\Temp`
- Esvazia a Lixeira

---

### 🔒 security_scan.py — Verificação de Segurança
- Executa `sfc /scannow` para verificar arquivos corrompidos

---

### 📦 check_dependencies.py — Verificador de Dependências
- Verifica e instala pacotes necessários automaticamente

---

## 🔗 Como os projetos se conectam

```
IDEIA CENTRAL: Painel de suporte automatizado
        │
        ├── tempad.py (GUI) ────────► Interface visual, chama os scripts
        │       └── scripts/        ► optimize, network, disk, security
        │
        ├── DarkNet_Tools.bat ──────► Diagnóstico de rede rápido (9 opções)
        │
        ├── painel_suporte.bat ─────► Suporte completo no terminal (26 opções)
        │
        ├── ping_report.ps1 ────────► Automação em massa, relatório de IPs
        │
        └── PRÓXIMO PASSO ──────────► Executável unificado
```

---

## 📊 Evolução do Projeto

| Versão | Script | Linguagem | Opções |
|--------|--------|-----------|--------|
| v1 | tempad.py | Python + tkinter | 4 módulos |
| v2 | DarkNet_Tools.bat | Batch | 9 opções |
| v3 | painel_suporte.bat | Batch | 26 opções |
| v3 | ping_report.ps1 | PowerShell | Relatório IPs |
| v1 | disk_check.py | Python OOP | 5 módulos |

---

## 🚀 Próximos Passos

- [ ] Corrigir caminhos hardcoded no `tempad.py`
- [ ] Melhorar log em tempo real na GUI
- [ ] Exportar relatório de ping em `.html` ou `.csv`
- [ ] Tornar lista de IPs configurável via arquivo externo
- [ ] Unificar tudo em um executável único
- [ ] Comentar todos os scripts detalhadamente
- [ ] Explorar automação com Python + SSH (Netmiko/Paramiko) para equipamentos Cisco

---

## 🎯 Contexto

Ferramentas desenvolvidas para suporte técnico no dia a dia, com foco em diagnóstico de redes e manutenção de sistemas Windows. Cada opção foi adicionada conforme problemas reais foram encontrados no trabalho.

**Linguagens:** Python · Batch · PowerShell  
**Área:** Suporte técnico · Redes · Automação  
**Inspiração visual:** TemPad — Loki (Marvel/Disney+)

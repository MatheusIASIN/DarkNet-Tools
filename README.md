
```markdown
# 🖥️ DarkNet Tools — TemPad (TVA Support & Diagnostic Suite)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/Status-Em%20Evolu%C3%A7%C3%A3o-orange?style=for-the-badge)](#-evolu%C3%A7%C3%A3o-do-projeto)

**Criado por:** [Matheus Iasin](https://github.com/MatheusIASIN)  
**Início:** 2024  
**Versão Atual:** v3.3 (Web CRT & Audio FX)  

---

## 📸 Interface TemPad Web

![TemPad Web CRT Interface](docs/tempad_preview.png)
*> Interface Web estilo TVA com efeito CRT âmbar, barra de status animada e feedback sonoro via Web Audio API.*

---

## 💡 Ideia Central

Um painel central de suporte e diagnóstico de TI de alta performance, projetado para automação de rotinas de manutenção de sistemas Windows e redes, reduzindo drasticamente o tempo de atendimento técnico.

O projeto nasceu como uma GUI local em Python (Tkinter), expandiu-se com scripts ágeis em Batch e PowerShell para o terminal do Windows, e agora evoluiu para uma **interface web responsiva com estética retrofuturista estilo TVA (TemPad - Marvel/Loki)** com efeitos visuais CRT e efeitos sonoros gerados via Web Audio API.

---

## 🚀 Principais Destaques (v3.3)

- 🎛️ **Interface TemPad Web:** Painel web construído em **Flask** e **Bootstrap 5** com iluminação âmbar, scanlines CRT e estética de terminal analógico.
- 🔊 **Web Audio API Synth:** Efeitos sonoros retrô sintetizados diretamente pelo navegador (sem dependência de arquivos `.mp3`/`.wav` externos).
- 📊 **Monitor de Progresso:** Barras de status animadas e execução de diagnósticos em tempo real.
- ⚡ **Scripts Autônomos:** Suporte nativo a tarefas de disco, limpeza de temporários, verificação de integridade (SFC/DISM) e diagnósticos de rede.

---

## 📁 Estrutura do Repositório

```text
DarkNet-Tools/
├── Rare/                      # Módulo Principal Web (TemPad v3.3)
│   ├── main_web.py            # Servidor Flask, rotas e interface CRT/Áudio
│   ├── main.py                # Interface gráfica desktop legada (Tkinter)
│   ├── disk_check.py          # Verificação e saúde de disco
│   ├── optimize.py            # Otimização e limpeza de temporários
│   ├── network_diagnosis.py   # Diagnóstico de rede (ping, traceroute)
│   └── security_scan.py       # Verificação de integridade (SFC)
│
├── scripts/                   # Scripts auxiliares do projeto
│   ├── tempad.py              # Interface legada alternativa
│   └── check_dependencies.py  # Verificador/instalador de dependências
│
├── DarkNet_Tools.bat          # Menu rápido de diagnóstico de rede (9 opções)
├── painel_suporte.bat         # Painel completo de suporte no terminal (26 opções)
└── ping_report.ps1            # Relatório de ping em massa (PowerShell)

```

---

## 🧩 Componentes do Sistema

### 🌐 1. TemPad Web (`Rare/main_web.py`)

* **Web Console CRT:** Interface web inspirada nos monitores analógicos da Autoridade de Variância Temporal (TVA).
* **Som Sintetizado:** Feedback sonoro ao interagir com botões e durante o carregamento de diagnósticos.
* **Painel Responsivo:** Compatível com telas desktop e dispositivos móveis.

### 🛠️ 2. Módulos Python de Diagnóstico (`Rare/`)

* **`disk_check.py`:** Automação para `chkdsk`, saúde física do disco e verificação de permissões de administrador.
* **`optimize.py`:** Limpeza profunda de diretórios temporários (`%TEMP%`, `C:\Windows\Temp`) e esvaziamento da lixeira.
* **`network_diagnosis.py`:** Teste de latência (ping) e traçamento de rota (traceroute).
* **`security_scan.py`:** Verificação de integridade do sistema operacional com `sfc /scannow`.

### 🖥️ 3. Scripts de Terminal e Automação

* **`painel_suporte.bat`:** Menu com 26 opções abrangendo manutenção de sistema, reparo de Windows Update, configurações de rede, GPO e ferramentas de administração.
* **`DarkNet_Tools.bat`:** Menu rápido com 9 funções focadas exclusivamente em diagnóstico de rede.
* **`ping_report.ps1`:** Script PowerShell para varredura de múltiplos IPs e geração de relatório em texto no Desktop.

---

## 📊 Evolução do Projeto

| Versão | Módulo / Script | Tecnologia | Foco / Recursos |
| --- | --- | --- | --- |
| **v1.0** | `tempad.py` | Python + Tkinter | Interface gráfica desktop inicial |
| **v2.0** | `DarkNet_Tools.bat` | Batch Script | Diagnóstico ágil de rede via terminal |
| **v3.0** | `painel_suporte.bat` | Batch Script | Suporte completo de TI (26 funções) |
| **v3.1** | `ping_report.ps1` | PowerShell | Varredura de latência em massa |
| **v3.2** | `disk_check.py` | Python (OOP) | Verificação robusta de integridade física e lógica |
| **v3.3** | **TemPad Web** | Flask + Bootstrap 5 + JS Audio | UI Web CRT, efeitos sonoros sintetizados e execução web |

---

## 🛠️ Como Executar o TemPad Web

1. **Clone o repositório:**
```bash
git clone [https://github.com/MatheusIASIN/DarkNet-Tools.git](https://github.com/MatheusIASIN/DarkNet-Tools.git)
cd DarkNet-Tools

```


2. **Instale as dependências:**
```bash
pip install flask

```


3. **Inicie o servidor:**
```bash
python Rare/main_web.py

```


4. **Acesse no navegador:**
Abra `http://localhost:5000` (ou utilize a porta encaminhada no GitHub Codespaces).

---

## 🎯 Próximos Passos & Roadmap

* [x] Unificar módulos Python em servidor web com Flask
* [x] Adicionar estilização CRT e suporte ao Bootstrap 5
* [x] Implementar efeitos sonoros com Web Audio API
* [ ] Implementar streaming de log em tempo real via SSE (Server-Sent Events)
* [ ] Limpeza/formatação HTML dos códigos de escape ANSI do terminal
* [ ] Exportar relatórios de diagnóstico em `.pdf` / `.html`
* [ ] Empacotar a aplicação web como executável standalone (`PyInstaller`)

---

## 📜 Licença e Créditos

Desenvolvido por **[Matheus Iasin](https://github.com/MatheusIASIN)** como ferramenta de uso real em rotinas de suporte técnico e infraestrutura.

*Inspiração estética:* TemPad / TVA (Time Variance Authority) da série Loki (Marvel Studios).

```

```

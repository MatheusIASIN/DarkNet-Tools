#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 TIME VARIANCE AUTHORITY — NEXUS INSTALLATION ENGINE (nexus_setup.py)
 -----------------------------------------------------------------------------
 Módulo de Bootstrap Nativo, Diagnóstico de Hardware & Auto-Launch do TemPad.
 100% Python Standard Library — Zero Dependências Prévias.
===============================================================================
"""

import os
import sys
import time
import random
import string
import platform
import subprocess
import ctypes
import importlib.util
import shutil
import webbrowser
import threading

# Módulo Winreg condicional (Windows)
if os.name == 'nt':
    try:
        import winreg
    except ImportError:
        winreg = None

# ---------------------------------------------------------------------------
# Suporte ANSI no Windows Terminal / CMD / PowerShell
# ---------------------------------------------------------------------------
def setup_terminal() -> None:
    """Habilita Virtual Terminal Processing para cores ANSI no Windows."""
    if os.name == 'nt':
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

setup_terminal()

# Paleta de Cores TemPad / TVA (ANSI)
CLR_AMBER  = "\033[38;2;255;136;0m"     # Âmbar neon clássico
CLR_BRIGHT = "\033[38;2;255;180;0m"     # Âmbar brilhante para destaques
CLR_GREEN  = "\033[38;2;50;205;50m"     # Verde confirmação
CLR_RED    = "\033[38;2;255;68;68m"      # Vermelho alerta Nexus
CLR_DIM    = "\033[38;2;130;75;0m"      # Bronze / Âmbar escuro para bordas
CLR_CYAN   = "\033[38;2;0;200;255m"     # Ciano destaques
CLR_RESET  = "\033[0m"

# ---------------------------------------------------------------------------
# Módulos Necessários no Stack
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn[standard]"),
    ("websockets", "websockets"),
    ("pydantic", "pydantic"),
    ("dotenv", "python-dotenv"),
    ("shapely", "shapely"),
    ("redis", "redis"),
    ("requests", "requests"),
    ("psutil", "psutil"),
    ("PIL", "Pillow"),
]

# ---------------------------------------------------------------------------
# Código Embutido do App Web (Garantia de Autocriação)
# ---------------------------------------------------------------------------
AETHER_NEXUS_APP_CODE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 AETHERNEXUS-CHRONOS — TEMPAD WEB APP (aether_nexus_app.py)
===============================================================================
"""

import os
import sys
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(
    title="AetherNexus TemPad Web OS",
    description="Autoridade de Variância Temporal — Painel de Controle Autônomo",
    version="3.3-CHRONOS"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

SCRIPT_MAP = {
    'disk': 'disk_check.py',
    'optim': 'optimize.py',
    'net': 'network_diagnosis.py',
    'sec': 'security_scan.py',
}

def inicializar_scripts_demo():
    for modulo, nome_script in SCRIPT_MAP.items():
        caminho = os.path.join(SCRIPTS_DIR, nome_script)
        if not os.path.exists(caminho):
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(
                    "import time\\n"
                    f"print('>>> [CHRONOS] Iniciando módulo {modulo.upper()}...')\\n"
                    "for i in range(1, 6):\\n"
                    "    print(f'   Analisa linha temporal... passo {i}/5')\\n"
                    "    time.sleep(0.4)\\n"
                    "print('>>> [OK] Varredura concluída sem anomalias.')\\n"
                )

inicializar_scripts_demo()

HTML_INTERFACE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AETHERNEXUS-CHRONOS — TemPad OS</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #080400; font-family: 'VT323', monospace; display: flex;
    justify-content: center; align-items: center; min-height: 100vh;
    user-select: none; overflow: hidden;
  }
  .device {
    background: linear-gradient(160deg, #b85000, #5c2400); border-radius: 32px;
    padding: 6px; width: 100%; max-width: 480px; box-shadow: 0 0 0 2px #e87a20, 0 8px 40px rgba(0,0,0,0.9);
  }
  .inner { background: #140b00; border-radius: 27px; padding: 20px; border: 1px solid #3a1c00; }
  .logo { font-size: 22px; font-weight: bold; color: #ff9933; letter-spacing: 3px; text-shadow: 0 0 8px rgba(255, 153, 51, 0.8); }
  .status { font-size: 13px; color: #b35000; text-align: right; line-height: 1.2; }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: #ff8800; display: inline-block; animation: blink 1.8s infinite; box-shadow: 0 0 6px #ff8800; }
  @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.2; } }
  .timeline-container { position: relative; width: 100%; height: 48px; background: #050200; border: 1px solid #ff880044; border-radius: 8px; margin-bottom: 8px; overflow: hidden; }
  #chronosCanvas { width: 100%; height: 100%; display: block; }
  .screen {
    position: relative; background: #050200; border-radius: 12px; border: 1px solid #ff880055;
    padding: 12px; height: 170px; overflow-y: auto; font-size: 15px; letter-spacing: 1px; color: #ff9900;
    line-height: 1.3; text-shadow: 0 0 5px rgba(255, 136, 0, 0.8); box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.95);
    white-space: pre-wrap; word-break: break-all;
  }
  .screen::after {
    content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.35) 50%); background-size: 100% 4px; pointer-events: none; opacity: 0.6;
  }
  .screen::-webkit-scrollbar { width: 4px; }
  .screen::-webkit-scrollbar-thumb { background: #5a3000; border-radius: 2px; }
  .progress-tva { background-color: #080300; border: 1px solid #5a3000; height: 18px; border-radius: 6px; }
  .progress-bar-tva { background-color: #ff8800; color: #140b00; font-weight: bold; font-family: 'VT323', monospace; font-size: 14px; box-shadow: 0 0 8px #ff8800; }
  .btn-tempad {
    background: #1f0f00; border: 1px solid #5a3000; border-radius: 12px; padding: 10px 6px;
    color: #ff9933; font-family: 'VT323', monospace; font-size: 16px; letter-spacing: 1px; cursor: pointer; transition: all 0.15s; width: 100%;
  }
  .btn-tempad:hover { background: #2e1800; border-color: #ff8800; color: #ffaa44; box-shadow: 0 0 10px rgba(255, 136, 0, 0.3); }
  .btn-tempad:active { transform: scale(0.97); }
  .running { border-color: #ff8800 !important; background: #3a1a00 !important; animation: pulse-btn 0.9s infinite alternate; }
  @keyframes pulse-btn { from { box-shadow: 0 0 4px rgba(255, 136, 0, 0.3); } to { box-shadow: 0 0 16px rgba(255, 136, 0, 0.9); } }
  .btn-sub { color: #884400; font-size: 12px; }
  .btn-exit { width: 100%; background: #2a0a00; border: 1px solid #6a2000; border-radius: 12px; padding: 8px; color: #ff4400; font-family: 'VT323', monospace; font-size: 16px; letter-spacing: 2px; text-shadow: 0 0 4px rgba(255, 68, 0, 0.5); }
  .btn-exit:hover { background: #3a1500; border-color: #ff4400; color: #ff6622; }
  .divider { height: 1px; background: #3a1800; margin: 10px 0; }
  .dot-sm { width: 7px; height: 7px; border-radius: 50%; background: #5a3000; }
  .dot-sm.active { background: #ff8800; animation: blink 2s infinite; box-shadow: 0 0 4px #ff8800; }
</style>
</head>
<body onclick="garantirAudio()">
<div class="device shadow-lg">
  <div class="inner">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="logo">AETHERNEXUS</span>
      <div class="status">CHRONOS v3.3 [TEMPORAL]<br><span id="clock"></span> <span class="dot"></span></div>
    </div>
    <div class="timeline-container"><canvas id="chronosCanvas"></canvas></div>
    <div class="screen mb-2" id="log"></div>
    <div class="progress progress-tva mb-2" id="progress-wrapper" style="display: none;">
      <div id="progress-bar" class="progress-bar progress-bar-striped progress-bar-animated progress-bar-tva" role="progressbar" style="width: 0%;">0%</div>
    </div>
    <div class="row g-2 mb-2">
      <div class="col-6"><button class="btn-tempad" onclick="rodar('disk', this)"><div class="fs-5">💿</div><div>Verificar Disco</div><div class="btn-sub">chkdsk / SFC</div></button></div>
      <div class="col-6"><button class="btn-tempad" onclick="rodar('optim', this)"><div class="fs-5">⚡</div><div>Otimizar PC</div><div class="btn-sub">TEMP / Lixeira</div></button></div>
      <div class="col-6"><button class="btn-tempad" onclick="rodar('net', this)"><div class="fs-5">🌐</div><div>Diagnóstico Rede</div><div class="btn-sub">Ping / Tracert</div></button></div>
      <div class="col-6"><button class="btn-tempad" onclick="rodar('sec', this)"><div class="fs-5">🔒</div><div>Segurança</div><div class="btn-sub">Defender / Scan</div></button></div>
    </div>
    <div class="divider"></div>
    <button class="btn btn-exit" onclick="tocaSomClique(); setTimeout(() => window.close(), 200)">PURGAR SESSÃO (ENCERRAR)</button>
    <div class="d-flex justify-content-between align-items-center mt-2">
      <div class="d-flex gap-1"><div class="dot-sm active"></div><div class="dot-sm"></div><div class="dot-sm"></div></div>
      <span style="font-size:11px; color:#6a3800;">AUTORIDADE DE VARIÂNCIA TEMPORAL • CHRONOS MATRIX</span>
    </div>
  </div>
</div>
<script>
const canvas = document.getElementById('chronosCanvas'); const ctx = canvas.getContext('2d');
function resizeCanvas() { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; }
window.addEventListener('resize', resizeCanvas); resizeCanvas();
let step = 0;
function drawTimelineAnimation() {
  ctx.fillStyle = 'rgba(5, 2, 0, 0.2)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
  const centerY = canvas.height / 2;
  ctx.beginPath(); ctx.strokeStyle = 'rgba(255, 136, 0, 0.8)'; ctx.lineWidth = 2;
  for (let x = 0; x < canvas.width; x += 5) {
    const y = centerY + Math.sin((x + step) * 0.05) * 4;
    if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();
  for (let i = 0; i < 3; i++) {
    ctx.beginPath(); ctx.strokeStyle = `rgba(255, 100, 0, ${0.2 + i * 0.2})`; ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 8) {
      const y = centerY + Math.cos((x - step * (i + 1)) * (0.03 + i * 0.01)) * (8 + i * 5);
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }
  const pingX = (step * 3) % canvas.width;
  ctx.beginPath(); ctx.arc(pingX, centerY, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#ffaa00'; ctx.shadowBlur = 10; ctx.shadowColor = '#ff8800'; ctx.fill(); ctx.shadowBlur = 0;
  step += 1.5; requestAnimationFrame(drawTimelineAnimation);
}
drawTimelineAnimation();

let audioCtx = null;
function garantirAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); }
function tocaSomClique() { garantirAudio(); if (!audioCtx) return; const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain(); osc.type = 'triangle'; osc.frequency.setValueAtTime(140, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.05); gain.gain.setValueAtTime(0.3, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.05); osc.connect(gain); gain.connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime + 0.05); }
function tocaSomProgresso() { garantirAudio(); if (!audioCtx) return; const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain(); osc.type = 'square'; osc.frequency.setValueAtTime(500 + Math.random() * 200, audioCtx.currentTime); gain.gain.setValueAtTime(0.02, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.03); osc.connect(gain); gain.connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime + 0.03); }
function tocaSomSucesso() { garantirAudio(); if (!audioCtx) return; [440, 554.37, 659.25, 880].forEach((freq, idx) => { const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain(); osc.type = 'sine'; osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.08); gain.gain.setValueAtTime(0.08, audioCtx.currentTime + idx * 0.08); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + idx * 0.08 + 0.2); osc.connect(gain); gain.connect(audioCtx.destination); osc.start(audioCtx.currentTime + idx * 0.08); osc.stop(audioCtx.currentTime + idx * 0.08 + 0.2); }); }

const asciiBanner = ["   _   _____ _____ _  _ ___ ___ ", "  /_\\\\ | ____|_   _| || | __| _ \\\\", " / _ \\\\| _|| | | | | __ | _||   /", "/_/ \\\\_\\\\_____|_| |_|_||_|___|_|_\\\\", "  [ A E T H E R N E X U S - C H R O N O S ]", "------------------------------------------", "> Sincronizando matriz temporal...", "> Servidor FastAPI operacional.", "> Aguardando instruções..."];
function executarBootAnimation() { const logEl = document.getElementById('log'); logEl.textContent = ''; let lineIdx = 0; const interval = setInterval(() => { if (lineIdx < asciiBanner.length) { logEl.textContent += asciiBanner[lineIdx] + '\\n'; logEl.scrollTop = logEl.scrollHeight; lineIdx++; } else { clearInterval(interval); } }, 90); }
window.onload = executarBootAnimation;

let progressoInterval = null;
function sanitize(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }
function log(msg) { const el = document.getElementById('log'); el.innerHTML += sanitize(msg) + '\\n'; el.scrollTop = el.scrollHeight; }
function iniciarBarraProgresso() { const wrapper = document.getElementById('progress-wrapper'); const bar = document.getElementById('progress-bar'); wrapper.style.display = 'flex'; let pct = 0; bar.style.width = '0%'; bar.textContent = '0%'; progressoInterval = setInterval(() => { if (pct < 90) { pct += Math.floor(Math.random() * 8) + 2; if (pct > 90) pct = 90; bar.style.width = pct + '%'; bar.textContent = pct + '%'; tocaSomProgresso(); } }, 200); }
function finalizarBarraProgresso() { clearInterval(progressoInterval); const wrapper = document.getElementById('progress-wrapper'); const bar = document.getElementById('progress-bar'); bar.style.width = '100%'; bar.textContent = '100% SUCESSO'; tocaSomSucesso(); setTimeout(() => { wrapper.style.display = 'none'; }, 2500); }

function rodar(modulo, btn) {
  tocaSomClique(); btn.classList.add('running'); btn.disabled = true;
  log('\\n> --- [ EXECUTANDO: ' + modulo.toUpperCase() + ' ] ---');
  iniciarBarraProgresso();
  const source = new EventSource('/rodar/' + modulo);
  source.onmessage = function(e) { log(e.data); };
  source.onerror = function() { source.close(); finalizarBarraProgresso(); btn.classList.remove('running'); btn.disabled = false; log('> --- [ CONCLUÍDO ] ---'); };
}
function clock() { document.getElementById('clock').textContent = new Date().toLocaleTimeString('pt-BR') + ' '; }
setInterval(clock, 1000); clock();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=HTML_INTERFACE)

@app.get("/rodar/{modulo}")
async def rodar(modulo: str):
    script_name = SCRIPT_MAP.get(modulo)
    if not script_name:
        raise HTTPException(status_code=404, detail="Módulo temporal não cadastrado")

    caminho_script = os.path.join(SCRIPTS_DIR, script_name)

    async def evento_gerador():
        if not os.path.exists(caminho_script):
            yield f"data: ❌ Script não localizado: {script_name}\\n\\n"
            return

        processo = await asyncio.create_subprocess_exec(
            sys.executable, "-u", caminho_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        try:
            while True:
                linha = await processo.stdout.readline()
                if not linha:
                    break
                texto = linha.decode('utf-8', errors='replace').strip()
                if texto:
                    yield f"data: {texto}\\n\\n"

            await processo.wait()
            yield f"data: ✅ Módulo {script_name} finalizado.\\n\\n"
        except asyncio.CancelledError:
            processo.kill()
            raise

    return StreamingResponse(evento_gerador(), media_type="text/event-stream")

if __name__ == '__main__':
    print("🚀 AETHERNEXUS-CHRONOS TemPad OS v3.3 iniciado em http://0.0.0.0:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
'''

# ---------------------------------------------------------------------------
# Inspeção Nativa de Hardware e Sistema Operacional
# ---------------------------------------------------------------------------
def is_admin() -> bool:
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.getuid() == 0
    except Exception:
        return False

def get_hostname() -> str:
    return platform.node() or os.getenv('COMPUTERNAME', 'Unknown')

def get_detailed_os() -> str:
    sys_name = platform.system()
    is_colab = "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ
    colab_prefix = "GOOGLE COLAB " if is_colab else ""

    if sys_name == "Linux":
        try:
            info = platform.freedesktop_os_release()
            pretty = info.get("PRETTY_NAME", "Linux Genérico")
            return f"{colab_prefix}({pretty})"
        except Exception:
            return f"{colab_prefix}(Linux {platform.release()})"
    elif sys_name == "Windows":
        return f"Windows {platform.release()} (Build {platform.version()})"
    elif sys_name == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    return sys_name

def get_cpu_name() -> str:
    if os.name == 'nt' and winreg:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return cpu_name.strip()
        except Exception:
            pass
    elif os.name == 'posix':
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except Exception:
            pass
    return platform.processor() or "Processador Genérico"

def get_gpu_name() -> str:
    if os.name == 'nt':
        try:
            cmd = 'powershell -NoProfile -Command "(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name"'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            if output:
                return output
        except Exception:
            pass
    elif os.name == 'posix':
        try:
            output = subprocess.check_output("lspci", text=True, stderr=subprocess.DEVNULL)
            for line in output.splitlines():
                if "VGA" in line or "3D" in line or "Display" in line:
                    return line.split(":")[2].strip()
        except Exception:
            pass
    return "Vídeo Integrado / Genérico"

def get_ram_details() -> str:
    if os.name == 'nt':
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            total_gb = stat.ullTotalPhys / (1024**3)
            avail_gb = stat.ullAvailPhys / (1024**3)
            return f"{total_gb:.2f} GB (Livre: {avail_gb:.2f} GB)"
        except Exception:
            pass
    elif os.name == 'posix':
        try:
            mem_total, mem_avail = 0, 0
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        mem_total = int(line.split()[1]) / (1024**2)
                    elif line.startswith("MemAvailable:"):
                        mem_avail = int(line.split()[1]) / (1024**2)
            if mem_total > 0:
                return f"{mem_total:.2f} GB (Livre: {mem_avail:.2f} GB)"
        except Exception:
            pass
    return "N/A"

def get_storage_details() -> str:
    total, used, _ = shutil.disk_usage("/")
    total_gb = total / (1024**3)
    used_gb = used / (1024**3)
    
    disk_type = "DISCO"
    if os.name == 'nt':
        try:
            cmd = 'powershell -NoProfile -Command "(Get-PhysicalDisk | Select-Object -First 1).MediaType"'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            if output in ["SSD", "HDD", "SCM"]:
                disk_type = output
        except Exception:
            pass
    elif os.name == 'posix':
        try:
            for block in ["nvme0n1", "sda", "sdb"]:
                rot_path = f"/sys/block/{block}/queue/rotational"
                if os.path.exists(rot_path):
                    with open(rot_path, 'r') as f:
                        disk_type = "SSD" if f.read().strip() == "0" else "HDD"
                    break
        except Exception:
            pass

    return f"{used_gb:.0f} GB de {total_gb:.0f} GB usados ({disk_type})"

# ---------------------------------------------------------------------------
# Animações & Componentes Visuais do Terminal
# ---------------------------------------------------------------------------
def render_banner(animado: bool = True) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner_lines = [
        r" █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ ",
        r"██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗",
        r"███████║█████╗     ██║   ███████║█████╗  ██████╔╝",
        r"██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗",
        r"██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║",
        r"╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
        r"███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗      ",
        r"████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝      ",
        r"██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗      ",
        r"██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║      ",
        r"██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║      ",
        r"╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ",
        r"             ─── C H R O N O S ───               ",
        r" ╔══════════════════════════════════════════════════════════════════╗",
        r" ║     TIME VARIANCE AUTHORITY — NEXUS INSTALLATION ENGINE          ║",
        r" ╚══════════════════════════════════════════════════════════════════╝"
    ]

    for line in banner_lines:
        if animado:
            sys.stdout.write(f"{CLR_BRIGHT}{line}{CLR_RESET}\n")
            sys.stdout.flush()
            time.sleep(0.02)
            sys.stdout.write(f"\033[F{CLR_AMBER}{line}{CLR_RESET}\n")
        else:
            print(f"{CLR_AMBER}{line}{CLR_RESET}")

def barra_progresso_tva(atual: int, total: int, prefixo: str = "", largura: int = 25) -> None:
    percentual = atual / float(total)
    preenchidos = int(largura * percentual)
    barra = '█' * preenchidos + '░' * (largura - preenchidos)
    sys.stdout.write(
        f"\r {CLR_DIM}│{CLR_RESET} {prefixo:<22} {CLR_AMBER}[{barra}]{CLR_RESET} {CLR_BRIGHT}{int(percentual * 100):>3}%{CLR_RESET}"
    )
    sys.stdout.flush()
    if atual == total:
        sys.stdout.write("\n")

def efeito_glitch(texto_final: str, duracao_frames: int = 4) -> None:
    chars = string.ascii_uppercase + string.digits + "!@#$%^&*"
    texto_atual = [" "] * len(texto_final)
    
    for i in range(len(texto_final)):
        for _ in range(duracao_frames):
            char_temp = random.choice(chars)
            sys.stdout.write(f"\r{CLR_AMBER}{''.join(texto_atual[:i])}{CLR_BRIGHT}{char_temp}{CLR_RESET}")
            sys.stdout.flush()
            time.sleep(0.008)
        texto_atual[i] = texto_final[i]
    
    sys.stdout.write(f"\r{CLR_GREEN}{''.join(texto_final)}{CLR_RESET}\n")

def spinner_tva(mensagem: str, segundos: float = 0.8) -> None:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    fim = time.time() + segundos
    i = 0
    while time.time() < fim:
        sys.stdout.write(f"\r{CLR_AMBER}{frames[i % len(frames)]}{CLR_RESET} {mensagem}...")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    sys.stdout.write(f"\r{CLR_GREEN}[✓]{CLR_RESET} {mensagem} COMPLETO!   \n")

def draw_box(title: str, items: list) -> None:
    width = 68
    print(f"\n{CLR_DIM}┌──[{CLR_RESET} {CLR_BRIGHT}{title}{CLR_RESET} {CLR_DIM}]" + "─" * (width - len(title) - 7) + "┐" + CLR_RESET)
    for label, val in items:
        padding = " " * (22 - len(label))
        print(f" {CLR_DIM}│{CLR_RESET} {CLR_AMBER}{label}{padding}:{CLR_RESET} {val}")
    print(f"{CLR_DIM}└" + "─" * (width - 1) + "┘" + CLR_RESET)

# ---------------------------------------------------------------------------
# Verificação e Instalação de Pacotes
# ---------------------------------------------------------------------------
def check_and_install_packages() -> list:
    width = 68
    title = "VERIFICANDO DEPENDÊNCIAS PIP"
    print(f"\n{CLR_DIM}┌──[{CLR_RESET} {CLR_BRIGHT}{title}{CLR_RESET} {CLR_DIM}]" + "─" * (width - len(title) - 7) + "┐" + CLR_RESET)
    
    total_pacotes = len(REQUIRED_PACKAGES)
    failed = []

    for idx, (import_name, pip_name) in enumerate(REQUIRED_PACKAGES, 1):
        barra_progresso_tva(idx - 1, total_pacotes, prefixo=f"CHECANDO {pip_name[:12]}")
        
        is_installed = importlib.util.find_spec(import_name) is not None
        
        if not is_installed:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pip_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                failed.append(pip_name)
        
        time.sleep(0.04)
        barra_progresso_tva(idx, total_pacotes, prefixo=f"CHECANDO {pip_name[:12]}")

    print(f"{CLR_DIM}└" + "─" * (width - 1) + "┘" + CLR_RESET)
    return failed

# ---------------------------------------------------------------------------
# Auto-Lançador do Servidor Web e Navegador (Com Autocriação de Arquivo)
# ---------------------------------------------------------------------------
def launch_web_app() -> None:
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aether_nexus_app.py")
    
    # Se o aether_nexus_app.py não existir, cria o arquivo automaticamente
    if not os.path.exists(app_path):
        print(f"\n{CLR_AMBER}[⚡] GERANDO AUTOMATICAMENTE 'aether_nexus_app.py'...{CLR_RESET}")
        try:
            with open(app_path, "w", encoding="utf-8") as f:
                f.write(AETHER_NEXUS_APP_CODE)
            print(f"{CLR_GREEN}[✓] ARQUIVO AETHER_NEXUS_APP.PY GERADO COM SUCESSO!{CLR_RESET}")
        except Exception as e:
            print(f"{CLR_RED}[X] ERRO CRÍTICO AO GERAR ARQUIVO: {e}{CLR_RESET}\n")
            return

    print(f"\n{CLR_BRIGHT}▶ INICIANDO AETHERNEXUS TEMPAD WEB OS...{CLR_RESET}")
    print(f"{CLR_AMBER}  Servidor local: http://127.0.0.1:5000{CLR_RESET}")
    
    # Suporte para Colab / Codespaces / Ambiente Local
    is_colab = "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ
    is_codespace = "CODESPACES" in os.environ

    if is_colab:
        try:
            from google.colab import output
            output.serve_kernel_port_as_iframe(5000)
            print(f"{CLR_GREEN}[✓] Iframe do Google Colab carregado.{CLR_RESET}\n")
        except Exception:
            pass
    elif not is_codespace:
        print(f"{CLR_AMBER}  Abrindo navegador automaticamente...{CLR_RESET}\n")
        def abrir_navegador():
            time.sleep(1.8)
            webbrowser.open("http://127.0.0.1:5000")
        threading.Thread(target=abrir_navegador, daemon=True).start()
    else:
        print(f"{CLR_GREEN}[✓] GitHub Codespaces detectado: Acesse a aba 'Ports' (Porta 5000).{CLR_RESET}\n")

    try:
        subprocess.run([sys.executable, app_path])
    except KeyboardInterrupt:
        print(f"\n\n{CLR_RED}[!] Servidor TemPad encerrado pelo usuário.{CLR_RESET}\n")

# ---------------------------------------------------------------------------
# Execução Principal
# ---------------------------------------------------------------------------
def main() -> None:
    render_banner(animado=True)
    print()

    spinner_tva("SINCRONIZANDO COM AETHERNEXUS CHRONOS", 0.8)
    spinner_tva("INSPECIONANDO HARDWARE DO DISPOSITIVO", 0.6)

    device_info = [
        ("NOME DO DISPOSITIVO", get_hostname()),
        ("SISTEMA OPERACIONAL", get_detailed_os()),
        ("PROCESSADOR", get_cpu_name()),
        ("ARQUITETURA / CPU", f"{platform.machine()} ({os.cpu_count() or 1} Cores)"),
        ("MEMÓRIA RAM", get_ram_details()),
        ("PLACA GRÁFICA", get_gpu_name()),
        ("ARMAZENAMENTO", get_storage_details()),
        ("VERSÃO DO PYTHON", sys.version.split()[0]),
        ("PRIVILÉGIOS ADMIN", "SIM" if is_admin() else "NÃO")
    ]
    draw_box("STATUS DO DISPOSITIVO", device_info)

    failed_packages = check_and_install_packages()

    print(f"\n{CLR_DIM}┌──[{CLR_RESET} {CLR_BRIGHT}DIAGNÓSTICO FINAL{CLR_RESET} {CLR_DIM}]" + "─" * 45 + "┐" + CLR_RESET)
    if failed_packages:
        print(f" {CLR_DIM}│{CLR_RESET} {CLR_RED}[!] FALHA AO INSTALAR: {', '.join(failed_packages)}{CLR_RESET}")
    else:
        sys.stdout.write(f" {CLR_DIM}│{CLR_RESET} ")
        efeito_glitch("[✓] NENHUM EVENTO NEXUS DETECTADO. AETHERNEXUS-CHRONOS OS ONLINE!")
    print(f"{CLR_DIM}└" + "─" * 67 + "┘" + CLR_RESET)

    launch_web_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{CLR_RED}[!] Instalação interrompida pelo usuário.{CLR_RESET}\n")
    except Exception as err:
        print(f"\n{CLR_RED}[X] ERRO CRÍTICO DURANTE O SETUP: {err}{CLR_RESET}\n")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 AETHERNEXUS-CHRONOS — TEMPAD WEB APP (Rare/aether_nexus_app.py)
 -----------------------------------------------------------------------------
 Engine Web Assíncrona (FastAPI + Uvicorn + Async SSE + Chronos CRT Animation)
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

# Gera scripts de demonstração caso a pasta esteja vazia
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
                    "import time\n"
                    f"print('>>> [CHRONOS] Iniciando módulo {modulo.upper()}...')\n"
                    "for i in range(1, 6):\n"
                    "    print(f'   Analisa linha temporal... passo {i}/5')\n"
                    "    time.sleep(0.4)\n"
                    "print('>>> [OK] Varredura concluída sem anomalias.')\n"
                )

inicializar_scripts_demo()

HTML_INTERFACE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AETHERNEXUS-CHRONOS — TemPad OS</title>

<!-- Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">

<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #080400;
    font-family: 'VT323', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    user-select: none;
    overflow: hidden;
  }
  
  .device {
    background: linear-gradient(160deg, #b85000, #5c2400);
    border-radius: 32px;
    padding: 6px;
    width: 100%;
    max-width: 480px;
    box-shadow: 0 0 0 2px #e87a20, 0 8px 40px rgba(0,0,0,0.9);
  }
  .inner {
    background: #140b00;
    border-radius: 27px;
    padding: 20px;
    border: 1px solid #3a1c00;
  }

  .logo {
    font-size: 22px;
    font-weight: bold;
    color: #ff9933;
    letter-spacing: 3px;
    text-shadow: 0 0 8px rgba(255, 153, 51, 0.8);
  }
  .status {
    font-size: 13px;
    color: #b35000;
    text-align: right;
    line-height: 1.2;
  }
  .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #ff8800;
    display: inline-block;
    animation: blink 1.8s infinite;
    box-shadow: 0 0 6px #ff8800;
  }
  @keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.2; }
  }

  .timeline-container {
    position: relative;
    width: 100%;
    height: 48px;
    background: #050200;
    border: 1px solid #ff880044;
    border-radius: 8px;
    margin-bottom: 8px;
    overflow: hidden;
  }
  #chronosCanvas { width: 100%; height: 100%; display: block; }
  
  .screen {
    position: relative;
    background: #050200;
    border-radius: 12px;
    border: 1px solid #ff880055;
    padding: 12px;
    height: 170px;
    overflow-y: auto;
    font-size: 15px;
    letter-spacing: 1px;
    color: #ff9900;
    line-height: 1.3;
    text-shadow: 0 0 5px rgba(255, 136, 0, 0.8);
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.95);
    white-space: pre-wrap;
    word-break: break-all;
  }
  
  .screen::after {
    content: " ";
    display: block;
    position: absolute;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.35) 50%);
    background-size: 100% 4px;
    pointer-events: none;
    opacity: 0.6;
  }

  .screen::-webkit-scrollbar { width: 4px; }
  .screen::-webkit-scrollbar-thumb { background: #5a3000; border-radius: 2px; }

  .progress-tva {
    background-color: #080300;
    border: 1px solid #5a3000;
    height: 18px;
    border-radius: 6px;
  }
  .progress-bar-tva {
    background-color: #ff8800;
    color: #140b00;
    font-weight: bold;
    font-family: 'VT323', monospace;
    font-size: 14px;
    box-shadow: 0 0 8px #ff8800;
  }

  .btn-tempad {
    background: #1f0f00;
    border: 1px solid #5a3000;
    border-radius: 12px;
    padding: 10px 6px;
    color: #ff9933;
    font-family: 'VT323', monospace;
    font-size: 16px;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.15s;
    width: 100%;
  }
  .btn-tempad:hover { 
    background: #2e1800; 
    border-color: #ff8800;
    color: #ffaa44;
    box-shadow: 0 0 10px rgba(255, 136, 0, 0.3);
  }
  .btn-tempad:active { transform: scale(0.97); }

  .running { 
    border-color: #ff8800 !important; 
    background: #3a1a00 !important;
    animation: pulse-btn 0.9s infinite alternate;
  }
  @keyframes pulse-btn {
    from { box-shadow: 0 0 4px rgba(255, 136, 0, 0.3); }
    to { box-shadow: 0 0 16px rgba(255, 136, 0, 0.9); }
  }

  .btn-sub { color: #884400; font-size: 12px; }
  
  .btn-exit {
    width: 100%;
    background: #2a0a00;
    border: 1px solid #6a2000;
    border-radius: 12px;
    padding: 8px;
    color: #ff4400;
    font-family: 'VT323', monospace;
    font-size: 16px;
    letter-spacing: 2px;
    text-shadow: 0 0 4px rgba(255, 68, 0, 0.5);
  }
  .btn-exit:hover { background: #3a1500; border-color: #ff4400; color: #ff6622; }
  .divider { height: 1px; background: #3a1800; margin: 10px 0; }
  
  .dot-sm {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #5a3000;
  }
  .dot-sm.active { background: #ff8800; animation: blink 2s infinite; box-shadow: 0 0 4px #ff8800; }
</style>
</head>
<body onclick="garantirAudio()">

<div class="device shadow-lg">
  <div class="inner">
    
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="logo">AETHERNEXUS</span>
      <div class="status">
        CHRONOS v3.3 [TEMPORAL]<br>
        <span id="clock"></span>
        <span class="dot"></span>
      </div>
    </div>

    <div class="timeline-container">
      <canvas id="chronosCanvas"></canvas>
    </div>

    <div class="screen mb-2" id="log"></div>

    <div class="progress progress-tva mb-2" id="progress-wrapper" style="display: none;">
      <div id="progress-bar" 
           class="progress-bar progress-bar-striped progress-bar-animated progress-bar-tva" 
           role="progressbar" 
           style="width: 0%;">0%</div>
    </div>

    <div class="row g-2 mb-2">
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('disk', this)">
          <div class="fs-5">💿</div>
          <div>Verificar Disco</div>
          <div class="btn-sub">chkdsk / SFC / DISM</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('optim', this)">
          <div class="fs-5">⚡</div>
          <div>Otimizar PC</div>
          <div class="btn-sub">TEMP / Lixeira</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('net', this)">
          <div class="fs-5">🌐</div>
          <div>Diagnóstico Rede</div>
          <div class="btn-sub">Ping / Tracert</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('sec', this)">
          <div class="fs-5">🔒</div>
          <div>Segurança</div>
          <div class="btn-sub">Defender / SFC</div>
        </button>
      </div>
    </div>

    <div class="divider"></div>
    <button class="btn btn-exit" onclick="tocaSomClique(); setTimeout(() => window.close(), 200)">PURGAR SESSÃO (ENCERRAR)</button>

    <div class="d-flex justify-content-between align-items-center mt-2">
      <div class="d-flex gap-1">
        <div class="dot-sm active"></div>
        <div class="dot-sm"></div>
        <div class="dot-sm"></div>
      </div>
      <span style="font-size:11px; color:#6a3800;">AUTORIDADE DE VARIÂNCIA TEMPORAL • CHRONOS MATRIX</span>
    </div>

  </div>
</div>

<script>
// Canvas Engine
const canvas = document.getElementById('chronosCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

let step = 0;
function drawTimelineAnimation() {
  ctx.fillStyle = 'rgba(5, 2, 0, 0.2)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const centerY = canvas.height / 2;
  
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(255, 136, 0, 0.8)';
  ctx.lineWidth = 2;
  for (let x = 0; x < canvas.width; x += 5) {
    const y = centerY + Math.sin((x + step) * 0.05) * 4;
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  for (let i = 0; i < 3; i++) {
    ctx.beginPath();
    ctx.strokeStyle = `rgba(255, 100, 0, ${0.2 + i * 0.2})`;
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 8) {
      const freq = 0.03 + i * 0.01;
      const amp = 8 + i * 5;
      const y = centerY + Math.cos((x - step * (i + 1)) * freq) * amp;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  const pingX = (step * 3) % canvas.width;
  ctx.beginPath();
  ctx.arc(pingX, centerY, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#ffaa00';
  ctx.shadowBlur = 10;
  ctx.shadowColor = '#ff8800';
  ctx.fill();
  ctx.shadowBlur = 0;

  step += 1.5;
  requestAnimationFrame(drawTimelineAnimation);
}
drawTimelineAnimation();

// Web Audio API
let audioCtx = null;
function garantirAudio() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (audioCtx.state === 'suspended') audioCtx.resume();
}

function tocaSomClique() {
  garantirAudio();
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(140, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.05);
  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.05);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.05);
}

function tocaSomProgresso() {
  garantirAudio();
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(500 + Math.random() * 200, audioCtx.currentTime);
  gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.03);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.03);
}

function tocaSomSucesso() {
  garantirAudio();
  if (!audioCtx) return;
  const notas = [440, 554.37, 659.25, 880];
  notas.forEach((freq, idx) => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.08);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime + idx * 0.08);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + idx * 0.08 + 0.2);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(audioCtx.currentTime + idx * 0.08);
    osc.stop(audioCtx.currentTime + idx * 0.08 + 0.2);
  });
}

// Boot ASCII
const asciiBanner = [
  "   _   _____ _____ _  _ ___ ___ ",
  "  /_\\ | ____|_   _| || | __| _ \\",
  " / _ \\| _|| | | | | __ | _||   /",
  "/_/ \\_\\_____|_| |_|_||_|___|_|_\\",
  "  [ A E T H E R N E X U S - C H R O N O S ]",
  "------------------------------------------",
  "> Inicializando sincronia de linha temporal...",
  "> Conectado ao servidor assíncrono FastAPI.",
  "> Aguardando instrução de comando..."
];

function executarBootAnimation() {
  const logEl = document.getElementById('log');
  logEl.textContent = '';
  let lineIdx = 0;

  const interval = setInterval(() => {
    if (lineIdx < asciiBanner.length) {
      logEl.textContent += asciiBanner[lineIdx] + '\\n';
      logEl.scrollTop = logEl.scrollHeight;
      lineIdx++;
    } else {
      clearInterval(interval);
    }
  }, 100);
}
window.onload = executarBootAnimation;

// Logs e Progresso
let progressoInterval = null;

function sanitize(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function log(msg) {
  const el = document.getElementById('log');
  el.innerHTML += sanitize(msg) + '\\n';
  el.scrollTop = el.scrollHeight;
}

function iniciarBarraProgresso() {
  const wrapper = document.getElementById('progress-wrapper');
  const bar = document.getElementById('progress-bar');
  wrapper.style.display = 'flex';
  
  let pct = 0;
  bar.style.width = '0%';
  bar.textContent = '0%';

  progressoInterval = setInterval(() => {
    if (pct < 90) {
      pct += Math.floor(Math.random() * 8) + 2;
      if (pct > 90) pct = 90;
      bar.style.width = pct + '%';
      bar.textContent = pct + '%';
      tocaSomProgresso();
    }
  }, 200);
}

function finalizarBarraProgresso() {
  clearInterval(progressoInterval);
  const wrapper = document.getElementById('progress-wrapper');
  const bar = document.getElementById('progress-bar');
  
  bar.style.width = '100%';
  bar.textContent = '100% SUCESSO';
  tocaSomSucesso();

  setTimeout(() => {
    wrapper.style.display = 'none';
  }, 2500);
}

function rodar(modulo, btn) {
  tocaSomClique();
  btn.classList.add('running');
  btn.disabled = true;

  log('\\n> --- [ EXECUTANDO: ' + modulo.toUpperCase() + ' ] ---');
  iniciarBarraProgresso();

  const source = new EventSource('/rodar/' + modulo);
  source.onmessage = function(e) {
    log(e.data);
  };
  source.onerror = function() {
    source.close();
    finalizarBarraProgresso();
    
    btn.classList.remove('running');
    btn.disabled = false;
    log('> --- [ CONCLUÍDO ] ---');
  };
}

function clock() {
  document.getElementById('clock').textContent =
    new Date().toLocaleTimeString('pt-BR') + ' ';
}
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
            yield f"data: ❌ Script não localizado: {script_name}\n\n"
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
                    yield f"data: {texto}\n\n"

            await processo.wait()
            yield f"data: ✅ Módulo {script_name} finalizado.\n\n"
        except asyncio.CancelledError:
            processo.kill()
            raise

    return StreamingResponse(evento_gerador(), media_type="text/event-stream")

if __name__ == '__main__':
    print("🚀 AETHERNEXUS-CHRONOS TemPad OS v3.3 iniciado em http://127.0.0.1:5000")
    uvicorn.run(app, host="127.0.0.1", port=5000)

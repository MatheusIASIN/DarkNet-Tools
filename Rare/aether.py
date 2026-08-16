"""
============================================
DarkNet Tools — TemPad Web
Criado por: Matheus Iasin
Versão: 3.3 (Bootstrap 5 + TVA Audio + CRT FX)
============================================
COMO RODAR:
    pip install flask
    python main_web.py
    Acesse: http://localhost:5000
============================================
"""

from flask import Flask, Response, render_template_string
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TemPad — TVA Tools</title>

<!-- Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Fonte Retro Monospaced -->
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
  }
  
  /* Carcaça Fisiomórfica do TemPad */
  .device {
    background: linear-gradient(160deg, #b85000, #5c2400);
    border-radius: 32px;
    padding: 6px;
    width: 100%;
    max-width: 450px;
    box-shadow: 0 0 0 2px #e87a20, 0 8px 40px rgba(0,0,0,0.9);
  }
  .inner {
    background: #140b00;
    border-radius: 27px;
    padding: 20px;
    border: 1px solid #3a1c00;
  }

  .logo {
    font-size: 24px;
    font-weight: bold;
    color: #ff9933;
    letter-spacing: 4px;
    text-shadow: 0 0 8px rgba(255, 153, 51, 0.7);
  }
  .status {
    font-size: 14px;
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
  
  /* Display Estilo CRT Analógico da TVA */
  .screen {
    position: relative;
    background: #050200;
    border-radius: 12px;
    border: 1px solid #ff880055;
    padding: 12px;
    height: 150px;
    overflow-y: auto;
    font-size: 17px;
    letter-spacing: 1px;
    color: #ff9900;
    line-height: 1.3;
    text-shadow: 0 0 5px rgba(255, 136, 0, 0.8);
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.95);
  }
  
  /* Linhas de Varredura CRT */
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

  /* Customização de Progresso do Bootstrap para o Tema TVA */
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

  /* Estilização dos Botões */
  .btn-tempad {
    background: #1f0f00;
    border: 1px solid #5a3000;
    border-radius: 12px;
    padding: 12px 8px;
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

  /* Animação do Botão em Execução */
  .running { 
    border-color: #ff8800 !important; 
    background: #3a1a00 !important;
    animation: pulse-btn 0.9s infinite alternate;
  }
  @keyframes pulse-btn {
    from { box-shadow: 0 0 4px rgba(255, 136, 0, 0.3); }
    to { box-shadow: 0 0 16px rgba(255, 136, 0, 0.9); }
  }

  .btn-sub { color: #884400; font-size: 13px; }
  
  .btn-exit {
    width: 100%;
    background: #2a0a00;
    border: 1px solid #6a2000;
    border-radius: 12px;
    padding: 10px;
    color: #ff4400;
    font-family: 'VT323', monospace;
    font-size: 16px;
    letter-spacing: 2px;
    text-shadow: 0 0 4px rgba(255, 68, 0, 0.5);
  }
  .btn-exit:hover { background: #3a1500; border-color: #ff4400; color: #ff6622; }
  .divider { height: 1px; background: #3a1800; margin: 12px 0; }
  
  .dot-sm {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #5a3000;
  }
  .dot-sm.active { background: #ff8800; animation: blink 2s infinite; box-shadow: 0 0 4px #ff8800; }
</style>
</head>
<body>

<div class="device shadow-lg">
  <div class="inner">
    
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <span class="logo">TEMPAD</span>
      <div class="status">
        TVA BOOTSTRAP v3.3<br>
        <span id="clock"></span>
        <span class="dot"></span>
      </div>
    </div>

    <!-- Tela CRT -->
    <div class="screen mb-2" id="log">
&gt; TVA TemPad OS v3.3 [BOOTSTRAP OK]<br>
&gt; Módulos analógicos e de áudio online.<br>
&gt; Aguardando instrução do agente...
    </div>

    <!-- Barra de Progresso Bootstrap -->
    <div class="progress progress-tva mb-3" id="progress-wrapper" style="display: none;">
      <div id="progress-bar" 
           class="progress-bar progress-bar-striped progress-bar-animated progress-bar-tva" 
           role="progressbar" 
           style="width: 0%;">0%</div>
    </div>

    <!-- Grid de Botões no Sistema do Bootstrap -->
    <div class="row g-2 mb-2">
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('disk', this)">
          <div class="fs-4">💿</div>
          <div>Verificar Disco</div>
          <div class="btn-sub">chkdsk / SFC / DISM</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('optim', this)">
          <div class="fs-4">⚡</div>
          <div>Otimizar PC</div>
          <div class="btn-sub">TEMP / Lixeira</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('net', this)">
          <div class="fs-4">🌐</div>
          <div>Diagnóstico Rede</div>
          <div class="btn-sub">Ping / Tracert</div>
        </button>
      </div>
      <div class="col-6">
        <button class="btn-tempad" onclick="rodar('sec', this)">
          <div class="fs-4">🔒</div>
          <div>Segurança</div>
          <div class="btn-sub">Defender / SFC</div>
        </button>
      </div>
    </div>

    <div class="divider"></div>
    <button class="btn btn-exit" onclick="tocaSomClique(); setTimeout(() => window.close(), 200)">ENCERRAR SESSÃO</button>

    <!-- Rodapé -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <div class="d-flex gap-1">
        <div class="dot-sm active"></div>
        <div class="dot-sm"></div>
        <div class="dot-sm"></div>
      </div>
      <span style="font-size:12px; color:#6a3800;">AUTORIDADE DE VARIÂNCIA TEMPORAL</span>
    </div>

  </div>
</div>

<script>
// --- SINTETIZADOR DE ÁUDIO RETRÔ ---
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function tocaSomClique() {
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(120, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.05);
  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.05);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.05);
}

function tocaSomProgresso() {
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(550 + Math.random() * 150, audioCtx.currentTime);
  gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.03);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.03);
}

function tocaSomSucesso() {
  if (audioCtx.state === 'suspended') audioCtx.resume();
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

// --- CONTROLE DE LOGS E PROGRESSO ---
let progressoInterval = null;

function log(msg) {
  const el = document.getElementById('log');
  el.innerHTML += '<br>' + msg;
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
  }, 250);
}

function finalizarBarraProgresso() {
  clearInterval(progressoInterval);
  const wrapper = document.getElementById('progress-wrapper');
  const bar = document.getElementById('progress-bar');
  
  bar.style.width = '100%';
  bar.textContent = '100% OK!';
  tocaSomSucesso();

  setTimeout(() => {
    wrapper.style.display = 'none';
  }, 3000);
}

function rodar(modulo, btn) {
  tocaSomClique();
  btn.classList.add('running');
  btn.disabled = true;

  log('<br>&gt; --- [ INICIANDO: ' + modulo.toUpperCase() + ' ] ---');
  iniciarBarraProgresso();

  const source = new EventSource('/rodar/' + modulo);
  source.onmessage = function(e) {
    log('&gt; ' + e.data);
  };
  source.onerror = function() {
    source.close();
    finalizarBarraProgresso();
    
    btn.classList.remove('running');
    btn.disabled = false;
    log('&gt; --- [ CONCLUÍDO ] ---');
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

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/rodar/<modulo>')
def rodar(modulo):
    scripts = {
        'disk': 'disk_check.py',
        'optim': 'optimize.py',
        'net': 'network_diagnosis.py',
        'sec': 'security_scan.py',
    }

    script = scripts.get(modulo)
    if not script:
        return "Módulo inválido", 404

    caminho = os.path.join(SCRIPTS_DIR, script)

    def gerar():
        if not os.path.exists(caminho):
            yield f"data: ❌ Script não encontrado: {script}\n\n"
            return

        processo = subprocess.Popen(
            ['python', '-u', caminho],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for linha in processo.stdout:
            yield f"data: {linha.strip()}\n\n"

        processo.wait()
        yield f"data: ✅ Concluído com sucesso!\n\n"

    return Response(gerar(), mimetype='text/event-stream')

if __name__ == '__main__':
    print("🚀 TemPad Web v3.3 (Bootstrap + Audio FX) iniciado!")
    print("📡 Acesse: http://localhost:5000")
    app.run(debug=False, port=5000)

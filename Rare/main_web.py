"""
============================================
DarkNet Tools — TemPad Web
Criado por: Matheus Iasin
Versao: 3.0 (Web - TVA Retro Style)
============================================
COMO RODAR:
    pip install flask
    python main_web.py
    Abre no navegador: http://localhost:5000
============================================
"""

from flask import Flask, Response, render_template_string
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# ============================================
# HTML DO TEMPAD
# ============================================

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>TemPad — TVA Tools</title>
<!-- Importação da fonte Retro Monospaced da TVA -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">

<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d0700;
    font-family: 'VT323', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }
  .device {
    background: linear-gradient(160deg, #c45a00, #7a3200);
    border-radius: 32px;
    padding: 6px;
    width: 440px;
    box-shadow: 0 0 0 2px #e87a20, 0 8px 40px rgba(0,0,0,0.8);
  }
  .inner {
    background: #1a0e00;
    border-radius: 27px;
    padding: 20px;
    border: 1px solid #3a2000;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }
  .logo {
    font-size: 22px;
    font-weight: bold;
    color: #ff9933;
    letter-spacing: 4px;
    text-shadow: 0 0 6px rgba(255, 153, 51, 0.6);
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
    animation: blink 2s infinite;
    box-shadow: 0 0 6px #ff8800;
  }
  @keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.2; }
  }
  
  /* DISPLAY ESTILO RETRO CRT / TVA */
  .screen {
    background: #060300;
    border-radius: 12px;
    border: 1px solid #ff880044;
    padding: 12px;
    height: 160px;
    overflow-y: auto;
    margin-bottom: 16px;
    font-family: 'VT323', monospace;
    font-size: 17px;
    letter-spacing: 1px;
    color: #ff9900;
    line-height: 1.3;
    
    /* Efeito de iluminação de fósforo laranja */
    text-shadow: 0 0 5px rgba(255, 136, 0, 0.7);
    box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.9);
  }
  .screen::-webkit-scrollbar { width: 4px; }
  .screen::-webkit-scrollbar-thumb { background: #5a3000; border-radius: 2px; }
  
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 10px;
  }
  .btn {
    background: #1f0f00;
    border: 1px solid #5a3000;
    border-radius: 12px;
    padding: 12px 8px;
    color: #ff9933;
    font-family: 'VT323', monospace;
    font-size: 16px;
    letter-spacing: 1px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    transition: all 0.15s;
    text-align: center;
  }
  .btn:hover { 
    background: #2e1800; 
    border-color: #ff8800;
    box-shadow: 0 0 10px rgba(255, 136, 0, 0.2);
  }
  .btn:active { transform: scale(0.97); }
  .btn-icon { font-size: 22px; }
  .btn-sub { color: #884400; font-size: 13px; font-family: 'VT323', monospace; }
  .btn-exit {
    width: 100%;
    background: #2a0a00;
    border: 1px solid #6a2000;
    border-radius: 12px;
    padding: 10px;
    color: #ff4400;
    font-family: 'VT323', monospace;
    font-size: 16px;
    cursor: pointer;
    letter-spacing: 2px;
    margin-top: 4px;
    text-shadow: 0 0 4px rgba(255, 68, 0, 0.5);
  }
  .btn-exit:hover { background: #3a1500; border-color: #ff4400; }
  .divider { height: 1px; background: #3a1800; margin: 12px 0; }
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
  }
  .dot-row { display: flex; gap: 5px; }
  .dot-sm {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #5a3000;
  }
  .dot-sm.active { background: #ff8800; animation: blink 2s infinite; box-shadow: 0 0 4px #ff8800; }
  .running { border-color: #ff8800 !important; background: #2a1400 !important; }
</style>
</head>
<body>
<div class="device">
  <div class="inner">
    <div class="header">
      <span class="logo">TEMPAD</span>
      <div class="status">
        TVA TOOLS v3.0<br>
        <span id="clock"></span>
        <span class="dot"></span>
      </div>
    </div>

    <div class="screen" id="log">
&gt; TVA TemPad v3.0 inicializado...<br>
&gt; Bem-vindo, Agente.<br>
&gt; Selecione um módulo abaixo.
    </div>

    <div class="grid">
      <button class="btn" onclick="rodar('disk', this)">
        <span class="btn-icon">💿</span>
        <span>Verificar Disco</span>
        <span class="btn-sub">chkdsk / SFC / DISM</span>
      </button>
      <button class="btn" onclick="rodar('optim', this)">
        <span class="btn-icon">⚡</span>
        <span>Otimizar PC</span>
        <span class="btn-sub">TEMP / Lixeira</span>
      </button>
      <button class="btn" onclick="rodar('net', this)">
        <span class="btn-icon">🌐</span>
        <span>Diagnóstico Rede</span>
        <span class="btn-sub">Ping / Tracert</span>
      </button>
      <button class="btn" onclick="rodar('sec', this)">
        <span class="btn-icon">🔒</span>
        <span>Segurança</span>
        <span class="btn-sub">Defender / SFC</span>
      </button>
    </div>

    <div class="divider"></div>
    <button class="btn-exit" onclick="window.close()">ENCERRAR SESSÃO</button>

    <div class="footer">
      <div class="dot-row">
        <div class="dot-sm active"></div>
        <div class="dot-sm"></div>
        <div class="dot-sm"></div>
      </div>
      <span style="font-size:12px;color:#6a3800;">AUTORIDADE DE VARIÂNCIA TEMPORAL</span>
    </div>
  </div>
</div>

<script>
function log(msg) {
  const el = document.getElementById('log');
  el.innerHTML += '<br>' + msg;
  el.scrollTop = el.scrollHeight;
}

function rodar(modulo, btn) {
  btn.classList.add('running');
  btn.disabled = true;
  log('<br>&gt; --- Iniciando módulo: ' + modulo + ' ---');

  const source = new EventSource('/rodar/' + modulo);
  source.onmessage = function(e) {
    log('&gt; ' + e.data);
  };
  source.onerror = function() {
    source.close();
    btn.classList.remove('running');
    btn.disabled = false;
    log('&gt; --- Módulo concluído ---');
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

# ============================================
# ROTAS
# ============================================

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/rodar/<modulo>')
def rodar(modulo):
    """Executa o script e retorna saída em tempo real via SSE"""

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

        # -u garante o streaming de stdout sem buffering
        processo = subprocess.Popen(
            ['python', '-u', caminho],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for linha in processo.stdout:
            yield f"data: {linha.strip()}\n\n"

        processo.wait()
        yield f"data: ✅ Concluído!\n\n"

    return Response(gerar(), mimetype='text/event-stream')

# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == '__main__':
    print("🚀 TemPad Web iniciado!")
    print("📡 Acesse: http://localhost:5000")
    app.run(debug=False, port=5000)

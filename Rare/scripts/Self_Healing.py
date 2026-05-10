import subprocess
import psutil
import os
import time
import logging
from datetime import datetime

# ============================================
# Self-Healing System
# Criado por: Matheus Iasin
# Versao: 1.0
# Descricao: Sistema autonomo de auto-cura
#            para ambientes corporativos
# ============================================

# Configuracao do log
logging.basicConfig(
    filename="C:\\self_healing.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(mensagem):
    """Registra evento no log e exibe no terminal"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}")
    logging.info(mensagem)

# ============================================
# MODULO 1 — Fila de Impressao
# ============================================

def verificar_fila_impressao():
    """Verifica se o spooler esta travado e corrige"""
    try:
        resultado = subprocess.run(
            ["sc", "query", "spooler"],
            capture_output=True, text=True
        )
        if "RUNNING" not in resultado.stdout:
            log("⚠️  Spooler de impressao parado — iniciando auto-cura...")
            subprocess.run(["net", "stop", "spooler"], capture_output=True)
            # Limpa fila de impressao
            spool_path = r"C:\Windows\System32\spool\PRINTERS"
            for arquivo in os.listdir(spool_path):
                try:
                    os.remove(os.path.join(spool_path, arquivo))
                except:
                    pass
            subprocess.run(["net", "start", "spooler"], capture_output=True)
            log("✅  Spooler reiniciado e fila limpa com sucesso!")
        else:
            log("✅  Spooler de impressao OK")
    except Exception as e:
        log(f"❌  Erro ao verificar spooler: {e}")

# ============================================
# MODULO 2 — Disco Cheio
# ============================================

def verificar_disco():
    """Verifica uso do disco e limpa se necessario"""
    try:
        uso = psutil.disk_usage("C:\\")
        percentual = uso.percent
        log(f"💿  Disco C: {percentual}% usado")

        if percentual >= 90:
            log("⚠️  Disco acima de 90% — iniciando limpeza automatica...")
            # Limpa temporarios
            subprocess.run("del /s /f /q %TEMP%\\*", shell=True, capture_output=True)
            subprocess.run("del /s /f /q C:\\Windows\\Temp\\*", shell=True, capture_output=True)
            subprocess.run("del /s /f /q C:\\Windows\\Prefetch\\*", shell=True, capture_output=True)
            # Esvazia lixeira
            subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin -Force"],
                capture_output=True
            )
            log("✅  Limpeza automatica concluida!")
        else:
            log("✅  Espaco em disco OK")
    except Exception as e:
        log(f"❌  Erro ao verificar disco: {e}")

# ============================================
# MODULO 3 — Conectividade de Rede
# ============================================

def verificar_rede():
    """Verifica conectividade e corrige se necessario"""
    try:
        resultado = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", "8.8.8.8"],
            capture_output=True, text=True
        )
        if resultado.returncode != 0:
            log("⚠️  Sem conectividade — iniciando auto-cura de rede...")
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
            subprocess.run(["ipconfig", "/release"], capture_output=True)
            subprocess.run(["ipconfig", "/renew"], capture_output=True)
            log("✅  Rede reiniciada — DNS limpo, IP renovado!")
        else:
            log("✅  Conectividade de rede OK")
    except Exception as e:
        log(f"❌  Erro ao verificar rede: {e}")

# ============================================
# MODULO 4 — Servicos Criticos
# ============================================

SERVICOS_CRITICOS = [
    "wuauserv",   # Windows Update
    "bits",       # Background Intelligent Transfer
    "dhcp",       # Cliente DHCP
    "dnscache",   # Cache DNS
]

def verificar_servicos():
    """Verifica e reinicia servicos criticos parados"""
    for servico in SERVICOS_CRITICOS:
        try:
            resultado = subprocess.run(
                ["sc", "query", servico],
                capture_output=True, text=True
            )
            if "RUNNING" not in resultado.stdout:
                log(f"⚠️  Servico '{servico}' parado — reiniciando...")
                subprocess.run(["net", "start", servico], capture_output=True)
                log(f"✅  Servico '{servico}' reiniciado!")
            else:
                log(f"✅  Servico '{servico}' OK")
        except Exception as e:
            log(f"❌  Erro ao verificar servico {servico}: {e}")

# ============================================
# MODULO 5 — Uso de Memoria
# ============================================

def verificar_memoria():
    """Verifica uso de RAM e alerta se critico"""
    try:
        mem = psutil.virtual_memory()
        percentual = mem.percent
        log(f"🧠  Memoria RAM: {percentual}% em uso")

        if percentual >= 90:
            log("⚠️  Memoria acima de 90% — registrando processos pesados...")
            processos = sorted(
                psutil.process_iter(['pid', 'name', 'memory_percent']),
                key=lambda p: p.info['memory_percent'],
                reverse=True
            )[:5]
            for p in processos:
                log(f"   🔴 PID {p.info['pid']} | {p.info['name']} | {p.info['memory_percent']:.1f}%")
        else:
            log("✅  Uso de memoria OK")
    except Exception as e:
        log(f"❌  Erro ao verificar memoria: {e}")

# ============================================
# LOOP PRINCIPAL
# ============================================

def executar_ciclo():
    """Executa um ciclo completo de verificacao"""
    log("=" * 50)
    log("🔄  Iniciando ciclo de auto-cura...")
    log("=" * 50)
    verificar_fila_impressao()
    verificar_disco()
    verificar_rede()
    verificar_servicos()
    verificar_memoria()
    log("=" * 50)
    log("✅  Ciclo concluido — aguardando proximo ciclo...")
    log("=" * 50)

if __name__ == "__main__":
    log("🚀  Self-Healing System iniciado!")
    log("📄  Log salvo em: C:\\self_healing.log")

    # Roda a cada 5 minutos
    INTERVALO = 300

    while True:
        executar_ciclo()
        time.sleep(INTERVALO)

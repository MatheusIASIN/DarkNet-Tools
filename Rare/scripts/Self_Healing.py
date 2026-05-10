"""
============================================
Self-Healing System
Criado por: Matheus Iasin
Versao: 2.0
Python: 3.14+ compatível
Descricao: Sistema autonomo de auto-cura
           para ambientes corporativos de
           alta criticidade (ex: aeroportos)
============================================

DEPENDENCIAS:
    pip install psutil

COMO RODAR COMO SERVICO WINDOWS:
    1. Instale o NSSM: https://nssm.cc/
    2. nssm install SelfHealing python self_healing_v2.py
    3. nssm start SelfHealing

LOG:
    C:\\self_healing.log
============================================
"""

import subprocess
import psutil
import os
import time
import logging
from datetime import datetime
from pathlib import Path  # Python 3.4+ — mais moderno que os.path

# ============================================
# CONFIGURACAO DO SISTEMA
# ============================================

# Intervalo entre ciclos de verificacao (em segundos)
INTERVALO_CICLO: int = 300  # 5 minutos

# Limite de uso de disco para acionar limpeza (%)
LIMITE_DISCO: int = 90

# Limite de uso de RAM para acionar alerta (%)
LIMITE_MEMORIA: int = 90

# Caminho do arquivo de log — usa Path para compatibilidade total
LOG_PATH: Path = Path("C:/self_healing.log")

# Servicos criticos que devem estar sempre rodando
# Adicione ou remova servicos conforme o ambiente
SERVICOS_CRITICOS: list[str] = [
    "wuauserv",   # Windows Update
    "bits",       # Background Intelligent Transfer
    "dhcp",       # Cliente DHCP
    "dnscache",   # Cache DNS
    "spooler",    # Spooler de impressao
]

# ============================================
# CONFIGURACAO DO LOG
# ============================================

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"  # Python 3.9+ — garante suporte a caracteres especiais
)

def log(mensagem: str) -> None:
    """
    Registra uma mensagem no arquivo de log e exibe no terminal.

    Args:
        mensagem: Texto a ser registrado
    """
    hora_atual = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora_atual}] {mensagem}")
    logging.info(mensagem)


# ============================================
# MODULO 1 — Fila de Impressao
# ============================================

def verificar_fila_impressao() -> None:
    """
    Verifica se o spooler de impressao esta rodando.
    Se estiver parado, limpa a fila e reinicia o servico.

    Critico em ambientes com impressoras de alto volume
    como check-in de aeroportos.
    """
    try:
        # Consulta o status do servico spooler
        resultado = subprocess.run(
            ["sc", "query", "spooler"],
            capture_output=True,
            text=True
        )

        if "RUNNING" not in resultado.stdout:
            log("⚠️  Spooler parado — iniciando auto-cura...")

            # Para o servico antes de limpar a fila
            subprocess.run(["net", "stop", "spooler"], capture_output=True)

            # Limpa todos os arquivos da fila de impressao
            # Path.iterdir() e mais pythônico que os.listdir()
            spool_path = Path(r"C:\Windows\System32\spool\PRINTERS")
            for arquivo in spool_path.iterdir():
                try:
                    arquivo.unlink()  # Path.unlink() substitui os.remove()
                except PermissionError:
                    pass  # Arquivo em uso — ignora e continua

            # Reinicia o servico apos limpeza
            subprocess.run(["net", "start", "spooler"], capture_output=True)
            log("✅  Spooler reiniciado e fila limpa!")
        else:
            log("✅  Spooler de impressao OK")

    except Exception as e:
        log(f"❌  Erro ao verificar spooler: {e}")


# ============================================
# MODULO 2 — Disco Cheio
# ============================================

def verificar_disco() -> None:
    """
    Monitora o uso do disco C:.
    Se ultrapassar o limite definido, executa limpeza automatica
    de temporarios, prefetch e lixeira.
    """
    try:
        uso = psutil.disk_usage("C:\\")
        percentual: float = uso.percent
        log(f"💿  Disco C: {percentual:.1f}% usado")

        if percentual >= LIMITE_DISCO:
            log(f"⚠️  Disco acima de {LIMITE_DISCO}% — limpando...")

            # Lista de pastas temporarias para limpar
            pastas_temp: list[str] = [
                "%TEMP%",
                r"C:\Windows\Temp",
                r"C:\Windows\Prefetch",
            ]

            for pasta in pastas_temp:
                subprocess.run(
                    f'del /s /f /q "{pasta}\\*"',
                    shell=True,
                    capture_output=True
                )
                log(f"   🗑️  Limpando: {pasta}")

            # Esvazia lixeira via PowerShell
            subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin -Force"],
                capture_output=True
            )

            # Exibe espaco apos limpeza
            novo_uso = psutil.disk_usage("C:\\")
            log(f"✅  Limpeza concluida! Disco agora: {novo_uso.percent:.1f}%")
        else:
            log("✅  Espaco em disco OK")

    except Exception as e:
        log(f"❌  Erro ao verificar disco: {e}")


# ============================================
# MODULO 3 — Conectividade de Rede
# ============================================

def verificar_rede() -> None:
    """
    Testa conectividade com a internet via ping no 8.8.8.8.
    Se falhar, executa sequencia de auto-cura:
    flush DNS → release IP → renew IP.
    """
    try:
        # Ping unico com timeout de 1 segundo
        resultado = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", "8.8.8.8"],
            capture_output=True,
            text=True
        )

        if resultado.returncode != 0:
            log("⚠️  Sem conectividade — auto-cura de rede...")

            # Sequencia de recuperacao de rede
            comandos_rede: list[list[str]] = [
                ["ipconfig", "/flushdns"],   # Limpa cache DNS
                ["ipconfig", "/release"],    # Libera IP atual
                ["ipconfig", "/renew"],      # Solicita novo IP ao DHCP
            ]

            for cmd in comandos_rede:
                subprocess.run(cmd, capture_output=True)
                log(f"   🔧 Executado: {' '.join(cmd)}")

            log("✅  Rede reiniciada!")
        else:
            log("✅  Conectividade de rede OK")

    except Exception as e:
        log(f"❌  Erro ao verificar rede: {e}")


# ============================================
# MODULO 4 — Servicos Criticos
# ============================================

def verificar_servicos() -> None:
    """
    Verifica se todos os servicos criticos estao rodando.
    Tenta reiniciar automaticamente qualquer servico parado.

    A lista SERVICOS_CRITICOS e configuravel no topo do arquivo.
    """
    for servico in SERVICOS_CRITICOS:
        try:
            resultado = subprocess.run(
                ["sc", "query", servico],
                capture_output=True,
                text=True
            )

            if "RUNNING" not in resultado.stdout:
                log(f"⚠️  Servico '{servico}' parado — reiniciando...")
                reinicio = subprocess.run(
                    ["net", "start", servico],
                    capture_output=True,
                    text=True
                )

                # Verifica se o reinicio teve sucesso
                if reinicio.returncode == 0:
                    log(f"✅  Servico '{servico}' reiniciado!")
                else:
                    log(f"❌  Falha ao reiniciar '{servico}': {reinicio.stderr.strip()}")
            else:
                log(f"✅  Servico '{servico}' OK")

        except Exception as e:
            log(f"❌  Erro ao verificar servico '{servico}': {e}")


# ============================================
# MODULO 5 — Uso de Memoria
# ============================================

def verificar_memoria() -> None:
    """
    Monitora o uso de memoria RAM.
    Se ultrapassar o limite, lista os 5 processos
    que mais consomem memoria para analise no log.
    """
    try:
        mem = psutil.virtual_memory()
        percentual: float = mem.percent

        # Converte bytes para GB para exibicao mais legivel
        total_gb: float = mem.total / (1024 ** 3)
        usado_gb: float = mem.used / (1024 ** 3)

        log(f"🧠  RAM: {usado_gb:.1f}GB / {total_gb:.1f}GB ({percentual:.1f}%)")

        if percentual >= LIMITE_MEMORIA:
            log(f"⚠️  Memoria acima de {LIMITE_MEMORIA}% — listando processos...")

            # Ordena processos por consumo de memoria (maior primeiro)
            processos = sorted(
                psutil.process_iter(["pid", "name", "memory_percent"]),
                key=lambda p: p.info["memory_percent"] or 0,
                reverse=True
            )[:5]  # Top 5 processos

            for proc in processos:
                log(
                    f"   🔴 PID {proc.info['pid']:>6} | "
                    f"{proc.info['name']:<30} | "
                    f"{proc.info['memory_percent']:.1f}%"
                )
        else:
            log("✅  Uso de memoria OK")

    except Exception as e:
        log(f"❌  Erro ao verificar memoria: {e}")


# ============================================
# LOOP PRINCIPAL
# ============================================

def executar_ciclo() -> None:
    """
    Executa um ciclo completo de verificacao e auto-cura.
    Chama todos os modulos em sequencia e registra o resultado.
    """
    separador = "=" * 50
    log(separador)
    log("🔄  Iniciando ciclo de auto-cura...")
    log(separador)

    verificar_fila_impressao()
    verificar_disco()
    verificar_rede()
    verificar_servicos()
    verificar_memoria()

    log(separador)
    log(f"✅  Ciclo concluido — proximo em {INTERVALO_CICLO // 60} minutos")
    log(separador)


def main() -> None:
    """
    Ponto de entrada do programa.
    Inicia o loop infinito de monitoramento e auto-cura.
    """
    log("🚀  Self-Healing System v2.0 iniciado!")
    log(f"📄  Log: {LOG_PATH}")
    log(f"⏱️   Intervalo: {INTERVALO_CICLO // 60} minutos")
    log(f"💾  Limite disco: {LIMITE_DISCO}%")
    log(f"🧠  Limite RAM: {LIMITE_MEMORIA}%")

    # Loop infinito — roda enquanto o servico estiver ativo
    while True:
        executar_ciclo()
        time.sleep(INTERVALO_CICLO)


# Ponto de entrada padrao do Python
if __name__ == "__main__":
    main()

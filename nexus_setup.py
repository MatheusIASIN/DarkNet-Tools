#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 TIME VARIANCE AUTHORITY — NEXUS INSTALLATION ENGINE (nexus_setup.py)
 -----------------------------------------------------------------------------
 Módulo de Bootstrap Nativo & Diagnóstico de Hardware da TVA.
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
            # ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING
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
# Módulos Necessários no Stack (FastAPI / WebSockets / Timedoor / Spatial)
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
# Inspeção Nativa de Hardware e Sistema Operacional
# ---------------------------------------------------------------------------
def is_admin() -> bool:
    """Verifica se o script está rodando com privilégios de Admin/Root."""
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.getuid() == 0
    except Exception:
        return False

def get_hostname() -> str:
    """Retorna o nome da máquina / dispositivo."""
    return platform.node() or os.getenv('COMPUTERNAME', 'Unknown')

def get_detailed_os() -> str:
    """Detecta a distribuição Linux exata (ex: Ubuntu no Colab), Windows ou macOS."""
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
    """Detecta a marca e modelo exato do processador."""
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
    """Detecta a GPU principal via PowerShell (Windows) ou lspci (Linux)."""
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
    """Calcula a memória RAM total e disponível."""
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
    """Mede o espaço em disco e identifica se a unidade é SSD ou HDD."""
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
    """Projeta a banner ASCII com animação de varredura estilo monitor da TVA."""
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
        # Destaca temporariamente a linha que está sendo 'varrida' em tom brilhante
        if animado:
            sys.stdout.write(f"{CLR_BRIGHT}{line}{CLR_RESET}\n")
            sys.stdout.flush()
            time.sleep(0.035)
            # Retorna para a cor âmbar padrão
            sys.stdout.write(f"\033[F{CLR_AMBER}{line}{CLR_RESET}\n")
        else:
            print(f"{CLR_AMBER}{line}{CLR_RESET}")

def barra_progresso_tva(atual: int, total: int, prefixo: str = "", largura: int = 25) -> None:
    """Exibe uma barra de carregamento dinâmica estilo TemPad."""
    percentual = atual / float(total)
    preenchidos = int(largura * percentual)
    barra = '█' * preenchidos + '░' * (largura - preenchidos)
    sys.stdout.write(
        f"\r {CLR_DIM}│{CLR_RESET} {prefixo:<22} {CLR_AMBER}[{barra}]{CLR_RESET} {CLR_BRIGHT}{int(percentual * 100):>3}%{CLR_RESET}"
    )
    sys.stdout.flush()
    if atual == total:
        sys.stdout.write("\n")

def efeito_glitch(texto_final: str, duracao_frames: int = 5) -> None:
    """Animação que decodifica o texto caractere por caractere."""
    chars = string.ascii_uppercase + string.digits + "!@#$%^&*"
    texto_atual = [" "] * len(texto_final)
    
    for i in range(len(texto_final)):
        for _ in range(duracao_frames):
            char_temp = random.choice(chars)
            sys.stdout.write(f"\r{CLR_AMBER}{''.join(texto_atual[:i])}{CLR_BRIGHT}{char_temp}{CLR_RESET}")
            sys.stdout.flush()
            time.sleep(0.01)
        texto_atual[i] = texto_final[i]
    
    sys.stdout.write(f"\r{CLR_GREEN}{''.join(texto_final)}{CLR_RESET}\n")

def spinner_tva(mensagem: str, segundos: float = 1.0) -> None:
    """Indicador animado de carregamento estilo TVA."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    fim = time.time() + segundos
    i = 0
    while time.time() < fim:
        sys.stdout.write(f"\r{CLR_AMBER}{frames[i % len(frames)]}{CLR_RESET} {mensagem}...")
        sys.stdout.flush()
        time.sleep(0.07)
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
        
        time.sleep(0.08)
        barra_progresso_tva(idx, total_pacotes, prefixo=f"CHECANDO {pip_name[:12]}")

    print(f"{CLR_DIM}└" + "─" * (width - 1) + "┘" + CLR_RESET)
    return failed

# ---------------------------------------------------------------------------
# Execução Principal
# ---------------------------------------------------------------------------
def main() -> None:
    render_banner(animado=True)
    print()

    # Spinners de Inicialização estilo TVA
    spinner_tva("SINCRONIZANDO COM AETHERNEXUS CHRONOS", 1.2)
    spinner_tva("INSPECIONANDO HARDWARE DO DISPOSITIVO", 0.8)

    # Leitura e Impressão das Informações do Dispositivo
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

    # Checagem do PIP com Barra de Carregamento
    failed_packages = check_and_install_packages()

    # Diagnóstico Final
    print(f"\n{CLR_DIM}┌──[{CLR_RESET} {CLR_BRIGHT}DIAGNÓSTICO FINAL{CLR_RESET} {CLR_DIM}]" + "─" * 45 + "┐" + CLR_RESET)
    if failed_packages:
        print(f" {CLR_DIM}│{CLR_RESET} {CLR_RED}[!] FALHA AO INSTALAR: {', '.join(failed_packages)}{CLR_RESET}")
    else:
        sys.stdout.write(f" {CLR_DIM}│{CLR_RESET} ")
        efeito_glitch("[✓] NENHUM EVENTO NEXUS DETECTADO. AETHERNEXUS-CHRONOS OS ONLINE!")
    print(f"{CLR_DIM}└" + "─" * 67 + "┘" + CLR_RESET)

    print(f"\n{CLR_AMBER}▶ Digite {CLR_BRIGHT}python main_web.py{CLR_AMBER} para iniciar o TemPad OS.{CLR_RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{CLR_RED}[!] Instalação interrompida pelo usuário.{CLR_RESET}\n")
    except Exception as err:
        print(f"\n{CLR_RED}[X] ERRO CRÍTICO DURANTE O SETUP: {err}{CLR_RESET}\n")
        

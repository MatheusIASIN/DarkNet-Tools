import os
import sys
import subprocess
import ctypes
import time
import psutil
import platform
from datetime import datetime

# 🎨 Cores ANSI para Terminal / Log Web
class Cor:
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    VERMELHO = "\033[91m"
    RESET = "\033[0m"

# 📜 Sistema de Logs Resiliente
class Logger:
    LOG_PATH = "C:\\manutencao_sistema.log" if platform.system() == "Windows" else "manutencao_sistema.log"

    @staticmethod
    def registrar(mensagem):
        """Registra eventos em arquivo sem travar caso haja erro de escrita"""
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem_formatada = f"[{data_hora}] {mensagem}\n"
        
        try:
            with open(Logger.LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(mensagem_formatada)
        except Exception:
            pass  # Ignora erros de escrita em unidades sem permissão

# 🔧 Núcleo de Manutenção do Sistema
class ManutencaoSistema:
    def __init__(self):
        self.verificar_permissoes()

    def verificar_permissoes(self):
        """Verifica privilégios administrativos no Windows"""
        if platform.system() != "Windows":
            print(f"{Cor.AMARELO}⚠️ Modo de compatibilidade ativado (Ambiente não-Windows detected).{Cor.RESET}", flush=True)
            return

        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print(f"{Cor.VERMELHO}⚠️ ALERTA: Execute o script como Administrador para obter acesso completo.{Cor.RESET}", flush=True)
        except AttributeError:
            pass

    def listar_drives(self):
        """Lista os discos disponíveis no sistema"""
        particoes = psutil.disk_partitions()
        return [p.device.replace(":\\", "").replace("/", "") for p in particoes]

    def info_disco(self):
        """Exibe informações de uso e capacidade de cada partição"""
        print(f"{Cor.AZUL}📊 Detalhes dos Discos:{Cor.RESET}", flush=True)
        for particao in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(particao.mountpoint)
                print(f"📂 Disco: {particao.device}", flush=True)
                print(f"   📏 Total: {uso.total / (1024 ** 3):.2f} GB", flush=True)
                print(f"   🟢 Livre: {uso.free / (1024 ** 3):.2f} GB", flush=True)
                print(f"   🔴 Usado: {uso.percent}%", flush=True)
                Logger.registrar(f"Uso do disco {particao.device}: {uso.percent}%")
            except PermissionError:
                print(f"   ⚠️ Acesso negado para {particao.device}", flush=True)
            except Exception as e:
                print(f"   ⚠️ Erro ao ler partição {particao.device}: {e}", flush=True)

    def diagnostico_sistema(self):
        """Executa reparos SFC e DISM no Windows"""
        if platform.system() != "Windows":
            print(f"{Cor.AMARELO}⚠️ Diagnóstico SFC/DISM disponível apenas no Windows.{Cor.RESET}", flush=True)
            return

        print(f"{Cor.AZUL}🔍 Executando verificação de arquivos (SFC)...{Cor.RESET}", flush=True)
        subprocess.run("sfc /scannow", shell=True)
        Logger.registrar("Comando SFC/Scannow executado.")

        print(f"{Cor.AZUL}🛠️ Executando reparo de imagem (DISM)...{Cor.RESET}", flush=True)
        subprocess.run("DISM /Online /Cleanup-Image /RestoreHealth", shell=True)
        Logger.registrar("Comando DISM RestoreHealth executado.")

    def verificar_hd(self):
        """Verifica integridade S.M.A.R.T dos discos via WMIC"""
        if platform.system() != "Windows":
            print(f"{Cor.AMARELO}⚠️ Verificação de saúde de hardware (WMIC) restrita ao Windows.{Cor.RESET}", flush=True)
            return

        print(f"{Cor.AZUL}💾 Verificando status de integridade do HD/SSD...{Cor.RESET}", flush=True)
        subprocess.run("wmic diskdrive get model, status", shell=True)
        Logger.registrar("Saúde física do HD/SSD consultada via WMIC.")

    def executar_modo_tempad(self):
        """Rotina automática otimizada para o TemPad Web"""
        print(f"{Cor.AZUL}🚀 [MÓDULO DISCO] Análise iniciada pelo TemPad...{Cor.RESET}\n", flush=True)
        self.info_disco()
        time.sleep(1)
        self.verificar_hd()
        time.sleep(1)
        self.diagnostico_sistema()

# 📜 Menu para execução manual no terminal
class Menu:
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir(self):
        while True:
            print(f"\n{Cor.AZUL}🔧 Painel de Manutenção do Sistema{Cor.RESET}")
            print("[1] Listar discos disponíveis")
            print("[2] Informações de capacidade de disco")
            print("[3] Saúde física dos discos (WMIC)")
            print("[4] Diagnóstico completo do Windows (SFC/DISM)")
            print("[5] Executar análise completa (Modo TemPad)")
            print("[0] Sair")

            escolha = input("\n👉 Escolha uma opção: ").strip()

            if escolha == "1":
                print(f"\nDiscos detectados: {', '.join(self.sistema.listar_drives())}")
            elif escolha == "2":
                self.sistema.info_disco()
            elif escolha == "3":
                self.sistema.verificar_hd()
            elif escolha == "4":
                self.sistema.diagnostico_sistema()
            elif escolha == "5":
                self.sistema.executar_modo_tempad()
            elif escolha == "0":
                print("Encerrando...")
                break
            else:
                print(f"{Cor.VERMELHO}Opção inválida!{Cor.RESET}")

# 🚀 Ponto de Entrada
if __name__ == "__main__":
    sistema = ManutencaoSistema()
    
    # Se chamado via subprocess ou sem terminal interativo (ex: pelo TemPad Web)
    if not sys.stdin.isatty():
        sistema.executar_modo_tempad()
    else:
        Menu(sistema).exibir()

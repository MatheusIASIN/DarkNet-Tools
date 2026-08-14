import os
import subprocess
import ctypes
import time
import psutil
from datetime import datetime

import platform

if platform.system() != "Windows":
    print("⚠️ Este módulo só funciona no Windows.")
    exit()

# 🎨 Cores para terminal
class Cor:
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    VERMELHO = "\033[91m"
    RESET = "\033[0m"

# 📜 Classe para manipular logs
class Logger:
    LOG_PATH = "C:\\manutencao_sistema.log"

    @staticmethod
    def registrar(mensagem):
        """Registra eventos no log e exibe no terminal"""
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem_formatada = f"[{data_hora}] {mensagem}\n"
        
        with open(Logger.LOG_PATH, "a") as log_file:
            log_file.write(mensagem_formatada)
        
        print(Cor.AMARELO + mensagem + Cor.RESET)

# 🔧 Classe principal para manutenção do sistema
class ManutencaoSistema:
    def __init__(self):
        self.verificar_permissoes()

    def verificar_permissoes(self):
        """Verifica se o script está rodando como administrador"""
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print(Cor.VERMELHO + "⚠️ Este script precisa ser executado como Administrador!" + Cor.RESET)
            input("Pressione ENTER para sair...")
            exit()

    def listar_drives(self):
        """Lista os discos disponíveis no sistema"""
        particoes = psutil.disk_partitions()
        discos = [p.device.replace(":\\", "") for p in particoes]
        return discos

    def disco_em_uso(self, drive):
        """Verifica se um disco está em uso por processos"""
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                if proc.info['open_files']:
                    for arquivo in proc.info['open_files']:
                        if arquivo.path.startswith(f"{drive}:"):
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    def verificar_disco(self, drive="C"):
        """Executa a verificação do disco com opções avançadas"""
        log_path = f"C:\\chkdsk_{drive}.log"

        if self.disco_em_uso(drive):
            print(f"{Cor.AMARELO}⚠️ O disco {drive}: está em uso. Deseja agendar a verificação no próximo boot? (S/N){Cor.RESET}")
            opcao = input("👉 ").strip().lower()
            if opcao == 's':
                subprocess.run(f'chkntfs /C {drive}:', shell=True)
                print(f"{Cor.VERDE}✅ Verificação do disco {drive}: foi agendada para o próximo boot.{Cor.RESET}")
                Logger.registrar(f"Verificação agendada para {drive}: no próximo boot.")
            return

        try:
            print(f"{Cor.AZUL}📀 Iniciando verificação do disco {drive}: ...{Cor.RESET}")
            comando = f'chkdsk {drive}: /f /r > "{log_path}"'
            subprocess.run(["cmd", "/c", "start", "cmd", "/k", comando], shell=True)
            print(f"{Cor.VERDE}✅ Verificação do disco {drive}: iniciada!{Cor.RESET}")
            print(f"{Cor.AMARELO}📄 O relatório será salvo em: {log_path}{Cor.RESET}")
            Logger.registrar(f"Verificação iniciada no disco {drive}.")

        except subprocess.CalledProcessError as e:
            print(f"{Cor.VERMELHO}❌ Erro ao executar o comando: {e}{Cor.RESET}")
            Logger.registrar(f"Erro na verificação do disco {drive}: {e}")
        except Exception as e:
            print(f"{Cor.VERMELHO}⚠️ Ocorreu um erro inesperado: {e}{Cor.RESET}")
            Logger.registrar(f"Erro inesperado na verificação do disco {drive}: {e}")

    def diagnostico_sistema(self):
        """Executa diagnóstico e reparo do Windows"""
        print(f"{Cor.AZUL}\n🔍 **Verificando arquivos do sistema**...{Cor.RESET}")
        subprocess.run("sfc /scannow", shell=True)
        Logger.registrar("Verificação SFC executada.")

        print(f"{Cor.AZUL}\n🛠️ **Reparando a imagem do Windows**...{Cor.RESET}")
        subprocess.run("DISM /Online /Cleanup-Image /RestoreHealth", shell=True)
        Logger.registrar("Reparo DISM executado.")

    def verificar_hd(self):
        """Verifica a integridade física do HD/SSD"""
        print(f"{Cor.AZUL}\n💾 **Verificando o estado do HD/SSD**...{Cor.RESET}")
        subprocess.run("wmic diskdrive get model, status", shell=True)
        Logger.registrar("Estado do HD/SSD verificado.")

    def info_disco(self):
        """Exibe informações detalhadas dos discos"""
        print(f"{Cor.AZUL}\n📊 **Detalhes dos Discos**:{Cor.RESET}")
        for particao in psutil.disk_partitions():
            uso = psutil.disk_usage(particao.mountpoint)
            print(f"\n📂 Disco: {particao.device}")
            print(f"   📏 Total: {uso.total / (1024 ** 3):.2f} GB")
            print(f"   🟢 Livre: {uso.free / (1024 ** 3):.2f} GB")
            print(f"   🔴 Usado: {uso.percent}%")
            Logger.registrar(f"Informações do disco {particao.device} verificadas.")
            time.sleep(1)

# 📜 Classe para o menu interativo
class Menu:
    def __init__(self):
        self.sistema = ManutencaoSistema()

    def exibir(self):
        """Exibe o menu principal"""
        while True:
            print(f"\n{Cor.AZUL}🔧 **Painel de Manutenção do Sistema**{Cor.RESET}")
            print("[1] Verificar discos disponíveis")
            print("[2] Verificar um disco específico")
            print("[3] Diagnóstico do Windows (SFC/DISM)")
            print("[4] Verificar saúde do HD/SSD")
            print("[5] Exibir informações detalhadas dos discos")
            print("[0] Sair")

            escolha = input("Digite a opção desejada: ").strip()

            if escolha == "1":
                print("\n💾 Discos disponíveis no sistema:")
                for disco in self.sistema.listar_drives():
                    print(f"   🔹 {disco}:")
            elif escolha == "2":
                drive = input("Digite a letra do disco (ex: C, D, E...): ").upper()
                self.sistema.verificar_disco(drive)
            elif escolha == "3":
                self.sistema.diagnostico_sistema()
            elif escolha == "4":
                self.sistema.verificar_hd()
            elif escolha == "5":
                self.sistema.info_disco()
            elif escolha == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida! Tente novamente.")

# 🚀 Executa o programa
if __name__ == "__main__":
    Menu().exibir()

import subprocess
import sys
import importlib.metadata

# Função para verificar se o pacote está instalado
def is_package_installed(package_name):
    try:
        # Tenta obter a distribuição do pacote
        importlib.metadata.metadata(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False

# Função para instalar o pacote
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Função para verificar e instalar os pacotes
def check_and_install():
    packages = ["pygame", "playsound", "requests", "Pillow", "tkinter", "psutil"]

    for package in packages:
        print(f"[🔄] Verificando {package}...")
        
        if package == "tkinter":
            if is_package_installed(package):
                print(f"[✓] {package} já está instalado.")
            else:
                print(f"[!] {package} não está instalado. Não é possível instalar via pip. Verifique se o tkinter está disponível ou reinstale o Python.")
        else:
            if is_package_installed(package):
                print(f"[✓] {package} já está instalado.")
            else:
                print(f"[!] {package} não está instalado. Instalando...")
                try:
                    install(package)
                    print(f"[✓] {package} instalado com sucesso.")
                except subprocess.CalledProcessError:
                    print(f"[!] Erro ao tentar instalar {package}. Verifique se há problemas de rede ou permissões.")

# Executa a verificação e instalação
check_and_install()

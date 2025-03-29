import os
import subprocess

def otimizar():
    print("Iniciando otimização do sistema...")
    
    # Limpeza de arquivos temporários
    os.system('del /s /q %temp%\\*.*')
    os.system('del /s /q C:\\Windows\\Temp\\*.*')

    # Esvaziar a lixeira
    subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'])
    
    print("Otimização concluída!")

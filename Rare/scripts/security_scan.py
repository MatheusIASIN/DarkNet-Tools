import subprocess

def verificar_segurança():
    print("Iniciando verificação de segurança...")
    
    # Verificação de arquivos corrompidos
    comando_sfc = ['sfc', '/scannow']
    subprocess.run(comando_sfc)
    
    print("Verificação de segurança concluída!")

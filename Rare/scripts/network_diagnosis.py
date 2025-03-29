import subprocess

def diagnostico_rede():
    print("Iniciando diagnóstico de rede...")

    # Teste de ping para o Google
    comando_ping = ['ping', '8.8.8.8']
    try:
        resultado_ping = subprocess.run(comando_ping, capture_output=True, text=True, check=True)
        print("Ping bem-sucedido!")
        print(resultado_ping.stdout)
    except subprocess.CalledProcessError:
        print("Erro ao executar o comando ping. Verifique sua conexão de rede.")

    # Teste de traceroute
    comando_tracert = ['tracert', '8.8.8.8']
    try:
        resultado_tracert = subprocess.run(comando_tracert, capture_output=True, text=True, check=True)
        print("\nTraceroute bem-sucedido!")
        print(resultado_tracert.stdout)
    except subprocess.CalledProcessError:
        print("Erro ao executar o comando tracert. Verifique sua conexão de rede.")

    print("Diagnóstico concluído!")


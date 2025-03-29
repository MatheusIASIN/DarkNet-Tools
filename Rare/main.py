import subprocess
import tkinter as tk
from tkinter import PhotoImage, messagebox, scrolledtext
import os

# Diretório base dos ícones
ASSETS_DIR = r"C:\Users\Matheus\Desktop\Rare\assets"

# Diretório base dos scripts
SCRIPTS_DIR = r"C:\Users\Matheus\Desktop\Rare\scripts"

# Função para executar os scripts Python (.py) e mostrar saída no log
def executar_py(caminho_arquivo_py, log_text):
    """Executa um arquivo Python (.py) e captura a saída"""
    try:
        log_text.insert(tk.END, f"Executando: {caminho_arquivo_py}\n")
        log_text.see(tk.END)  # Rola automaticamente para o final
        
        # Executa o comando e captura a saída e erros
        resultado = subprocess.run(["python", caminho_arquivo_py], capture_output=True, text=True, check=True)
        log_text.insert(tk.END, f"Saída:\n{resultado.stdout}\n")  # Mostra a saída no log
        log_text.insert(tk.END, f"Erros:\n{resultado.stderr}\n")  # Mostra os erros no log (se houver)

        messagebox.showinfo("Sucesso", f'{caminho_arquivo_py} executado com sucesso!')
    except subprocess.CalledProcessError as e:
        log_text.insert(tk.END, f"Erro ao executar {caminho_arquivo_py}:\n{e}\n")
        messagebox.showerror("Erro", f'Erro ao executar {caminho_arquivo_py}:\n{e}')
    except FileNotFoundError:
        messagebox.showerror("Erro", f'O arquivo {caminho_arquivo_py} não foi encontrado.')
        log_text.insert(tk.END, f"Arquivo não encontrado: {caminho_arquivo_py}\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
        log_text.insert(tk.END, f"Erro inesperado: {e}\n")

# Função para carregar ícones redimensionados
def carregar_icone(nome_arquivo_icone):
    """Carrega o ícone na pasta de assets"""
    caminho_icone = os.path.join(ASSETS_DIR, nome_arquivo_icone)
    if os.path.exists(caminho_icone):
        return PhotoImage(file=caminho_icone).subsample(4, 4)  # Redimensiona o ícone
    else:
        messagebox.showerror("Erro", f"Ícone não encontrado: {caminho_icone}")
        return None

# Funções para os scripts
def otimizador_pc(log_text):
    caminho = os.path.join(SCRIPTS_DIR, "optimize.py")
    executar_py(caminho, log_text)

def diagnostico_rede(log_text):
    caminho = os.path.join(SCRIPTS_DIR, "network_diagnosis.py")
    executar_py(caminho, log_text)

def verificacao_disco(log_text):
    caminho = os.path.join(SCRIPTS_DIR, "disk_check.py")
    executar_py(caminho, log_text)

def verificacao_defender(log_text):
    caminho = os.path.join(SCRIPTS_DIR, "security_scan.py")
    executar_py(caminho, log_text)

# Função para criar a interface gráfica
def criar_interface():
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("TemPad - Gerenciador de Scripts de Manutenção")
    janela.geometry("600x600")
    janela.configure(bg='#1c1c1c')  # Cor de fundo escura para dar um toque futurista
    
    # Título da janela
    titulo = tk.Label(janela, text="Escolha uma opção de manutenção:", font=("Arial", 16), fg="#00ff00", bg="#1c1c1c")
    titulo.pack(pady=20)
    
    # Área de log
    log_text = scrolledtext.ScrolledText(janela, width=70, height=15, bg="#000000", fg="#00ff00", font=("Arial", 10))
    log_text.pack(pady=10)
    log_text.insert(tk.END, "Log de execução iniciado...\n")

    # Carregar ícones
    disk_icon = carregar_icone("hard-disk.gif")
    otim_icon = carregar_icone("optimization.gif")
    network_icon = carregar_icone("network.gif")
    safe_icon = carregar_icone("safe.gif")

    # Criar botões com ícones ao lado
    def criar_botao(frame, texto, comando, icone):
        container = tk.Frame(frame, bg="#1c1c1c")  # Frame para alinhar ícone e botão
        container.pack(pady=10, fill="x")

        if icone:
            tk.Label(container, image=icone, bg="#1c1c1c").pack(side="left", padx=10)
        tk.Button(container, text=texto, command=comando, width=30, height=2, 
                  fg="#1c1c1c", bg="#00ff00", font=("Arial", 12), relief="raised", bd=3).pack(side="left", padx=10)

    criar_botao(janela, "Verificação de Disco", lambda: verificacao_disco(log_text), disk_icon)
    criar_botao(janela, "Otimização de PC", lambda: otimizador_pc(log_text), otim_icon)
    criar_botao(janela, "Diagnóstico de Rede", lambda: diagnostico_rede(log_text), network_icon)
    criar_botao(janela, "Verificação do Microsoft Defender", lambda: verificacao_defender(log_text), safe_icon)
    
    # Botão para fechar o programa
    tk.Button(janela, text="Sair", width=30, height=2, command=janela.quit, 
              fg="#1c1c1c", bg="#ff0000", font=("Arial", 12), relief="raised", bd=3).pack(pady=20)
    
    # Exibe a interface
    janela.mainloop()

# Executa a interface gráfica
if __name__ == '__main__':
    criar_interface()

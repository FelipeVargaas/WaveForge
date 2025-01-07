import json
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from tkinter import filedialog, messagebox

def load_config():
    try:
        # Abrir uma janela de diálogo para escolher o arquivo JSON
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de configuração",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not filepath:
            return  # Caso o usuário cancele a seleção

        # Abrir e carregar o conteúdo do arquivo JSON
        with open(filepath, 'r') as file:
            config = json.load(file)

        # Atualizar o valor do Meter
        if "valor" in config:
            value = config["valor"]
            max_value = 100  # Valor máximo para o Meter

            if 0 <= value <= max_value:
                meter.amountusedvar.set(value)  # Atualiza o valor interno
                meter.configure(amountused=value)  # Atualiza visualmente o Meter
            else:
                messagebox.showwarning(
                    "Valor inválido", 
                    f"O valor deve estar entre 0 e {max_value}."
                )

        # Atualizar o texto da label do Meter
        if "label" in config:
            label_text = config["label"]
            meter.configure(subtext=label_text)  # Atualiza o texto da label
        else:
            messagebox.showinfo("Aviso", "A chave 'label' não foi encontrada no arquivo JSON.")
    except json.JSONDecodeError:
        messagebox.showerror("Erro no arquivo", "O arquivo selecionado não é um JSON válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo: {e}")

# Criar a aplicação principal
app = ttk.Window(themename="superhero")
app.title("Teste do Meter com JSON")
app.geometry("400x300")

# Criar o Meter
meter = Meter(
    app,
    subtext="Exemplo",
    amounttotal=100,
    amountused=0,
    metersize=200,
    metertype="semi",
    bootstyle="success",
    interactive=True
)
meter.pack(pady=20)

# Criar o botão de carregar configurações
load_button = ttk.Button(
    app, 
    text="Carregar Configurações", 
    bootstyle="primary", 
    command=load_config
)
load_button.pack(pady=10)

# Iniciar o loop principal da aplicação
app.mainloop()

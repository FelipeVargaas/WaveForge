import json
from tkinter import filedialog, messagebox

# Função para carregar configurações do JSON e atualizar os valores dos meters
def load_config(meters, labels):
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

        # Atualizar os valores dos meters com base nas chaves do JSON
        for label, meter in zip(labels, meters):
            if label in config:
                value = config[label]
                meter.amountusedvar.set(value)  # Atualiza o valor interno
                meter.configure(amountused=value)  # Atualiza visualmente o Meter
    except json.JSONDecodeError:
        messagebox.showerror("Erro no arquivo", "O arquivo selecionado não é um JSON válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo: {e}")

        # Função para salvar os valores dos meters em um arquivo JSON
def save_config(meters, labels):
    try:
        # Abrir caixa de diálogo para salvar arquivo
        filepath = filedialog.asksaveasfilename(
            title="Salvar arquivo de configuração",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not filepath:
            return  # Caso o usuário cancele o salvamento

        # Criar um dicionário com os valores dos meters
        config = {label: meter.amountusedvar.get() for label, meter in zip(labels, meters)}

        # Salvar os dados no arquivo JSON
        with open(filepath, 'w') as file:
            json.dump(config, file, indent=4)

        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo: {e}")


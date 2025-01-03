import json
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter.filedialog import asksaveasfilename  # Para selecionar o caminho e nome do arquivo

def abrir_janela_configuracao(parent):
    def salvar_arquivo():
        """Abre uma janela para salvar as configurações em um arquivo JSON."""
        # Coletar valores dos campos
        configuracoes = {
            "Meter1": {
                "command": command_entry.get(),
                "label": label_entry.get(),
                "maxval": maxval_entry.get(),
                "unit": unit_entry.get(),
            }
        }

        # Abrir diálogo para salvar arquivo
        file_path = asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Salvar Configurações"
        )

        if file_path:  # Se o usuário escolheu um arquivo
            try:
                with open(file_path, "w") as json_file:
                    json.dump(configuracoes, json_file, indent=4)
                Messagebox.show_info("Sucesso", f"Configurações salvas com sucesso em {file_path}!")
            except Exception as e:
                Messagebox.show_error("Erro", f"Erro ao salvar o arquivo: {e}")

    # Criar janela de configuração
    config_window = ttk.Toplevel(parent)
    config_window.title("Editar Configurações")
    config_window.geometry("400x300")

    # Label principal
    ttk.Label(config_window, text="Meter1 Configurações", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Campo para Command
    ttk.Label(config_window, text="Command:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    command_entry = ttk.Entry(config_window, width=30)
    command_entry.grid(row=1, column=1, padx=10, pady=5)

    # Campo para Label
    ttk.Label(config_window, text="Label:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    label_entry = ttk.Entry(config_window, width=30)
    label_entry.grid(row=2, column=1, padx=10, pady=5)

    # Campo para MaxVal
    ttk.Label(config_window, text="MaxVal:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    maxval_entry = ttk.Entry(config_window, width=30)
    maxval_entry.grid(row=3, column=1, padx=10, pady=5)

    # Campo para Unit
    ttk.Label(config_window, text="Unit:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    unit_entry = ttk.Entry(config_window, width=30)
    unit_entry.grid(row=4, column=1, padx=10, pady=5)

    # Botão para salvar as configurações
    salvar_button = ttk.Button(config_window, text="Salvar", command=salvar_arquivo, bootstyle="success")
    salvar_button.grid(row=5, column=0, columnspan=2, pady=20)

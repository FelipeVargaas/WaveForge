import json
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter.filedialog import asksaveasfilename  # Para selecionar o caminho e nome do arquivo


def abrir_janela_configuracao(parent):
    def salvar_arquivo():
        """Abre uma janela para salvar as configurações em um arquivo JSON."""
        configuracoes = {}

        # Coletar valores dos campos
        for i, entries in enumerate(entry_fields):
            configuracoes[f"Meter{i+1}"] = {
                "command": entries["command"].get(),
                "label": entries["label"].get(),
                "maxval": entries["maxval"].get(),
                "unit": entries["unit"].get(),
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
    config_window.geometry("700x400")

    # Cabeçalhos
    headers = ["Meter", "Command", "Label", "MaxVal", "Unit"]
    for col, header in enumerate(headers):
        ttk.Label(config_window, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

    # Criar campos para 12 configurações
    entry_fields = []
    for i in range(12):
        # Meter Label
        ttk.Label(config_window, text=f"Meter{i+1}").grid(row=i + 1, column=0, padx=5, pady=5)

        # Campos de entrada
        command_entry = ttk.Entry(config_window, width=15)
        command_entry.grid(row=i + 1, column=1, padx=5, pady=5)

        label_entry = ttk.Entry(config_window, width=15)
        label_entry.grid(row=i + 1, column=2, padx=5, pady=5)

        maxval_entry = ttk.Entry(config_window, width=10)
        maxval_entry.grid(row=i + 1, column=3, padx=5, pady=5)

        unit_entry = ttk.Entry(config_window, width=10)
        unit_entry.grid(row=i + 1, column=4, padx=5, pady=5)

        # Adicionar entradas ao array
        entry_fields.append({
            "command": command_entry,
            "label": label_entry,
            "maxval": maxval_entry,
            "unit": unit_entry,
        })

    # Botão para salvar as configurações
    salvar_button = ttk.Button(config_window, text="Salvar", command=salvar_arquivo, bootstyle="success")
    salvar_button.grid(row=13, column=0, columnspan=5, pady=20)

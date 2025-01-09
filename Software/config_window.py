import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog, messagebox
import json

def abrir_janela_configuracao(parent, meters, labels, commands, max_vals, unit):
    # Criar janela de configuração
    config_window = ttk.Toplevel(parent)
    config_window.title("Editar Configurações")
    config_window.geometry("600x600")

    # Cabeçalhos
    headers = ["Meter", "Command", "Label", "MaxVal", "Unit"]
    for col, header in enumerate(headers):
        ttk.Label(config_window, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

    # Criar campos para 12 configurações
    entry_fields = []
    for i in range(12):
        # Meter Label
        ttk.Label(config_window, text=f"Meter {i + 1}").grid(row=i + 1, column=0, padx=5, pady=5)

        # Campos de entrada pré-preenchidos
        command_entry = ttk.Entry(config_window, width=15)
        command_entry.insert(0, commands[i])  # Preencher com o comando atual
        command_entry.grid(row=i + 1, column=1, padx=5, pady=5)

        label_entry = ttk.Entry(config_window, width=15)
        label_entry.insert(0, labels[i])  # Preencher com o label atual
        label_entry.grid(row=i + 1, column=2, padx=5, pady=5)

        maxval_entry = ttk.Entry(config_window, width=10)
        maxval_entry.insert(0, max_vals[i])  # Preencher com o maxval atual
        maxval_entry.grid(row=i + 1, column=3, padx=5, pady=5)

        unit_entry = ttk.Entry(config_window, width=10)
        unit_entry.insert(0, unit[i])  # Preencher com a unidade atual
        unit_entry.grid(row=i + 1, column=4, padx=5, pady=5)

        # Adicionar entradas ao array
        entry_fields.append({
            "command": command_entry,
            "label": label_entry,
            "maxVal": maxval_entry,
            "unit": unit_entry,
        })  


    # Função para salvar alterações
    def salvar_alteracoes():       
        configuracoes = {} 
        try:
            # for i, fields in enumerate(entry_fields):
            #     # Atualizar valores nos arrays
            #     commands[i] = fields["command"].get()
            #     labels[i] = fields["label"].get()
            #     max_vals[i] = int(fields["maxVal"].get())
            #     unit[i] = fields["unit"].get()
            configuracoes = {"meters": []}  # Inicia o dicionário com uma lista vazia

            for entry in entry_fields:
                configuracoes["meters"].append({
                    "command": entry["command"].get(),
                    "label": entry["label"].get(),
                    "maxVal": int(entry["maxVal"].get()),  # Converte para int, se necessário
                    "unit": entry["unit"].get(),
                })
                # Atualizar os meters correspondentes
                # meters[i].configure(subtext=labels[i])
                # meters[i].configure(amounttotal=max_vals[i])
                # meters[i].configure(textright=unit[i])
                # Messagebox.show_info("Sucesso", "Configurações atualizadas com sucesso!")
            
            # Abrir diálogo para salvar arquivo
            
            file_path = filedialog.asksaveasfilename(
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
            
            config_window.destroy()
        except ValueError:
            Messagebox.show_error("Erro", "Certifique-se de que os valores de MaxVal são números inteiros.")

    # Botão para salvar as alterações
    save_button = ttk.Button(
        config_window,
        text="Salvar Configurações",
        bootstyle="success",
        command=salvar_alteracoes
    )
    save_button.grid(row=13, column=0, columnspan=5, pady=20)

    # Botão para cancelar
    cancel_button = ttk.Button(
        config_window,
        text="Cancelar",
        bootstyle="danger",
        command=config_window.destroy
    )
    cancel_button.grid(row=14, column=0, columnspan=5, pady=10)


    # def save_config(meters, labels):
    #     try:
    #         # Abrir caixa de diálogo para salvar arquivo
    #         filepath = "meters_config.json"

    #         # Criar um dicionário com os valores dos meters
    #         config = {label: meter.amountusedvar.get() for label, meter in zip(labels, meters)}

    #         # Salvar os dados no arquivo JSON
    #         with open(filepath, 'w') as file:
    #             json.dump(config, file, indent=4)

    #         messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
    #     except Exception as e:
    #         messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo: {e}")


    # Botão para salvar as configurações
    # salvar_button = ttk.Button(config_window, text="Salvar", command=save_config, bootstyle="success")
    # salvar_button.grid(row=15, column=0, columnspan=5, pady=20)



# def salvar_arquivo():
#         """Abre uma janela para salvar as configurações em um arquivo JSON."""
#         configuracoes = {}

#         # Coletar valores dos campos
#         for i, entries in enumerate(entry_fields):
#             configuracoes[f"Meter{i+1}"] = {
#                 "command": entries["command"].get(),
#                 "label": entries["label"].get(),
#                 "maxval": entries["maxval"].get(),
#                 "unit": entries["unit"].get(),
#             }

#         # Abrir diálogo para salvar arquivo
#         file_path = asksaveasfilename(
#             defaultextension=".json",
#             filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
#             title="Salvar Configurações"
#         )

#         if file_path:  # Se o usuário escolheu um arquivo
#             try:
#                 with open(file_path, "w") as json_file:
#                     json.dump(configuracoes, json_file, indent=4)
#                 Messagebox.show_info("Sucesso", f"Configurações salvas com sucesso em {file_path}!")
#             except Exception as e:
#                 Messagebox.show_error("Erro", f"Erro ao salvar o arquivo: {e}")
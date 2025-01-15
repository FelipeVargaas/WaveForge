import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog, messagebox
import json

def abrir_janela_configuracao(parent, meters, labels, commands, max_vals, unit):
    # Criar janela de configuração
    config_window = ttk.Toplevel(parent)
    config_window.title("Editar Medidores")
    config_window.geometry("600x650")

 

    # Configurar as colunas para distribuição uniforme
    config_window.grid_columnconfigure(0, weight=1)
    config_window.grid_columnconfigure(1, weight=1)
    config_window.grid_columnconfigure(2, weight=1)
    config_window.grid_columnconfigure(3, weight=1)
    config_window.grid_columnconfigure(4, weight=1)

    # Título
    titulo_config = ttk.Label(
        config_window, text="Editar Medidores", font=("Helvetica", 22)
    )
    titulo_config.grid(row=0, column=0, columnspan=5, pady=20)

    # Cabeçalhos
    headers = ["Meter", "Command", "Label", "MaxVal", "Unit"]
    for col, header in enumerate(headers):
        ttk.Label(config_window, text=header, font=("Helvetica", 10, "bold")).grid(row=1, column=col, padx=5, pady=5)

    # Criar campos para 12 configurações
    entry_fields = []
    for i in range(12):
        # Meter Label
        ttk.Label(config_window, text=f"Meter {i + 1}").grid(row=i + 2, column=0, padx=5, pady=5)

        # Campos de entrada pré-preenchidos
        command_entry = ttk.Entry(config_window, width=15)
        command_entry.insert(0, commands[i])  # Preencher com o comando atual
        command_entry.grid(row=i + 2, column=1, padx=5, pady=5)

        label_entry = ttk.Entry(config_window, width=15)
        label_entry.insert(0, labels[i])  # Preencher com o label atual
        label_entry.grid(row=i + 2, column=2, padx=5, pady=5)

        maxval_entry = ttk.Entry(config_window, width=10)
        maxval_entry.insert(0, max_vals[i])  # Preencher com o maxval atual
        maxval_entry.grid(row=i + 2, column=3, padx=5, pady=5)

        unit_entry = ttk.Entry(config_window, width=10)
        unit_entry.insert(0, unit[i])  # Preencher com a unidade atual
        unit_entry.grid(row=i + 2, column=4, padx=5, pady=5)

        # Adicionar entradas ao array
        entry_fields.append({
            "command": command_entry,
            "label": label_entry,
            "maxVal": maxval_entry,
            "unit": unit_entry,
        })  

    def carregar_configuracoes():
        try:
            # Abrir caixa de diálogo para carregar o arquivo de configurações
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
                title="Carregar Configurações"
            )

            if file_path:  # Se o usuário escolheu um arquivo
                # Carregar o conteúdo do arquivo JSON
                with open(file_path, "r") as json_file:
                    configuracoes = json.load(json_file)
                
                # Atualizar os meters com as configurações carregadas
                aplicar_configuracoes(meters, labels, configuracoes)

                # Mostrar mensagem de sucesso
                Messagebox.show_info("Sucesso", f"Configurações carregadas com sucesso de {file_path}!")
            else:
                print("Nenhum arquivo selecionado.")

        except Exception as e:
            Messagebox.show_error("Erro", f"Erro ao carregar o arquivo: {e}")
            print("Erro ao carregar o arquivo:", e)

    def aplicar_configuracoes(meters, labels, config):
        try:
            for i, meter_config in enumerate(config["meters"]):
                meters[i].configure(amounttotal=meter_config["maxVal"])  # Atualiza o valor máximo
                meters[i].configure(subtext=meter_config["label"])  # Atualiza o texto do subtext
                meters[i].configure(textright=meter_config["unit"])  # Atualiza a unidade
                labels[i] = meter_config["label"]  # Atualiza a lista de labels
        except AttributeError as e:
            print(f"Erro ao aplicar configurações: {e}")
            raise
    def salvar_alteracoes():
        configuracoes = {}
        try:
            configuracoes = {"meters": []}  # Inicia o dicionário com uma lista vazia

            for entry in entry_fields:
                configuracoes["meters"].append({
                    "command": entry["command"].get(),
                    "label": entry["label"].get(),
                    "maxVal": int(entry["maxVal"].get()),  # Converte para int, se necessário
                    "unit": entry["unit"].get(),
                })
            
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
                    
                    # Atualizar os meters após salvar
                    aplicar_configuracoes(meters, labels, configuracoes)
                except Exception as e:
                    Messagebox.show_error("Erro", f"Erro ao salvar o arquivo: {e}")
                    print("Erro", f"Erro ao salvar o arquivo: {e}")
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
    save_button.grid(row=14, column=1, padx=10, pady=20, sticky="ew")  # Coluna 1

    # Botão para carregar configurações
    load_button = ttk.Button(
        config_window,
        text="Carregar Configurações",
        bootstyle="info",
        command=carregar_configuracoes
    )
    load_button.grid(row=14, column=2, padx=10, pady=20, sticky="ew")  # Coluna 2

    # Botão para cancelar
    cancel_button = ttk.Button(
        config_window,
        text="Cancelar",
        bootstyle="danger",
        command=config_window.destroy
    )
    cancel_button.grid(row=14, column=3, padx=10, pady=20, sticky="ew")  # Coluna 3



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
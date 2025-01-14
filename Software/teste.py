import time
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
import serial
import serial.tools.list_ports  # Biblioteca para comunicação Bluetooth e listagem de portas
from config_window import abrir_janela_configuracao
from save_and_load import load_config, save_config
from tkinter import filedialog, messagebox
import json
import os

def sendAll():
    # if not bluetooth:  # Verifica se está conectado antes de enviar os comandos
    #     status_label.configure(text="Nenhuma conexão ativa!", bootstyle="danger")
    #     return

    original_text = status_label.cget("text")  # Salva o texto original
    status_label.configure(text="Enviando comandos...")
    progress_bar = ttk.Progressbar(menu_frame, mode="determinate", bootstyle="success", maximum=len(meters))
    progress_bar.pack(side="left", padx=10)

    for i in range(len(meters)):
        send_command(round(meters[i].amountusedvar.get()), config["meters"][i]["command"])
        progress_bar["value"] = i + 1
        app.update_idletasks()  # Atualiza a interface durante o loop
        time.sleep(0.1)  # Simula o tempo de envio

    progress_bar.destroy()  # Remove a barra de progresso
    status_label.configure(text=original_text)  # Restaura o texto original

# Função para listar portas COM disponíveis
bluetooth = None
def listar_portas():
    portas = serial.tools.list_ports.comports()
    return [porta.device for porta in portas]

# Função para conectar à porta serial escolhida
def conectar_serial():
    porta = porta_var.get()
    baudrate = baudrate_var.get()
    
    if porta and baudrate:
        try:
            global bluetooth
            bluetooth = serial.Serial(porta, baudrate, timeout=1)
            status_label.configure(text=f"Conectado à {porta} com baudrate {baudrate}")
        except serial.SerialException as e:
            status_label.configure(text=f"Erro ao conectar")
            #status_label.configure(text=f"Erro ao conectar: {e}")
    else:
        status_label.configure(text="Selecione uma porta e baudrate válidos!")

# Janela principal
app = ttk.Window(themename="darkly")  # Define o tema da interface
app.title("Wave Forge")
app.geometry("750x700")  # Aumenta o tamanho da janela para acomodar 12 meters

# Frame para barra de menu, botão conectar e label de status
menu_frame = ttk.Frame(app)
menu_frame.pack(fill="x", pady=0, padx=0)

# Barra de Menu
barra_menu = ttk.Menubutton(menu_frame, text="Conexão", bootstyle="primary")
barra_menu.pack(side="left", padx=0, pady=0)

# Submenu para escolher porta COM e baudrate
menu_conexao = ttk.Menu(barra_menu, tearoff=False)
barra_menu["menu"] = menu_conexao

# Variáveis para armazenar a porta COM e baudrate
porta_var = ttk.StringVar()
baudrate_var = ttk.IntVar(value=9600)

# Adicionando opções de porta COM
portas_disponiveis = listar_portas()
for porta in portas_disponiveis:
    menu_conexao.add_radiobutton(label=porta, variable=porta_var, value=porta)

# Adicionando opções de baudrate
menu_conexao.add_separator()
baudrates = [9600, 19200, 38400, 57600, 115200]
for baud in baudrates:
    menu_conexao.add_radiobutton(label=f"{baud} Baud", variable=baudrate_var, value=baud)

# Botão para conectar
conectar_button = ttk.Button(menu_frame, text="Conectar", bootstyle="success", command=conectar_serial)
conectar_button.pack(side="left", padx=0)

# Label de status
status_label = ttk.Label(menu_frame, text="Selecione a porta e o baudrate.", bootstyle="info")
status_label.pack(side="left", padx=10)

# Barra de configurações
menu_config = ttk.Menubutton(menu_frame, text="Configurações", bootstyle="primary")
menu_config.pack(side="right", padx=0, pady=0)

# Botão para conectar
send_all = ttk.Button(menu_frame, text="Send All", bootstyle="danger", command=sendAll)
send_all.pack(side="right", padx=2)

# Título principal
titulo_principal = ttk.Label(text="Wave Forge", font=("Helvetica", 32))
titulo_principal.pack(pady=5)

main_frame = ttk.Frame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Caminho do arquivo de configuração
CONFIG_FILE = "default_settings.json"

# Função para carregar ou criar configuração padrão
def load_or_create_config():
    default_config = {
        "meters": [
            {"command": "SET_RPM", "label": "RPM", "maxVal": 5000, "unit": ""},
            {"command": "SET_PEDAL", "label": "Pedal", "maxVal": 1000, "unit": ""},
            {"command": "SET_TEMP", "label": "Manometro", "maxVal": 250, "unit": "bar"},
            {"command": "SET_PRESSURE", "label": "T.Red", "maxVal": 100, "unit": "°C"},
            {"command": "SET_FUEL", "label": "Injetor A", "maxVal": 25, "unit": "ms"},
            {"command": "SET_AIRFLOW", "label": "Injetor B", "maxVal": 25, "unit": "ms"},
            {"command": "SET_OIL_TEMP", "label": "Injetor C", "maxVal": 25, "unit": "ms"},
            {"command": "SET_COOLANT_TEMP", "label": "Injetor D", "maxVal": 25, "unit": "ms"},
            {"command": "SET_VOLTAGE", "label": "MAP", "maxVal": 100, "unit": "bar"},
            {"command": "SET_SPEED", "label": "T.GNV", "maxVal": 100, "unit": "°C"},
            {"command": "SET_INJECTOR_A", "label": "P.GNV", "maxVal": 100, "unit": "bar"},
            {"command": "SET_INJECTOR_B", "label": "HPS", "maxVal": 100, "unit": "bar"}
        ]
    }
    # Verifica se o arquivo existe
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as file:
            json.dump(default_config, file, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
        
# Função para criar o meter e botão
def create_meter_and_button(parent, row, col, label_text, min_value, max_value, unit, initial_value, meter_label, command):
    # Criar um frame específico para o meter e botão
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=col, padx=10, pady=10)  # Usando grid no frame interno

    # Criar o meter
    meter = Meter(
        frame,
        subtext=meter_label,
        amounttotal=max_value,
        amountused=initial_value,
        metersize=140,
        metertype="semi",
        bootstyle="success",
        stepsize=(int(max_value) / 100),
        stripethickness=2,
        textright=unit,
        interactive=True
    )
    meter.grid(row=0, column=0, padx=10)  # Usar grid dentro do frame

    # Botão de envio
    send_button = ttk.Button(
        frame,
        text="Send",
        bootstyle="success",
        command=lambda: send_command(round(meter.amountusedvar.get()), command)
    )
    send_button.grid(row=1, column=0, padx=10, sticky="ew")  # Usar grid no botão também

    return meter

# Carregar a configuração
config = load_or_create_config()

# Extrair dados do config para listas individuais
labels = [meter["label"] for meter in config["meters"]]
commands = [meter["command"] for meter in config["meters"]]
maxVal = [meter["maxVal"] for meter in config["meters"]]
unit = [meter["unit"] for meter in config["meters"]]

# Criar múltiplos meters e botões
meters = []
for i in range(12):
    row = i // 4  # Define a linha
    col = i % 4  # Define a coluna
    meter = create_meter_and_button(
        main_frame, row, col,
        labels[i], 0, maxVal[i], unit[i], 0, labels[i], commands[i]
    )
    meters.append(meter)

# Submenu de configuracoes
menu_conexao = ttk.Menu(menu_config, tearoff=False)
menu_config["menu"] = menu_conexao

menu_conexao.add_command(label="Load config", command=lambda: load_config(meters, labels))
menu_conexao.add_command(label="Save config", command=lambda: save_config(meters,labels,commands,maxVal,unit))
#menu_conexao.add_command(label="Save config", command=lambda: save_config(meters, labels))
menu_conexao.add_separator()
menu_conexao.add_command(
    label="TITAN",
    command=lambda: load_config(meters, labels, file_path="C:\gitProjects\WaveForge\Software\igt_default\\titan.json")    
)
menu_conexao.add_command(label="Zeus", command=lambda: load_config(meters, labels))
menu_conexao.add_command(label="Kronos", command=lambda: load_config(meters, labels))
menu_conexao.add_separator()
menu_conexao.add_command(
    label="Editar Medidores",
    command=lambda: abrir_janela_configuracao(app, meters, labels, commands, maxVal, unit)
)



# Função para enviar o comando e valor via Bluetooth
def send_command(meter_value, command):
    if bluetooth:
        value = int(meter_value)  # Garante que o valor seja um número inteiro
        command_message = f"{command}:{value}\n"  # Comando e valor para enviar
        bluetooth.write(command_message.encode())
        print(f"Comando enviado: {command_message}")
    else:
        print("Bluetooth não está conectado.")

# Inicia a aplicação
app.mainloop()
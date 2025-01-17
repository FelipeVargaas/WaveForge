import time
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
import serial
import serial.tools.list_ports  # Biblioteca para comunicação Bluetooth e listagem de portas
from config_window import abrir_janela_configuracao
from save_and_load import load_config, save_config
from tkinter import Canvas, PhotoImage, filedialog, messagebox
import json
import os
from PIL import Image, ImageTk  # Importando Pillow
from serial_terminal import SerialTerminal

def sendAll():
    if not bluetooth:  # Verifica se está conectado antes de enviar os comandos
        status_label.configure(text="Nenhuma conexão ativa!", bootstyle="danger")
        return

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

# Variável de estado para rastrear conexão
conectado = False

# Função para alternar entre conectar e desconectar
def alternar_conexao():
    global conectado, bluetooth

    if not conectado:
        # Tentativa de conectar
        porta = porta_var.get()
        baudrate = baudrate_var.get()

        if porta and baudrate:
            try:
                bluetooth = serial.Serial(porta, baudrate, timeout=1)
                status_label.configure(text=f"Conectado à {porta} com baudrate {baudrate}", bootstyle="success")
                conectar_button.configure(text="Desconectar", bootstyle="danger")
                conectado = True
            except serial.SerialException:
                status_label.configure(text="Erro ao conectar!")
        else:
            status_label.configure(text="Selecione uma porta e baudrate válidos!")
    else:
        # Desconectar
        if bluetooth.is_open:
            bluetooth.close()
        status_label.configure(text="Desconectado",bootstyle="danger")
        conectar_button.configure(text="Conectar", bootstyle="success")
        conectado = False

# Janela principal
app = ttk.Window(themename="darkly")  # Define o tema da interface
app.title("IGT - Wave Forge")
app.geometry("750x700")  # Aumenta o tamanho da janela para acomodar 12 meters

# Carregar o ícone usando Pillow (no formato .ico)
icone = Image.open("icone_atalho.ico")
icone_tk = ImageTk.PhotoImage(icone)

# Definir o ícone da janela
app.iconphoto(True, icone_tk)

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

# Botão para conectar/desconectar
conectar_button = ttk.Button(
    menu_frame, text="Conectar", bootstyle="success", command=alternar_conexao
)
conectar_button.pack(side="left", padx=0)

# Label de status
status_label = ttk.Label(menu_frame, text="Selecione a porta e o baudrate.", bootstyle="info")
status_label.pack(side="left", padx=10)

# Barra de configurações
menu_config = ttk.Menubutton(menu_frame, text="Configurações", bootstyle="primary")
menu_config.pack(side="right", padx=0, pady=0)

# para enviar todas as configurações
send_all = ttk.Button(menu_frame, text="Send All", bootstyle="danger", command=sendAll)
send_all.pack(side="right", padx=2)

def open_terminal():
    # """
    # Abre a janela do terminal utilizando a conexão serial já existente.
    # """
    terminal = SerialTerminal(bluetooth)
    terminal.run()

# Frame para o título e o logo
titulo_frame = ttk.Frame(app)
titulo_frame.pack(fill="x", pady=10)

# Adicionar o logo no canto esquerdo
logo_imagem = PhotoImage(file="C:/gitProjects/WaveForge/Software/logo_menor.png")
logo_label = ttk.Label(titulo_frame, image=logo_imagem)
logo_label.grid(row=0, column=0, sticky="w", padx=10)

# Adicionar o título centralizado
titulo_principal = ttk.Label(titulo_frame, text="Wave Forge", font=("Helvetica", 32))
titulo_principal.grid(row=0, column=1, sticky="n", padx=0)

# Configurar as colunas para alinhamento
titulo_frame.grid_columnconfigure(0, weight=1)  # Coluna do logo
titulo_frame.grid_columnconfigure(1, weight=3)  # Coluna do título
titulo_frame.grid_columnconfigure(2, weight=6)  # Coluna vazia para equilibrar
titulo_frame.grid_columnconfigure(3, weight=2)  # Coluna vazia para equilibrar

# Main frame
main_frame = ttk.Frame(app)
main_frame.pack(fill="x", expand=True, padx=20, pady=10)

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

menu_conexao.add_command(label="Carregar Valores", command=lambda: load_config(meters, labels))
menu_conexao.add_command(label="Salvar Valores", command=lambda: save_config(meters,labels))
menu_conexao.add_separator()
    # Botão para abrir o terminal
# open_terminal_button = ttk.Button(app, text="Abrir Terminal Serial", command=open_terminal)
# open_terminal_button.pack(pady=20)
menu_conexao.add_command(label="Terminal Serial", command=open_terminal)
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
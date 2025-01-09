import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
import serial
import serial.tools.list_ports  # Biblioteca para comunicação Bluetooth e listagem de portas
from config_window import abrir_janela_configuracao
from save_and_load import load_config, save_config
from tkinter import filedialog, messagebox
import json


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
app.geometry("800x700")  # Aumenta o tamanho da janela para acomodar 12 meters

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

# Submenu de configuracoes
menu_conexao = ttk.Menu(menu_config, tearoff=False)
menu_config["menu"] = menu_conexao
menu_conexao.add_command(label= "Load config", command=lambda: load_config(meters, labels))
menu_conexao.add_command(label= "Save config", command=lambda: save_config(meters, labels))
menu_conexao.add_separator()
menu_conexao.add_command(label= "Editar Medidores", command=lambda: abrir_janela_configuracao(app, meters, labels, commands, maxVal, unit))

# Título principal
titulo_principal = ttk.Label(text="Wave Forge", font=("Helvetica", 32))
titulo_principal.pack(pady=5)

# Função para enviar o comando e valor via Bluetooth
def send_command(meter_value, command):
    if bluetooth:
        value = int(meter_value)  # Garante que o valor seja um número inteiro
        command_message = f"{command}:{value}\n"  # Comando e valor para enviar
        bluetooth.write(command_message.encode())
        print(f"Comando enviado: {command_message}")
    else:
        print("Bluetooth não está conectado.")


# Função para criar Meter, Botão de envio e garantir que o valor seja inteiro
def create_meter_and_button(parent, row, col, label_text, min_value, max_value, unit, initial_value, meter_label, command):
    # Frame para o meter, botão e o label
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=col, pady=10, padx=10, sticky="ew")

    # Meter
    meter = Meter(
        frame,
        subtext=meter_label,
        amounttotal=max_value,
        amountused=initial_value,
        metersize=140,
        metertype="semi",  # Tipo de medidor (semi, full, quarter, donut)
        bootstyle="success",  # Define o estilo de cor
        stepsize=(int(max_value)/100),
        stripethickness=2,
        textright=unit,
        interactive=True
    )
    meter.grid(row=0, column=0, padx=10, sticky="ew")

    # Botão Send
    send_button = ttk.Button(frame, text="Send", bootstyle="success", 
                             command=lambda: send_command(round(meter.amountusedvar.get()), command))  # Arredonda o valor para inteiro
    send_button.grid(row=1, column=0, padx=10, sticky="ew")

    return meter

# Frame principal
main_frame = ttk.Frame(app)
main_frame.pack(pady=20, padx=40, fill="x", expand=True)

# Criar múltiplos meters e botões de envio em 4 colunas e 3 linhas
meters = []
commands = ["SET_RPM", "SET_PEDAL", "SET_TEMP", "SET_PRESSURE", "SET_FUEL", "SET_AIRFLOW", "SET_OIL_TEMP", "SET_COOLANT_TEMP", 
            "SET_VOLTAGE", "SET_SPEED", "SET_INJECTOR_A", "SET_INJECTOR_B"]
labels = ["RPM", "Pedal", "Manometro", "T.Red", "Injetor A", "Injetor B", "Injetor C", "Injetor D", 
          "MAP", "T.GNV", "P.GNV", "HPS"]
maxVal = ["5000", "1000", "250", "100", "25", "25", "25", "25", 
          "100", "100", "100", "100"]
unit = ["", "", "bar", "°C", "ms", "ms", "ms", "ms", 
          "bar", "°C", "bar", "bar"]

# Loop para criar os meters organizados em 4 colunas e 3 linhas
for i in range(12):
    row = i // 4  # Define a linha
    col = i % 4  # Define a coluna
    meter = create_meter_and_button(main_frame, row, col, labels[i], 0, maxVal[i],unit[i], 0, labels[i], commands[i])
    meters.append(meter)



# Inicia a aplicação
app.mainloop()
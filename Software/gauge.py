import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
import json
import serial
import serial.tools.list_ports

# Função para listar portas COM disponíveis
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
            status_label.configure(text=f"Erro ao conectar: {e}")
    else:
        status_label.configure(text="Selecione uma porta e baudrate válidos!")

# Função para carregar configurações de um arquivo JSON
def carregar_configuracoes():
    try:
        with open("config.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        # Configurações padrão
        config = {
            "meters": [
                {"command": "SET_RPM", "label": "RPM", "maxVal": 5000, "unit": ""},
                {"command": "SET_PEDAL", "label": "Pedal", "maxVal": 1000, "unit": ""},
                {"command": "SET_MANOMETER", "label": "Manômetro", "maxVal": 250, "unit": "bar"},
                {"command": "SET_TRED", "label": "T.Red", "maxVal": 100, "unit": "°C"},
            ]
        }
        salvar_configuracoes(config)
        return config

# Função para salvar configurações em um arquivo JSON
def salvar_configuracoes(config):
    with open("config.json", "w") as arquivo:
        json.dump(config, arquivo, indent=4)

# Função para abrir janela de configuração
def abrir_janela_configuracao():
    config_window = ttk.Toplevel(app)
    config_window.title("Editar Configurações")
    config_window.geometry("400x300")

    ttk.Label(config_window, text="Editar Configurações", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Exibir as configurações atuais e permitir edição
    for i, meter in enumerate(config["meters"]):
        ttk.Label(config_window, text=f"Meter {i + 1}:").grid(row=i + 1, column=0, sticky="w", padx=10)
        command_entry = ttk.Entry(config_window, width=15)
        command_entry.insert(0, meter["command"])
        command_entry.grid(row=i + 1, column=1, padx=10)

        label_entry = ttk.Entry(config_window, width=15)
        label_entry.insert(0, meter["label"])
        label_entry.grid(row=i + 1, column=2, padx=10)

        max_val_entry = ttk.Entry(config_window, width=10)
        max_val_entry.insert(0, meter["maxVal"])
        max_val_entry.grid(row=i + 1, column=3, padx=10)

        unit_entry = ttk.Entry(config_window, width=10)
        unit_entry.insert(0, meter["unit"])
        unit_entry.grid(row=i + 1, column=4, padx=10)

    ttk.Button(config_window, text="Salvar", command=lambda: salvar_configuracoes(config)).grid(row=len(config["meters"]) + 1, column=0, columnspan=5, pady=10)

# Função para criar Meter e Botão de envio
def create_meter_and_button(parent, row, col, label_text, max_value, meter_label, command):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=col, pady=10, padx=10, sticky="nsew")

    meter = Meter(
        frame,
        subtext=meter_label,
        amounttotal=max_value,
        metersize=140,
        metertype="semi",
        bootstyle="success",
        interactive=True
    )
    meter.grid(row=0, column=0, padx=10, sticky="ew")

    send_button = ttk.Button(frame, text="Send", bootstyle="success",
                             command=lambda: send_command(round(meter.amountusedvar.get()), command))
    send_button.grid(row=1, column=0, padx=10, sticky="ew")

    return meter

# Função para enviar comandos
def send_command(value, command):
    if bluetooth:
        command_message = f"{command}:{value}\n"
        bluetooth.write(command_message.encode())
        print(f"Comando enviado: {command_message}")
    else:
        print("Bluetooth não está conectado.")

# Janela principal
app = ttk.Window(themename="darkly")
app.title("Wave Forge")
app.geometry("800x700")

# Carregar configurações
config = carregar_configuracoes()

# Barra de menu
barra_menu = ttk.Menubutton(app, text="Menu", bootstyle="primary")
barra_menu.grid(row=0, column=0, padx=10, pady=5)

menu_opcoes = ttk.Menu(barra_menu, tearoff=False)
barra_menu["menu"] = menu_opcoes
menu_opcoes.add_command(label="Editar Configurações", command=abrir_janela_configuracao)

# Variáveis para porta e baudrate
porta_var = ttk.StringVar()
baudrate_var = ttk.IntVar(value=9600)

# Frame para conexão
conexao_frame = ttk.Frame(app)
conexao_frame.grid(row=0, column=1, sticky="e", padx=10, pady=5)

porta_menu = ttk.Menubutton(conexao_frame, text="Selecionar Porta", bootstyle="primary")
porta_menu.grid(row=0, column=0, padx=5)

menu_conexao = ttk.Menu(porta_menu, tearoff=False)
porta_menu["menu"] = menu_conexao
for porta in listar_portas():
    menu_conexao.add_radiobutton(label=porta, variable=porta_var, value=porta)

baudrate_menu = ttk.Menubutton(conexao_frame, text="Selecionar Baudrate", bootstyle="primary")
baudrate_menu.grid(row=0, column=1, padx=5)
for baudrate in [9600, 19200, 38400, 57600, 115200]:
    menu_conexao.add_radiobutton(label=str(baudrate), variable=baudrate_var, value=baudrate)

conectar_button = ttk.Button(conexao_frame, text="Conectar", bootstyle="success", command=conectar_serial)
conectar_button.grid(row=0, column=2, padx=5)

status_label = ttk.Label(conexao_frame, text="Não conectado", bootstyle="info")
status_label.grid(row=0, column=3, padx=5)

# Frame principal para os meters
main_frame = ttk.Frame(app)
main_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=40, sticky="nsew")

# Criar meters a partir das configurações
for i, meter in enumerate(config["meters"]):
    row = i // 4
    col = i % 4
    create_meter_and_button(main_frame, row, col, meter["label"], meter["maxVal"], f"{meter['label']} ({meter['unit']})", meter["command"])

# Iniciar aplicação
app.mainloop()

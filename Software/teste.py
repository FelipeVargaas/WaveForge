import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
import serial  # Biblioteca para comunicação Bluetooth

# Configuração do Bluetooth
try:
    bluetooth = serial.Serial(port="COM3", baudrate=9600, timeout=1)  # Ajuste "COM3" para a sua porta Bluetooth
    print("Bluetooth conectado!")
except serial.SerialException as e:
    print(f"Erro ao conectar ao Bluetooth: {e}")
    bluetooth = None

# Janela principal
app = ttk.Window(themename="darkly")  # Define o tema da interface
app.title("Wave Forge")
app.geometry("800x700")  # Aumenta o tamanho da janela para acomodar 12 meters

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
def create_meter_and_button(parent, row, col, label_text, min_value, max_value, initial_value, meter_label, command):
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
labels = ["RPM", "Pedal", "Temperatura", "Pressão", "Combustível", "Ar", "Óleo", "Temperatura do líquido", 
          "Voltagem", "Velocidade", "Injetor A", "Injetor B"]

# Loop para criar os meters organizados em 4 colunas e 3 linhas
for i in range(12):
    row = i // 4  # Define a linha
    col = i % 4  # Define a coluna
    meter = create_meter_and_button(main_frame, row, col, labels[i], 0, 100, 0, labels[i], commands[i])
    meters.append(meter)

# Inicia a aplicação
app.mainloop()

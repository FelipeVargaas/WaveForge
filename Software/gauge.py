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
app.geometry("1000x600")

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
def create_meter_and_button(parent, row, label_text, min_value, max_value, initial_value, meter_label, command):
    # Frame para o meter, botão e o label
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

    # Meter
    meter = Meter(
        frame,
        subtext=meter_label,
        amounttotal=max_value,
        amountused=initial_value,
        metersize=140,  # Tamanho do Meter
        metertype="semi",
        bootstyle="success",        
        meterstyle="TMeter",
        interactive=True  # Torna o Meter interativo    
    )
    meter.grid(row=0, column=0, padx=10, sticky="ew")
    # Botão Send
    send_button = ttk.Button(frame, text="Send", bootstyle="success", 
    command=lambda: send_command(round(meter.amountusedvar.get()), command))  # Arredonda o valor para inteiro
    send_button.grid(row=0, column=1, padx=10, sticky="ew")

    return meter

# Frame principal
main_frame = ttk.Frame(app)
main_frame.pack(pady=20, padx=20, fill="x")

# Criar múltiplos meters e botões de envio na mesma linha
meter1 = create_meter_and_button(main_frame, 0, "RPM", 0, 5000, 0, "RPM", "SET_RPM")
meter2 = create_meter_and_button(main_frame, 1, "Pedal", 0, 100, 0, "Pedal", "SET_PEDAL")
meter3 = create_meter_and_button(main_frame, 2, "Temperatura", 0, 100, 0, "Temperatura", "SET_TEMP")

# Inicia a aplicação
app.mainloop()

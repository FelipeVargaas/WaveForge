import customtkinter as ctk
import serial  # Biblioteca para comunicação serial

# Configurar Bluetooth
try:
    bluetooth = serial.Serial(port="COM3", baudrate=9600, timeout=1)  # Ajuste "COM3" para o nome da sua porta Bluetooth
    print("Bluetooth conectado!")
except serial.SerialException as e:
    print(f"Erro ao conectar ao Bluetooth: {e}")
    bluetooth = None

ctk.set_appearance_mode('dark')

app = ctk.CTk()
app.title('Wave Forge')
app.geometry('400x400')

titulo = ctk.CTkLabel(app, text='Gerador de Sinais')
titulo.pack(pady='10')

# Função para criar um slider com label e botão de envio
def create_slider_with_label(parent, from_, to, initial_value, label_text, send_command):
    # Frame para alinhar o slider e o label
    slider_frame = ctk.CTkFrame(parent)
    slider_frame.pack(pady='10', padx='10', fill='x')

    slider_title = ctk.CTkLabel(slider_frame, text=label_text)
    slider_title.grid(row=0, column=0, padx=5)

    # Slider dentro do Frame
    slider = ctk.CTkSlider(slider_frame, from_=from_, to=to)
    slider.grid(row=0, column=1, padx=5)
    slider.set(initial_value)  # Define o valor inicial

    # Label dentro do Frame
    value_label = ctk.CTkLabel(slider_frame, text=int(initial_value))
    value_label.grid(row=0, column=2, padx=5)

    def slider_callback(value):
        value_label.configure(text=int(value))

    slider.configure(command=slider_callback)

    # Botão de envio
    def send_button_callback():
        if bluetooth:
            value = int(slider.get())
            command = f"{send_command}:{value}\n"
            bluetooth.write(command.encode())
            print(f"Comando enviado: {command}")
        else:
            print("Bluetooth não está conectado.")

    btn = ctk.CTkButton(slider_frame, text="Send", width=60, command=send_button_callback)
    btn.grid(row=0, column=3, padx=20)

    return slider, value_label

# Criar sliders reutilizando a função
slider1, label1 = create_slider_with_label(app, 0, 5000, 0, "RPM", "SET_RPM")
slider2, label2 = create_slider_with_label(app, 0, 200, 0, "Pedal", "SET_PEDAL")

app.mainloop()

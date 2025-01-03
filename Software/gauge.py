import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter

# Janela principal
app = ttk.Window(themename="darkly")  # Define o tema da interface
app.title("Wave Forge")
app.geometry("500x300")

# Função de callback para atualizar o Meter com o valor do Slider
def slider_event(value):
    value = int(float(value))  # Converte o valor do slider para inteiro
    rpm_meter.configure(amountused=value)  # Atualiza o Meter

# Frame para alinhar o Slider e o Meter
main_frame = ttk.Frame(app)
main_frame.pack(pady=20, padx=20, fill="x")

# Slider no lado esquerdo
slider = ttk.Scale(
    main_frame,
    from_=0,
    to=5000,
    command=slider_event,
    orient="horizontal",  # Slider horizontal
    bootstyle="primary"
)
slider.grid(row=0, column=0, padx=10, sticky="w")

# Meter no lado direito
rpm_meter = Meter(
    main_frame,
    subtext="RPM",
    amounttotal=5000,
    amountused=0,
    metersize=120,  # Tamanho do Meter
    bootstyle="success"
)
rpm_meter.grid(row=0, column=1, padx=10, sticky="e")

# Inicia a aplicação
app.mainloop()

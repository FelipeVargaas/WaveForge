import json
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from tkinter import filedialog, messagebox

# Função para carregar configurações do JSON e atualizar os valores dos meters
def load_config():
    try:
        # Abrir uma janela de diálogo para escolher o arquivo JSON
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de configuração",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not filepath:
            return  # Caso o usuário cancele a seleção

        # Abrir e carregar o conteúdo do arquivo JSON
        with open(filepath, 'r') as file:
            config = json.load(file)

        # Atualizar os valores dos meters com base nas chaves do JSON
        for label, meter in zip(labels, meters):
            if label in config:
                value = config[label]
                meter.amountusedvar.set(value)  # Atualiza o valor interno
                meter.configure(amountused=value)  # Atualiza visualmente o Meter
    except json.JSONDecodeError:
        messagebox.showerror("Erro no arquivo", "O arquivo selecionado não é um JSON válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo: {e}")

# Criar a aplicação principal
app = ttk.Window(themename="superhero")
app.title("Meters com Configuração JSON")
app.geometry("600x400")

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
        metertype="semi",
        bootstyle="success",
        stepsize=(max_value / 100),
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
labels = ["RPM", "Pedal", "Manômetro", "T.Red", "Injetor A", "Injetor B", "Injetor C", "Injetor D",
          "MAP", "T.GNV", "P.GNV", "HPS"]
maxVal = [5000, 1000, 250, 100, 25, 25, 25, 25, 100, 100, 100, 100]
unit = ["", "", "bar", "°C", "ms", "ms", "ms", "ms", "bar", "°C", "bar", "bar"]

# Loop para criar os meters organizados em 4 colunas e 3 linhas
for i in range(12):
    row = i // 4  # Define a linha
    col = i % 4  # Define a coluna
    meter = create_meter_and_button(main_frame, row, col, labels[i], 0, maxVal[i], unit[i], 0, labels[i], commands[i])
    meters.append(meter)

# Botão para carregar configurações
load_button = ttk.Button(
    app,
    text="Carregar Configurações",
    bootstyle="primary",
    command=load_config
)
load_button.pack(pady=20)

# Iniciar o loop principal da aplicação
app.mainloop()

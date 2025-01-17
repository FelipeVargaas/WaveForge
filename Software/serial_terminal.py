import tkinter as tk
from tkinter import scrolledtext
import threading

class SerialTerminal:
    def __init__(self, serial_connection):
        """
        Terminal Serial que utiliza uma conexão serial existente.
        :param serial_connection: Objeto da conexão serial já aberta.
        """
        self.serial_connection = serial_connection
        self.root = None
        self.text_area = None
        self.entry = None

    def send_command(self):
        """
        Envia o comando digitado para a conexão serial.
        """
        command = self.entry.get()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write((command + "\n").encode())
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, f"> {command}\n")
            self.text_area.configure(state='disabled')
        else:
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, "Erro: Conexão serial não disponível\n")
            self.text_area.configure(state='disabled')
        self.entry.delete(0, tk.END)

    def read_serial(self):
        """
        Lê dados da conexão serial em tempo real.
        """
        while self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()
                if data:
                    self.text_area.configure(state='normal')
                    self.text_area.insert(tk.END, f"{data}\n")
                    self.text_area.configure(state='disabled')
                    self.text_area.see(tk.END)
            except Exception as e:
                self.text_area.configure(state='normal')
                self.text_area.insert(tk.END, f"Erro ao ler dados: {e}\n")
                self.text_area.configure(state='disabled')
                break

    def clear_terminal(self):
        """
        Limpa o conteúdo do terminal.
        """
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state='disabled')

    def run(self):
        """
        Inicializa a interface do terminal.
        """
        self.root = tk.Toplevel()
        self.root.title("Terminal Serial - Wave Forge")
        self.root.geometry("600x400")

        # Área de texto para o terminal
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, state='disabled')
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame para o campo de entrada e botões
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # Campo de entrada
        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda event: self.send_command())

        # Botão de enviar
        send_button = tk.Button(bottom_frame, text="Enviar", command=self.send_command)
        send_button.pack(side=tk.LEFT)

        # Botão de limpar
        clear_button = tk.Button(self.root, text="Limpar", command=self.clear_terminal)
        clear_button.pack(pady=5)

        # Thread para leitura serial
        serial_thread = threading.Thread(target=self.read_serial, daemon=True)
        serial_thread.start()

        # Função para fechar a janela
        def on_close():
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_close)
        self.root.mainloop()

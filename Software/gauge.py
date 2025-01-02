import tkinter as tk
from ttkbootstrap import Style

def update_gauge(value):
    canvas.itemconfig(arc, extent=value * 3.5)  # Mapeia 0-100 para 0-270 graus

root = tk.Tk()
style = Style(theme="darkly")  # Tema moderno
root.title("RPM Gauge")

canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)
canvas.pack()

# Criando um arco como gauge
arc = canvas.create_arc(0, 0, 150, 150, start=240, extent=0, fill="lime", outline="")


# Controle deslizante para simular valores
scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=lambda v: update_gauge(int(v)))
scale.pack()

root.mainloop()
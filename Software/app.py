import customtkinter as ctk

ctk.set_appearance_mode('dark')

slider_val = ''
app = ctk.CTk()
app.title('Wave Forge')
app.geometry('300x300')

titulo = ctk.CTkLabel(app,text='Gerador de RPM')
titulo.pack(pady='10')

valor_slider = ctk.CTkLabel(app,text='Valor: ' + slider_val)
valor_slider.pack(pady='10')

def button_event():
    print("button pressed")

button = ctk.CTkButton(app, text="CTkButton", command=button_event)
button.pack()

def slider_event(value):
    slider_val = value
    print(str(value) + '  ' + str(slider_val))
    valor_slider.configure(text='Valorrr: ' + str(slider_val)) 

slider = ctk.CTkSlider(app, from_=0, to=100, command=slider_event)
slider.pack(pady='10')



app.mainloop()
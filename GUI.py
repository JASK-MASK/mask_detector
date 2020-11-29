#!/usr/bin/env python3
import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox,PhotoImage

# Creación de la ventana
v = tk.Tk() 
v.title('JASK-MASK')

# Especificaciones de tamaño y fondo de la GUI
v.configure(background ='gray12') 
w, h = v.winfo_screenwidth(), v.winfo_screenheight()
v.geometry("%dx%d+0+0" % (w, h))

# Mensajes a desplegar en la GUI
mensaje1 = tk.Label( 
    v, text ="Detector de uso de mascarilla",  
    bg ='gray15', fg = 'maroon1', width = 65,  
    height = 2, font = ('mincho', 22, 'bold'))  
      
mensaje1.place(x = 0, y = 20) 

mensaje2 = tk.Label( 
    v, text ="El SARS-CoV-2 es un\n virus contagioso \n\n\nCuidémonos todos\n\n\n¡Use mascarilla!",  
    bg ='gray12', fg = 'maroon1', width = 25,  
    height = 15, font = ('helvetica', 20))  
      
mensaje2.place(x = 0, y = 150) 

mensaje3 = tk.Label( 
    v, text ="No olvide el protocolo:\n\nLavar las manos\n\n\nAplicar alcohol en gel\n\n\nTomar la temperatura\n\n\n Mantener 1.8m de distancia",  
    bg ='gray12', fg = 'maroon1', width = 25,  
    height = 15, font = ('helvetica', 20))  
      
mensaje3.place(x = 985, y = 150)


# Importación de imágen 
#image = tk.PhotoImage(file="./mask.jpg")
#label = tk.Label(image=image)
#label.place(x = 485, y = 150)


# Ventana de advertencia al cerrar la GUI
def on_closing():

        if messagebox.askokcancel("Salir", "¿Está segura/o?"):
            v.destroy() 
v.protocol("WM_DELETE_WINDOW", on_closing)

# Función para llamar al archivo detector de mascarilla
def run():
    os.system('python3 detector.py')

arial32 = tkFont.Font(family='arial', size=32, weight='bold')

# Definición de botón en la GUI que activa el detector de mascarilla
btn = Button(v, text="Activar Detector", bg="gray25", fg="DeepPink2",command=run, font=arial32)
btn.place(x = 506, y = 555)

# Ejecución de la ventana y sus elementos
v.mainloop()
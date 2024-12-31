from tkinter import Tk, Label, Frame, Entry
from PIL import Image, ImageTk

class Login:

    def __init__(self):
        # Creación de la ventana
        self.ventana = Tk()
        self.ventana.geometry("400x600")
        self.ventana.title("Login")
        self.ventana.resizable(0, 0)

        fondo = "#daeaf6"

        # Frame superior
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.config(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        self.titulo=Label(self.frame_superior,
                          text="Login",
                          font=("Calisto MT",30,"bold"),
                          bg=fondo)
        self.titulo.pack(side="top",pady=10)

        # Cargar la imagen
        self.img = Image.open("usuario.png")
        self.img = self.img.resize((145, 150))
        self.render = ImageTk.PhotoImage(self.img)

        # Mostrar la imagen
        self.fondo = Label(self.frame_superior, image=self.render, bg=fondo)
        # Cambia el valor de `pady` para ajustar la posición vertical
        self.fondo.pack(expand=True, side="top", pady=0)  # Reduce el espacio vertical

        # Frame inferior
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.config(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        #Etiquetas usuarios 
        self.label_usuario=Label(self.frame_inferior,
                                 text="Usuario:",
                                 font=("Arial,18"),
                                 bg=fondo,
                                 fg="black")
        self.label_usuario.grid(row=0,column=0,padx=10,sticky="e")

        self.entry_usuario=Entry(self.frame_inferior,
                                 bd=0,
                                 width=14,
                                 font=("Arial,18"))
        self.entry_usuario.grid(row=0,column=1,columnspan=3,padx=5,sticky="w")

        
        #Etiquetas usuarios 
        self.label_contraseña=Label(self.frame_inferior,
                                 text="Contraseña:",
                                 font=("Arial,18"),
                                 bg=fondo,
                                 fg="black")
        self.label_contraseña.grid(row=0,column=0,padx=10,sticky="e")

        self.entry_contraseña=Entry(self.frame_inferior,
                                 bd=0,
                                 width=14,
                                 font=("Arial,18")
                                 show="*")
        self.entry_contraseña.grid(row=0,column=1,columnspan=3,padx=5,sticky="w")        

        # Iniciar el bucle principal
        self.ventana.mainloop()

# Crear una instancia de la clase Login
Login()

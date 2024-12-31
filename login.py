# login_app.py
from tkinter import Tk, Label, Frame, Entry, Button, messagebox
from PIL import Image, ImageTk
from usuario import Usuario

class Login:
    def __init__(self):
        # Creación de la ventana
        self.ventana = Tk()
        self.ventana.geometry("400x500")
        self.ventana.title("Login")
        self.ventana.resizable(0, 0)

        fondo = "#9cadce"

        # Frame superior
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.config(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        self.titulo = Label(
            self.frame_superior,
            text="Login",
            font=("Calisto MT", 30, "bold"),
            bg=fondo
        )
        self.titulo.pack(side="top", pady=10)

        # Cargar la imagen
        try:
            self.img = Image.open("usuario.png")
            self.img = self.img.resize((145, 150))
            self.render = ImageTk.PhotoImage(self.img)

            # Mostrar la imagen
            self.fondo = Label(self.frame_superior, image=self.render, bg=fondo)
            self.fondo.pack(expand=True, side="top", pady=10)
        except FileNotFoundError:
            messagebox.showwarning("Imagen no encontrada", "La imagen 'usuario.png' no se encontró.")

        # Frame inferior
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.config(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        # Configurar columnas para mejor alineación
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=2)

        # Etiqueta y entrada para Usuario
        self.label_usuario = Label(
            self.frame_inferior,
            text="Usuario:",
            font=("Arial", 18),
            bg=fondo,
            fg="black"
        )
        self.label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_usuario = Entry(
            self.frame_inferior,
            bd=1,
            font=("Arial", 18)
        )
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Etiqueta y entrada para Contraseña
        self.label_contraseña = Label(
            self.frame_inferior,
            text="Contraseña:",
            font=("Arial", 18),
            bg=fondo,
            fg="black"
        )
        self.label_contraseña.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_contraseña = Entry(
            self.frame_inferior,
            bd=1,
            font=("Arial", 18),
            show="*"
        )
        self.entry_contraseña.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Botones
        self.boton_ingresar = Button(
            self.frame_inferior,
            text="Ingresar",
            width=16,
            font=("Arial", 12),
            command=self.entrar
        )
        self.boton_ingresar.grid(row=2, column=0, padx=10, pady=35)

        self.boton_crear = Button(
            self.frame_inferior,
            text="Registrarse",
            width=16,
            font=("Arial", 12),
            command=self.registrar
        )
        self.boton_crear.grid(row=2, column=1, padx=10, pady=35)

        # Iniciar el bucle principal
        self.ventana.mainloop()

    def entrar(self):
        nombre = self.entry_usuario.get().strip()
        contra = self.entry_contraseña.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        if Usuario.verificar_usuario(nombre, contra):
            messagebox.showinfo("Acceso Correcto", f"Bienvenido, {nombre}!")
            # Aquí puedes agregar la lógica después del login exitoso
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")

    def registrar(self):
        nombre = self.entry_usuario.get().strip()
        contra = self.entry_contraseña.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        if Usuario.registrar_usuario(nombre, contra):
            messagebox.showinfo("Registro Exitoso", f"Usuario '{nombre}' registrado correctamente.")
        else:
            messagebox.showerror("Registro Fallido", "El usuario ya existe.")

# Crear una instancia de la clase Login
if __name__ == "__main__":
    Login()

# banco_app.py
import tkinter as tk
from tkinter import messagebox
from usuario import Usuario
from cuenta_bancaria import cuentabancaria
import json

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco Simulado")
        self.root.geometry("400x500")
        self.root.resizable(0, 0)

        self.usuario_actual = None
        self.cuenta_actual = None

        # Frame principal (login/register)
        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(pady=50)

        self.lbl_titulo = tk.Label(self.frame_principal, text="Bienvenido al Banco", font=("Arial", 18))
        self.lbl_titulo.pack(pady=10)

        # Botones para Iniciar Sesión y Registrarse
        tk.Button(self.frame_principal, text="Iniciar Sesión", width=20, command=self.mostrar_login).pack(pady=5)
        tk.Button(self.frame_principal, text="Registrarse", width=20, command=self.mostrar_registro).pack(pady=5)

        # Frame de Login
        self.frame_login = tk.Frame(root)

        tk.Label(self.frame_login, text="Nombre de Usuario:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_login_usuario = tk.Entry(self.frame_login)
        self.entry_login_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_login, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_login_contrasena = tk.Entry(self.frame_login, show="*")
        self.entry_login_contrasena.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame_login, text="Ingresar", width=15, command=self.ingresar_login).grid(row=2, columnspan=2, pady=10)

        # Frame de Registro
        self.frame_registro = tk.Frame(root)

        tk.Label(self.frame_registro, text="Nombre de Usuario:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_registro_usuario = tk.Entry(self.frame_registro)
        self.entry_registro_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_registro, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_registro_contrasena = tk.Entry(self.frame_registro, show="*")
        self.entry_registro_contrasena.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame_registro, text="Registrar", width=15, command=self.ingresar_registro).grid(row=2, columnspan=2, pady=10)

        # Frame de Operaciones Bancarias
        self.frame_banco = tk.Frame(root)

        tk.Label(self.frame_banco, text="Bienvenido, ", font=("Arial", 14)).pack(pady=10)
        self.lbl_usuario = tk.Label(self.frame_banco, text="", font=("Arial", 12))
        self.lbl_usuario.pack()

        tk.Button(self.frame_banco, text="Consultar Saldo", width=20, command=self.consultar_saldo).pack(pady=5)
        tk.Button(self.frame_banco, text="Depositar", width=20, command=self.depositar).pack(pady=5)
        tk.Button(self.frame_banco, text="Retirar", width=20, command=self.retirar).pack(pady=5)
        tk.Button(self.frame_banco, text="Transferir", width=20, command=self.transferir).pack(pady=5)
        tk.Button(self.frame_banco, text="Ver Historial", width=20, command=self.ver_historial).pack(pady=5)
        tk.Button(self.frame_banco, text="Cerrar Sesión", width=20, command=self.cerrar_sesion).pack(pady=20)

    def mostrar_login(self):
        self.frame_principal.pack_forget()
        self.frame_registro.pack_forget()
        self.frame_login.pack()

    def mostrar_registro(self):
        self.frame_principal.pack_forget()
        self.frame_login.pack_forget()
        self.frame_registro.pack()

    def ingresar_login(self):
        nombre = self.entry_login_usuario.get().strip()
        contrasena = self.entry_login_contrasena.get().strip()

        if not nombre or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        verificacion, resultado = Usuario.verificar_usuario(nombre, contrasena)
        if verificacion:
            self.usuario_actual = nombre
            numero_cuenta = resultado
            self.cuenta_actual = self.cargar_cuenta(numero_cuenta)
            if self.cuenta_actual:
                self.mostrar_panel_banco()
                self.frame_login.pack_forget()
        else:
            messagebox.showerror("Error de Inicio", resultado)

    def ingresar_registro(self):
        nombre = self.entry_registro_usuario.get().strip()
        contrasena = self.entry_registro_contrasena.get().strip()

        if not nombre or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        exito, mensaje = Usuario.registrar_usuario(nombre, contrasena)
        if exito:
            messagebox.showinfo("Registro Exitoso", mensaje)
            self.frame_registro.pack_forget()
            self.frame_principal.pack()
        else:
            messagebox.showerror("Error de Registro", mensaje)

    def cargar_cuenta(self, numero_cuenta, archivo='cuentas.json'):
        cuentas = cuentabancaria.cargar_cuentas(archivo)
        if numero_cuenta in cuentas:
            datos = cuentas[numero_cuenta]
            cuenta = cuentabancaria(
                numero_cuenta,
                datos['titular'],
                datos['saldo'],
                datos['tipo_cuenta']
            )
            cuenta.historial = datos.get('historial', [])
            return cuenta
        else:
            messagebox.showerror("Error", "Cuenta bancaria no encontrada.")
            return None

    def mostrar_panel_banco(self):
        self.frame_banco.pack()
        self.lbl_usuario.config(text=f"{self.usuario_actual} - Cuenta: {self.cuenta_actual.numero_cuenta}")

    def consultar_saldo(self):
        saldo = self.cuenta_actual.consultar_saldo()
        messagebox.showinfo("Saldo Disponible", f"Su saldo es: ${saldo:.2f}")

    def depositar(self):
        self.operacion_monto("Depositar", self.cuenta_actual.depositar)

    def retirar(self):
        self.operacion_monto("Retirar", self.cuenta_actual.retirar)

    def transferir(self):
        def realizar_transferencia():
            cuenta_destino = entry_cuenta_destino.get().strip()
            monto_str = entry_monto.get().strip()
            if not cuenta_destino or not monto_str:
                messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
                return
            try:
                monto = float(monto_str)
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido.")
                return
            mensaje = self.cuenta_actual.transferir(monto, cuenta_destino)
            messagebox.showinfo("Resultado", mensaje)
            ventana.destroy()

        ventana = tk.Toplevel(self.root)
        ventana.title("Transferir")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Cuenta Destino:").pack(pady=10)
        entry_cuenta_destino = tk.Entry(ventana)
        entry_cuenta_destino.pack(pady=5)

        tk.Label(ventana, text="Monto:").pack(pady=10)
        entry_monto = tk.Entry(ventana)
        entry_monto.pack(pady=5)

        tk.Button(ventana, text="Transferir", command=realizar_transferencia).pack(pady=20)

    def ver_historial(self):
        historial = self.cuenta_actual.obtener_historial()
        messagebox.showinfo("Historial de Transacciones", historial)

    def operacion_monto(self, titulo, funcion):
        def realizar_operacion():
            monto_str = entry_monto.get().strip()
            if not monto_str:
                messagebox.showwarning("Campo Vacío", "Por favor, ingrese un monto.")
                return
            try:
                monto = float(monto_str)
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido.")
                return
            mensaje = funcion(monto)
            messagebox.showinfo("Resultado", mensaje)
            ventana.destroy()

        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("300x150")

        tk.Label(ventana, text="Monto:").pack(pady=10)
        entry_monto = tk.Entry(ventana)
        entry_monto.pack(pady=5)

        tk.Button(ventana, text=titulo, command=realizar_operacion).pack(pady=20)

    def cerrar_sesion(self):
        confirmacion = messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?")
        if confirmacion:
            self.usuario_actual = None
            self.cuenta_actual = None
            self.frame_banco.pack_forget()
            self.frame_principal.pack()
            # Limpiar campos de login
            self.entry_login_usuario.delete(0, tk.END)
            self.entry_login_contrasena.delete(0, tk.END)

if __name__ == "__main__":
    # Crear cuentas de ejemplo si no existen
    cuentas_existentes = cuentabancaria.cargar_cuentas()
    if not cuentas_existentes:
        exito1, mensaje1 = cuentabancaria.crear_cuenta("12345678", "Juan Perez", 1000, "Ahorro")
        exito2, mensaje2 = cuentabancaria.crear_cuenta("87654321", "Maria Lopez", 2000, "Corriente")
        print(mensaje1)
        print(mensaje2)
    
    # Crear usuarios de ejemplo si no existen
   # usuarios_existentes = Usuario.cargar_usuarios()
    #if not usuarios_existentes:
     #   exito3, mensaje3 = Usuario.registrar_usuario("Juan", "password123")
      #  exito4, mensaje4 = Usuario.registrar_usuario("Maria", "password456")
       # print(mensaje3)
        #print(mensaje4)
    

    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()


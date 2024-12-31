# usuario.py
import json
import os
import bcrypt

class Usuario:
    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = self.hash_password(contrasena)

    @staticmethod
    def hash_password(contrasena):
        """Hash de la contraseña usando bcrypt."""
        hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
        return hashed.decode()

    @classmethod
    def verificar_usuario(cls, nombre, contrasena, archivo='usuarios.json'):
        """Verifica si el usuario y la contraseña son correctos."""
        if not os.path.exists(archivo):
            return False
        with open(archivo, 'r') as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = {}
        contrasena_hash = usuarios.get(nombre)
        if not contrasena_hash:
            return False
        return bcrypt.checkpw(contrasena.encode(), contrasena_hash.encode())

    @classmethod
    def registrar_usuario(cls, nombre, contrasena, archivo='usuarios.json'):
        """Registra un nuevo usuario si no existe."""
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                try:
                    usuarios = json.load(f)
                except json.JSONDecodeError:
                    usuarios = {}
        else:
            usuarios = {}
        if nombre in usuarios:
            return False  # Usuario ya existe
        usuarios[nombre] = cls.hash_password(contrasena)
        with open(archivo, 'w') as f:
            json.dump(usuarios, f, indent=4)
        return True

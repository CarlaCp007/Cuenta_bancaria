# cuenta_bancaria.py
import json
import os

class cuentabancaria:
    def __init__(self, numero_cuenta, titular, saldo, tipo_cuenta):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo
        self.tipo_cuenta = tipo_cuenta
        self.historial = []

    @classmethod
    def cargar_cuentas(cls, archivo='cuentas.json'):
        """Carga las cuentas desde un archivo JSON."""
        if not os.path.exists(archivo):
            return {}
        with open(archivo, 'r') as f:
            try:
                cuentas = json.load(f)
            except json.JSONDecodeError:
                cuentas = {}
        return cuentas

    @classmethod
    def guardar_cuentas(cls, cuentas, archivo='cuentas.json'):
        """Guarda las cuentas en un archivo JSON."""
        with open(archivo, 'w') as f:
            json.dump(cuentas, f, indent=4)

    def guardar_cuenta(self, archivo='cuentas.json'):
        """Guarda o actualiza la cuenta en el archivo JSON."""
        cuentas = self.cargar_cuentas(archivo)
        cuentas[self.numero_cuenta] = {
            'titular': self.titular,
            'saldo': self.saldo,
            'tipo_cuenta': self.tipo_cuenta,
            'historial': self.historial
        }
        self.guardar_cuentas(cuentas, archivo)

    @classmethod
    def crear_cuenta(cls, numero_cuenta, titular, saldo, tipo_cuenta='Ahorro', archivo='cuentas.json'):
        """Crea una nueva cuenta bancaria."""
        cuentas = cls.cargar_cuentas(archivo)
        if numero_cuenta in cuentas:
            return False, "La cuenta ya existe."
        nueva_cuenta = cls(numero_cuenta, titular, saldo, tipo_cuenta)
        nueva_cuenta.guardar_cuenta(archivo)
        return True, "Cuenta creada exitosamente."

    def consultar_saldo(self):
        return self.saldo

    def depositar(self, monto):
        if monto <= 0:
            return "El monto debe ser positivo."
        self.saldo += monto
        self.historial.append(f"Depósito: +${monto}")
        self.guardar_cuenta()
        return "Depósito realizado con éxito."

    def retirar(self, monto):
        if monto <= 0:
            return "El monto debe ser positivo."
        if monto > self.saldo:
            return "Saldo insuficiente."
        self.saldo -= monto
        self.historial.append(f"Retiro: -${monto}")
        self.guardar_cuenta()
        return "Retiro realizado con éxito."

    def transferir(self, monto, cuenta_destino, archivo='cuentas.json'):
        if monto <= 0:
            return "El monto debe ser positivo."
        cuentas = self.cargar_cuentas(archivo)
        if cuenta_destino not in cuentas:
            return "La cuenta de destino no es válida."
        if monto > self.saldo:
            return "Saldo insuficiente."
        # Retirar del origen
        self.saldo -= monto
        self.historial.append(f"Transferencia: -${monto} a cuenta {cuenta_destino}")
        # Depositar en el destino
        cuenta_dest = cuentas[cuenta_destino]
        cuenta_dest['saldo'] += monto
        cuenta_dest['historial'].append(f"Transferencia: +${monto} desde cuenta {self.numero_cuenta}")
        # Guardar cambios
        cuentas[self.numero_cuenta]['saldo'] = self.saldo
        cuentas[self.numero_cuenta]['historial'] = self.historial
        self.guardar_cuentas(cuentas, archivo)
        return "Transferencia realizada con éxito."

    def obtener_historial(self):
        return "\n".join(self.historial) if self.historial else "No hay transacciones."

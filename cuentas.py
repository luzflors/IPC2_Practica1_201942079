from abc import ABC, abstractmethod
import random

class Cuenta(ABC):
    def __init__(self, titular, saldo):
        self._titular = titular
        self._saldo = saldo
        self.numero_cuenta = self._crearNumeroCuenta()
    
    @abstractmethod
    def retiros(self, monto):
        pass

    @abstractmethod
    def depositos(self, monto):
        pass

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, nuevo_saldo):
        self._saldo = nuevo_saldo
    
    @property
    def titular(self):
        return self._titular
    
    def datosCuenta(self):
        return f"Titular: {self.titular}\nNumero de cuenta: {self.numero_cuenta}\nSaldo: {self.saldo}"
    
    def _crearNumeroCuenta(self):
        return random.randint(10**15, 10**16 - 1)
    
class Cuenta_Monetaria(Cuenta):
    def __init__(self, titular, saldo, limite_credito):
        super().__init__(titular, saldo)
        self._limite_credito = limite_credito
        self._credito = limite_credito
    
    @property
    def credito(self):
        return self._credito

    @property
    def limite_credito(self):
        return self._limite_credito
    
    def retiros(self, monto):
        if self.saldo < monto:
            faltante = monto - self.saldo
            if faltante <= self._limite_credito:
                opcion = input("Desea retirar de su crédito? (S/N): ").strip().upper()
                while opcion not in ('S', 'N'):
                    opcion = input("Opción incorrecta. Intente nuevamente (S/N): ").strip().upper()
                if opcion == 'S':
                    self.saldo = 0
                    self._credito -= faltante
                    print(f"Transaccion exitosa. \nNuevo saldo: {self.saldo}")
                    
                else:
                    print(f"Saldo insuficiente. \nTransaccion invalida")
            else:
                print(f"Credito insuficiente. \nTransaccion invalida")
        else:
            self.saldo -= monto
            print(f"Transaccion exitosa. \nNuevo saldo: {self.saldo}")

    def depositos(self, monto):
        if self._credito == self._limite_credito:
            self.saldo += monto
        else:
            faltante = self._limite_credito - self._credito
            if monto <= faltante:
                self._credito += monto
            else:
                self._credito = self._limite_credito
                self.saldo += (monto - faltante)
        print(f"Transaccion exitosa. \nNuevo saldo: {self.saldo}")



class Cuenta_Ahorro(Cuenta):
    def __init__(self, titular, saldo, tasa):
        super().__init__(titular, saldo)
        self._tasa = tasa

    @property
    def tasa(self):
        return self._tasa

    def calcularInteres(self):
        intresesSaldo = self.saldo * (self.tasa / 100)
        self.saldo += intresesSaldo
        return intresesSaldo
    
    def retiros(self, monto):
        if(monto <= self.saldo):
            self.saldo -= monto
            print(f"Transacción exitosa.\nNuevo saldo: {self.saldo}")
        else:
            print(f"Saldo insuficiente. \nTransaccion Invalida")

    def depositos(self, monto):
        self.saldo += monto

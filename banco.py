from cuentas import Cuenta_Ahorro
from cuentas import Cuenta_Monetaria

class Nuevo:
    def __init__(self):
        self._listaCuentaMonetaria = []
        self._listaCuentaAhorro = []

    def Menu(self):
        print(f"====================================================")
        print(f"|          *         Menu Banco       *            |")
        print(f"====================================================")
        print(f"| 1. Abrir Cuenta                                  |")
        print(f"| 2. Gestionar Cuenta                              |")
        print(f"| 3. Salir                                         |")
        print(f"====================================================")
        opcion = input(f"\nSeleccione opcion: ").strip().upper()
        while opcion not in (1,2,3):
            opcion = input(f"Numero invalido \Seleccione una opcion valida: ").strip().upper()
        if opcion == 1:
            self.AbrirCuenta()
        elif opcion == 2:
            self.GestionarCuenta()
        else:
            print(f"Bye")

    def AbrirCuenta(self):
        print(f"====================================================")
        print(f"|          *       Abrir Cuenta       *            |")
        print(f"====================================================")
        print(f"| 1. Cuenta de ahorro                              |")
        print(f"| 2. Cuenta monetaria                              |")
        print(f"| 3. Regresar                                      |")
        print(f"====================================================")
        opcion = input(f"\nSeleccione opcion: ").strip().upper()
        while opcion not in (1,2,3):
            opcion = input(f"Numero invalido \Seleccione una opcion valida: ").strip().upper()

        if opcion == 1 or opcion == 2:
            if opcion == 1:
                print("------------ Abrir cuenta de Ahorro ------------")
            else:
                print("------------ Abrir cuenta Monetaria ------------")
            
            titular = input(f"\nIngresar titular: ").strip().upper()     
            saldo = float(input("Ingresar saldo: "))

        if opcion == 1:
            interes = float(input("Ingrese porcentaje de interes: "))
            self.listaCuentaAhorro.append(Cuenta_Ahorro(titular, saldo, interes))
        elif opcion == 2:
            limiteCredito = float(input("Ingrese limite de credito: "))
            self.listaCuentaMonetaria.append(Cuenta_Monetaria(titular, saldo, limiteCredito))
        else:
            print(f"\nRegresando...\n")
   

    def GestionarCuenta(self):
        print("====================================================")
        print("|          *     Gestionar Cuentas    *            |")
        print("====================================================")
        print("| 1. Ver informacion de cuentas                    |")
        print("| 2. Depositar dinero                              |")
        print("| 3. Retirar dinero                                |")
        print("| 4. Calcular interes (Solo Cuenta de Ahorro)      |")
        print("| 5. Regresar                                      |")
        print("====================================================")
        opcion = input(f"\nSeleccione opcion: ").strip().upper()
        while opcion not in (1,2,3,4,5):
            opcion = input(f"Numero invalido \Seleccione una opcion valida: ").strip().upper()
        if opcion == 1:
            print("------------ Ver Informacion de Cuentas ------------")
            self.verInformacion()
            return
        elif opcion == 2:
            print("------------ Depositos ------------")
            self.depositarCuentas()
            return
        elif opcion == 3:
            print("------------ Retiros ------------")
            self.retirarCuentas()
            opcion = 5
            return
        elif opcion == 4:
            print("------------ Calculo de interes ------------")
            self.calcularInteres()
            return
        else:
            print(f"\nRegresando...\n")

    def verInformacion(self):
        if self._listaCuentaAhorro or self._listaCuentaMonetaria:
            if self._listaCuentaAhorro:
                print("\n**********   Cuentas de Ahorro  **********")
                for cuenta_Ahorro in self._listaCuentaAhorro:
                    print(cuenta_Ahorro.datosCuenta())
                    print("Tasa de Interes: " + str(cuenta_Ahorro.tasa) + "%\n")
            if self._listaCuentaMonetaria:
                print("\n**********   Cuentas Monetarias  **********")
                for cuenta_Monetaria in self._listaCuentaMonetaria:
                    print(cuenta_Monetaria.datosCuenta())
                    print("Credito Disponible: " + str(cuenta_Monetaria.credito))
                    print("Limite de Credito: " + str(cuenta_Monetaria.limite_credito) + "\n")
        else:
            print("No existen cuentas")

    def depositarCuentas(self):
        if self._listaCuentaAhorro or self._listaCuentaMonetaria:
            print("\nA que tipo de cuenta desea depositar? \n1. Ahorro \n2. Monetaria")
            opcion = input(f"\nSeleccione opcion: ").strip().upper()
            while opcion not in (1,2,3,4,5):
                opcion = input(f"Numero invalido \Seleccione una opcion valida: ").strip().upper()
                if self._listaCuentaAhorro and self.opcion == 1:
                    if len(self._listaCuentaAhorro) > 1:
                        print("\n**********   Cuentas de Ahorro  **********")
                        i = 1
                        for cuenta_Ahorro in self._listaCuentaAhorro:
                            print(str(i) + ". " + cuenta_Ahorro.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        print("\nSeleccione opcion: ")
                        self.opcion = int(input())
                    else:
                        self.opcion = 1
                    print("\nIngrese monto a depositar: ")
                    montoDeposito = float(input())
                    if self.opcion > 0 and self.opcion <= len(self._listaCuentaAhorro):
                        self._listaCuentaAhorro[self.opcion - 1].depositos(montoDeposito)
                    else:
                        print("Numero incorrecto")
                elif not self._listaCuentaAhorro:
                    print("No existen cuentas de ahorro")

                if self._listaCuentaMonetaria and self.opcion == 2:
                    print("\n**********   Cuentas Monetarias  **********")
                    if len(self._listaCuentaMonetaria) > 1:
                        for cuenta_Monetaria in self._listaCuentaMonetaria:
                            i = 1
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nA cual cuenta de Monetaria? ")
                        print("\nSeleccione opcion: ")
                        self.opcion = int(input())
                    else:
                        self.opcion = 1
                    print("\nIngrese monto a depositar: ")
                    montoDeposito = float(input())
                    if self.opcion > 0 and self.opcion <= len(self._listaCuentaMonetaria):
                        self._listaCuentaMonetaria[self.opcion - 1].depositos(montoDeposito)
                    else:
                        print("Numero incorrecto")
                elif not self._listaCuentaMonetaria:
                    print("No existen cuentas monetarias")
        else:
            print("No existen cuentas de ahorro ni monetarias")

    def retirarCuentas(self):
        if self._listaCuentaAhorro or self._listaCuentaMonetaria:
            print("\nA que tipo de cuenta desea retirar? \n1. Ahorro \n2. Monetaria")
            opcion = input(f"\nSeleccione opcion: ").strip().upper()
            while opcion not in (1,2,3,4,5):
                opcion = input(f"Numero invalido \Seleccione una opcion valida: ").strip().upper()
                if self._listaCuentaAhorro and self.opcion == 1:
                    if len(self._listaCuentaAhorro) > 1:
                        print("\n**********   Cuentas de Ahorro  **********")
                        i = 1
                        for cuenta_Ahorro in self._listaCuentaAhorro:
                            print(str(i) + ". " + cuenta_Ahorro.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        print("\nSeleccione opcion: ")
                        self.opcion = int(input())
                    else:
                        self.opcion = 1
                    print("\nIngrese monto a retirar: ")
                    montoDeposito = float(input())
                    if self.opcion > 0 and self.opcion <= len(self._listaCuentaAhorro):
                        self._listaCuentaAhorro[self.opcion - 1].retiros(montoDeposito)
                    else:
                        print("Numero incorrecto")
                elif not self._listaCuentaAhorro:
                    print("No existen cuentas de ahorro")

                if self._listaCuentaMonetaria and self.opcion == 2:
                    print("\n**********   Cuentas Monetarias  **********")
                    if len(self._listaCuentaMonetaria) > 1:
                        for cuenta_Monetaria in self._listaCuentaMonetaria:
                            i = 1
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nA cual cuenta de Monetaria? ")
                        print("\nSeleccione opcion: ")
                        self.opcion = int(input())
                    else:
                        self.opcion = 1
                    print("\nIngrese monto a depositar: ")
                    montoDeposito = float(input())
                    if self.opcion > 0 and self.opcion <= len(self._listaCuentaMonetaria):
                        self._listaCuentaMonetaria[self.opcion - 1].retiros(montoDeposito)
                    else:
                        print("Numero incorrecto")
                elif not self._listaCuentaMonetaria:
                    print("No existen cuentas monetarias")
        else:
            print("No existen cuentas de ahorro ni monetarias")

    def calcularInteres(self):
        if self._listaCuentaAhorro():
            for cuenta_Ahorro in self._listaCuentaAhorro:
                print(cuenta_Ahorro.datosCuenta())
                print("Interes calculado: " + str(cuenta_Ahorro.calcularInteres()))
                print("Saldo Nuevo: " + str(cuenta_Ahorro.saldo))
        else:
            print("No existen cuentas de ahorro")
    
from cuentas import Cuenta_Ahorro
from cuentas import Cuenta_Monetaria

class Banco:
    def __init__(self):
        self._listaCuentaMonetaria = []
        self._listaCuentaAhorro = []

    def Menu(self):
        while True:
            print(f"====================================================")
            print(f"|          *         Menu Banco       *            |")
            print(f"====================================================")
            print(f"| 1. Abrir Cuenta                                  |")
            print(f"| 2. Gestionar Cuenta                              |")
            print(f"| 3. Salir                                         |")
            print(f"====================================================")
            
            try:
                opcion = int(input(f"\nSeleccione opcion: ").strip())
            except ValueError:
                print("Error: Debe ingresar un número.")
                continue
            
            while opcion not in (1, 2, 3):
                try:
                    opcion = int(input(f"Numero invalido. Seleccione una opcion valida: ").strip())
                except ValueError:
                    print("Error: Debe ingresar un número.")
                    continue

            if opcion == 1:
                self.AbrirCuenta()
            elif opcion == 2:
                self.GestionarCuenta()
            elif opcion == 3:
                print(f"Bye")
                break

    def AbrirCuenta(self):
        print(f"====================================================")
        print(f"|          *       Abrir Cuenta       *            |")
        print(f"====================================================")
        print(f"| 1. Cuenta de ahorro                              |")
        print(f"| 2. Cuenta monetaria                              |")
        print(f"| 3. Regresar                                      |")
        print(f"====================================================")
        
        try:
            opcion = int(input(f"\nSeleccione opcion: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número.")
            return

        while opcion not in (1, 2, 3):
            try:
                opcion = int(input(f"Numero invalido. Seleccione una opcion valida: ").strip())
            except ValueError:
                print("Error: Debe ingresar un número.")
                return

        if opcion == 1 or opcion == 2:
            if opcion == 1:
                print("\n------------ Abrir cuenta de Ahorro ------------")
            else:
                print("\n------------ Abrir cuenta Monetaria ------------")
            
            titular = input(f"\nIngresar titular: ").strip().upper()     

            try:
                saldo = float(input("Ingresar saldo: "))
            except ValueError:
                print("Error: Debe ingresar un saldo válido.")
                return

            if opcion == 1:
                try:
                    interes = float(input("Ingrese porcentaje de interes: "))
                except ValueError:
                    print("Error: Debe ingresar un porcentaje de interés válido.")
                    return
                self._listaCuentaAhorro.append(Cuenta_Ahorro(titular, saldo, interes))
                print("Cuenta de ahorro creada exitosamente.")
            elif opcion == 2:
                try:
                    limiteCredito = float(input("Ingrese limite de credito: "))
                except ValueError:
                    print("Error: Debe ingresar un límite de crédito válido.")
                    return
                self._listaCuentaMonetaria.append(Cuenta_Monetaria(titular, saldo, limiteCredito))
                print("Cuenta monetaria creada exitosamente.")

        elif opcion == 3:
            print(f"\nRegresando...\n")
            return 

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
        
        try:
            opcion = int(input(f"\nSeleccione opcion: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número.")
            return

        while opcion not in (1, 2, 3, 4, 5):
            try:
                opcion = int(input(f"Numero invalido \Seleccione una opcion valida: ").strip())
            except ValueError:
                print("Error: Debe ingresar un número.")
                return

        if opcion == 1:
            print("\n------------ Ver Informacion de Cuentas ------------")
            self.verInformacion()
        elif opcion == 2:
            print("\n------------ Depositos ------------")
            self.depositarCuentas()
        elif opcion == 3:
            print("\n------------ Retiros ------------")
            self.retirarCuentas()
        elif opcion == 4:
            print("\n------------ Calculo de interes ------------")
            if self._listaCuentaAhorro:
                i = 1
                for cuenta_Ahorro in self._listaCuentaAhorro:
                    print("Cuenta numero: " + str(i))
                    print(cuenta_Ahorro.datosCuenta())
                    cuenta_Ahorro.generadorIntereses()
                    print("Intereses:" + str(cuenta_Ahorro.intereses))
                    print("\nAgregamos los intereses a la cuenta? \n1. Si \n2. No")
                    try:
                        opcion = int(input(f"\nSeleccione opcion: ").strip())
                    except ValueError:
                        print("Error: Debe ingresar un número.")
                        return
                    while opcion not in (1, 2):
                        try:
                            opcion = int(input(f"Numero invalido \Seleccione una opcion valida: ").strip())
                        except ValueError:
                            print("Error: Debe ingresar un número.")
                            return
                    if opcion == 1:
                        cuenta_Ahorro.saldo += cuenta_Ahorro.intereses
                        print(f"Transaccion exitosa. \nNuevo saldo: {cuenta_Ahorro.saldo}")
                    if opcion == 2:
                        print(f"Ok")
                    i += 1  
            else:
                print("No existen cuentas")
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
            try:
                opcion = int(input(f"\nSeleccione opcion: ").strip())
            except ValueError:
                print("Error: Debe ingresar un número.")
                return

            while opcion not in (1, 2):
                try:
                    opcion = int(input(f"Numero invalido \Seleccione una opcion valida: ").strip())
                except ValueError:
                    print("Error: Debe ingresar un número.")
                    return

            if opcion == 1:
                if self._listaCuentaAhorro:
                    if len(self._listaCuentaAhorro) > 1:
                        print("\n**********   Cuentas de Ahorro  **********")
                        i = 1
                        for cuenta_Monetaria in self._listaCuentaAhorro:
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        try:
                            opcion = int(input(f"\nSeleccione opcion: ").strip())
                        except ValueError:
                            print("Error: Debe ingresar un número.")
                            return

                    try:
                        montoDeposito = float(input("\nIngrese monto a depositar: ").strip())
                    except ValueError:
                        print("Error: Debe ingresar un monto válido.")
                        return
                    
                    if opcion > 0 and opcion <= len(self._listaCuentaAhorro):
                        opcion -= 1
                    else:
                        opcion = 0
                    self._listaCuentaAhorro[opcion].retiros(montoDeposito)
                else:
                    print("No existen cuentas de ahorro")
            elif opcion == 2:
                if self._listaCuentaMonetaria:
                    if len(self._listaCuentaMonetaria) > 1:
                        print("\n**********   Cuentas Monetairas  **********")
                        i = 1
                        for cuenta_Monetaria in self._listaCuentaMonetaria:
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        try:
                            opcion = int(input(f"\nSeleccione opcion: ").strip())
                        except ValueError:
                            print("Error: Debe ingresar un número.")
                            return

                    try:
                        montoDeposito = float(input("\nIngrese monto a depositar: ").strip())
                    except ValueError:
                        print("Error: Debe ingresar un monto válido.")
                        return
                    
                    if opcion > 0 and opcion <= len(self._listaCuentaMonetaria):
                        opcion -= 1
                    else:
                        opcion = 0
                    self._listaCuentaMonetaria[opcion].retiros(montoDeposito)
                else:
                    print("No existen cuentas Monetarias")

    def retirarCuentas(self):
        if self._listaCuentaAhorro or self._listaCuentaMonetaria:
            print("\nA que tipo de cuenta desea retirar? \n1. Ahorro \n2. Monetaria")
            try:
                opcion = int(input(f"\nSeleccione opcion: ").strip())
            except ValueError:
                print("Error: Debe ingresar un número.")
                return

            while opcion not in (1, 2):
                try:
                    opcion = int(input(f"Numero invalido \Seleccione una opcion valida: ").strip())
                except ValueError:
                    print("Error: Debe ingresar un número.")
                    return

            if opcion == 1:
                if self._listaCuentaAhorro:
                    if len(self._listaCuentaAhorro) > 1:
                        print("\n**********   Cuentas de Ahorro  **********")
                        i = 1
                        for cuenta_Monetaria in self._listaCuentaAhorro:
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        try:
                            opcion = int(input(f"\nSeleccione opcion: ").strip())
                        except ValueError:
                            print("Error: Debe ingresar un número.")
                            return

                    try:
                        montoRetirar = float(input("\nIngrese monto a retirar: ").strip())
                    except ValueError:
                        print("Error: Debe ingresar un monto válido.")
                        return
                    
                    if opcion > 0 and opcion <= len(self._listaCuentaAhorro):
                        opcion -= 1
                    else:
                        opcion = 0
                    self._listaCuentaAhorro[opcion].retiros(montoRetirar)
                else:
                    print("No existen cuentas de ahorro")

            if opcion == 2:
                if self._listaCuentaMonetaria:
                    if len(self._listaCuentaMonetaria) > 1:
                        print("\n**********   Cuentas Monetairas  **********")
                        i = 1
                        for cuenta_Monetaria in self._listaCuentaMonetaria:
                            print(str(i) + ". " + cuenta_Monetaria.datosCuenta())
                            i += 1
                        print("\nQue cuenta de Ahorro? ")
                        try:
                            opcion = int(input(f"\nSeleccione opcion: ").strip())
                        except ValueError:
                            print("Error: Debe ingresar un número.")
                            return

                    try:
                        montoRetirar = float(input("\nIngrese monto a retirar: ").strip())
                    except ValueError:
                        print("Error: Debe ingresar un monto válido.")
                        return
                    
                    if opcion > 0 and opcion <= len(self._listaCuentaMonetaria):
                        opcion -= 1
                    else:
                        opcion = 0
                    self._listaCuentaMonetaria[opcion].retiros(montoRetirar)
                else:
                    print("No existen cuentas Monetarias")

from banco import Banco

class Main:
    def __init__(self):
        banco = Banco()
        banco.Menu()

# Bloque principal
if __name__ == "__main__":
    print(f"\n - - - - - - - - - - - BANCO - - - - - - - - - - - \n")
    app = Main()
from banco import Nuevo

class Main:
    def __init__(self):
        banco = Nuevo()
        banco.Menu()

# Bloque principal
if __name__ == "__main__":
    print(f"\n - - - - - - - - - - - BANCO - - - - - - - - - - - \n")
    app = Main()
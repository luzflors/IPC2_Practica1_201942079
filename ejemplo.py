import os
import xml.etree.ElementTree as ET
import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class NodoProteina():
    def __init__(self, proteina, es_inerte):
        self._proteina = proteina
        self._es_inerte = es_inerte 
        self.siguiente = None
        self.abajo = None

    def get_proteina(self):
        return self._proteina

    def get_es_inerte(self):
        return self._es_inerte
    
    def get_set_es_inerte(self, es_inerte):
        self._es_inerte = es_inerte
    
    def mostrar(self):
        print(self._proteina)
        
class ListaProteina():
    def __init__(self):
        self.primero = None

    def contar_porcentaje_inertes(self):
        total_nodos = 0
        inertes = 0
        fila_actual = self.primero
        
        while fila_actual is not None:
            nodo_actual = fila_actual
            while nodo_actual is not None:
                total_nodos += 1
                if nodo_actual.get_es_inerte():
                    inertes += 1
                nodo_actual = nodo_actual.siguiente
            fila_actual = fila_actual.abajo
        
        if total_nodos == 0:
            return 0  
        return (inertes / total_nodos) * 100 

    def cargar_rejilla_en_lista(self, rejilla_txt, filas, columnas):
        pro = rejilla_txt.split()
        index = 0
        primera_fila = None
        fila_anterior = None
        for i in range(filas):
            cabeza_fila = None
            nodo_anterior = None
            for j in range(columnas):
                if index < len(pro):
                    nuevo = NodoProteina(pro[index], False)
                    index += 1
                else:
                    break
                if cabeza_fila is None:
                    cabeza_fila = nuevo
                else:
                    nodo_anterior.siguiente = nuevo
                nodo_anterior = nuevo
            if fila_anterior is not None:
                nodo_actual = cabeza_fila
                nodo_superior = fila_anterior
                while nodo_actual is not None and nodo_superior is not None:
                    nodo_superior.abajo = nodo_actual
                    nodo_superior = nodo_superior.siguiente
                    nodo_actual = nodo_actual.siguiente
            else:
                primera_fila = cabeza_fila
            fila_anterior = cabeza_fila
        self.primero = primera_fila

    def buscar_parejas(self, proteina01, proteina02):
        fila_actual = self.primero
        
        while fila_actual is not None:
            nodo_actual = fila_actual
            while nodo_actual is not None:

                if nodo_actual.get_es_inerte():
                    nodo_actual = nodo_actual.siguiente
                    continue

                if nodo_actual.siguiente is not None and not nodo_actual.siguiente.get_es_inerte():
                    if (nodo_actual.get_proteina() == proteina01 and
                        nodo_actual.siguiente.get_proteina() == proteina02):
                        nodo_actual._es_inerte = True
                        nodo_actual.siguiente._es_inerte = True
                        print("Encontro pareja")
                        return True  

                if nodo_actual.abajo is not None and not nodo_actual.abajo.get_es_inerte():
                    if (nodo_actual.get_proteina() == proteina01 and
                        nodo_actual.abajo.get_proteina() == proteina02):
                        nodo_actual._es_inerte = True
                        nodo_actual.abajo._es_inerte = True
                        print("Encontro pareja")
                        return True  

                nodo_actual = nodo_actual.siguiente
            fila_actual = fila_actual.abajo

        return False 


    def buscar(self, nombre):
        tmp = self.primero 
        while tmp:
            if tmp._proteina == nombre:
                return tmp
            tmp = tmp.siguiente
        return None
    
    def limpiar(self):
        while self.primero is not None:
            tmp = self.primero  
            self.primero = self.primero.siguiente  
            tmp.siguiente = None

class NodoExperimento():
    def __init__(self, nombre, filas, columnas, rejilla, pareja):
        self._nombre = nombre 
        self._filas = int(filas)
        self._columnas = int(columnas)
        self._rejilla = rejilla 
        self._pareja = pareja    
        self.siguiente = None 

    def get_nombre(self):
        return self._nombre if self._nombre is not None else 'Experimento'
    
    def get_rejilla(self):
        return self._rejilla if self._rejilla is not None else ""

    def get_pareja(self):
        return self._pareja if self._pareja is not None else ""

    def get_columnas(self):
        return int(self._columnas) if self._columnas is not None else 0
    
    def get_filas(self):
        return int(self._filas) if self._filas is not None else 0
    
    def mostrar(self):
        print(f"  Nombre: {self.get_nombre()}")
        print(f"  Filas: {self.get_filas()}")
        print(f"  Columnas: {self.get_columnas()}")
        print("  Rejilla:")
        print(self.get_rejilla())
        print(f"  Pareja(s): {self.get_pareja()}")
        
    
class ListaExperimento:
    def __init__(self):
        self.primero = None  

    def insertar(self, nombre, filas, columnas, rejilla, pareja):
        nuevo = NodoExperimento(nombre, filas, columnas, rejilla, pareja)
        if self.primero is None:
            self.primero = nuevo
        else:
            tmp = self.primero
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo

    def mostrar_experimentos(self):
        tmp = self.primero
        while tmp:
            tmp.mostrar()
            tmp = tmp.siguiente

    def buscar(self, nombre):
        tmp = self.primero 
        while tmp:
            if tmp.get_nombre() == nombre:
                return tmp
            tmp = tmp.siguiente
        return None 

    def modificar(self, nombre):
        self.buscar(nombre)

    def limpiar(self):
        while self.primero is not None:
            tmp = self.primero  
            self.primero = self.primero.siguiente  
            tmp.siguiente = None 

class ExperimentoXML():
    def __init__(self, archivo):
        self._archivo = archivo
        self._experimentos = ListaExperimento()
    
    def _cargar_xml(self):
        try:
            xml_file = ET.parse(self._archivo)
            return xml_file.getroot()
        except Exception as err:
            print("Error:", err)
        return None
    
    def extraer_xml(self):
        xml_raiz = self._cargar_xml()
        if xml_raiz is None:
            print('No existen datos')
            return
        
        for experimento in xml_raiz.findall('experimento'):
            nombre = experimento.get('nombre')
            rejilla = ""
            filas = 0
            columnas = 0
            
            tejido = experimento.find('tejido')
            if tejido is not None:
                rejilla = tejido.find('rejilla').text if tejido.find('rejilla') is not None else ""
                filas = int(tejido.get('filas'))
                columnas = int(tejido.get('columnas'))
            
            parejas = ""
            proteinas = experimento.find('proteinas')
            if proteinas is not None:
                primera_pareja = True 
                for pareja in proteinas.findall('pareja'):
                    pareja_texto = pareja.text.strip() if pareja.text else ""
                    if pareja_texto:
                        if not primera_pareja:
                            parejas += ", " 
                        parejas += pareja_texto
                        primera_pareja = False
        
            self._experimentos.insertar(nombre, filas, columnas, rejilla, parejas)

    
    def _generar_rejilla(self, archivo, raiz, filas, columnas, estado):
        nombre_archivo = f"{archivo}_estado{estado}"
        with open(f"graficas/{nombre_archivo}.dot", "w", encoding="utf-8") as file:
            file.write("digraph G {\n")
            file.write("\trankdir = LR;\n")
            file.write(f'\tlabel="Estado: {estado}"\n')
            file.write("\tlabelloc=t;\n")
            file.write('\tnode [shape = plaintext, width=3, height=2];\n')
            file.write('\testado [label = <\n')
            file.write('\t\t<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n')
  
            file.write("\t\t\t<TR><TD></TD>")
            for j in range(1, columnas + 1):
                file.write(f"<TD>{j}</TD>")
            file.write("</TR>\n")
         
            fila_actual = raiz
            for i in range(1, filas + 1):
                file.write("\t\t\t<TR>\n")
                file.write(f"\t\t\t\t<TD CELLPADDING='5'>{i}</TD>\n")
                nodo_actual = fila_actual
                for j in range(1, columnas + 1):
                    if nodo_actual:
                        if nodo_actual.get_es_inerte():
                            file.write(f"\t\t\t\t<TD BGCOLOR='red'>{nodo_actual.get_proteina()}</TD>\n")
                        else:
                            file.write(f"\t\t\t\t<TD>{nodo_actual.get_proteina()}</TD>\n")
                        nodo_actual = nodo_actual.siguiente
                    else:
                        file.write("\t\t\t\t<TD></TD>\n")
                file.write("\t\t\t</TR>\n")
                if fila_actual:
                    fila_actual = fila_actual.abajo
            file.write("\t\t</TABLE>>];\n")
            file.write("}\n")

        subprocess.run(f"dot -Tsvg graficas/{nombre_archivo}.dot -o graficas/{nombre_archivo}.svg", shell=True)
        print(f"Se ha generado la gráfica: {estado} del experimento")

class Experimento():
    def __init__(self):
        self._lista_experimento = ListaExperimento()
        self._experimento_xml = None
        self._nombre_ejecutar = None

    def menu_principal(self):  # Listo
        print("\n====================================================")
        print("|          *            Menu          *            |")
        print("====================================================")
        print("| 1. Inicializar sistema                           |")
        print("| 2. Crear catalogo de experimentos                |")
        print("| 3. Desarrollar un experimento                    |")
        print("| 4. Mostrar datos del estudiante                  |")
        print("| 5. Salir                                         |")
        print("====================================================\n")
        try:
            opcion = int(input("Seleccione opcion: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número.")
            return
        
        if opcion == 1:
            self._iniciar_sistema()
        elif opcion == 2:
            self._crear_catalogo()
        elif opcion == 3:
            self._desarrollar_experimento()
        elif opcion == 4:
            self._datos_estudiante()
        elif opcion == 5:
            print("\nSaliendo del programa... ¡Hasta luego!")
            exit()

    def _iniciar_sistema(self):
        self._lista_experimento.limpiar()
        carpeta = 'graficas'
        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                ruta = os.path.join(carpeta, archivo)
                try:
                    if os.path.isfile(ruta):
                        os.remove(ruta)
                except Exception as e:
                    print(f"Error al eliminar {ruta}: {e}")
        else:
            print(f"La carpeta {carpeta} no existe.")
    
    def _crear_catalogo(self):  # Listo
        print("\n====================================================")
        print("|          *      Crear catalogo      *            |")
        print("====================================================")
        print("| 1. Cargar archivo de experimentos                |") 
        print("| 2. Ver estructura del archivo XML de entrada     |") 
        print("| 3. Regresar                                      |") 
        print("====================================================\n")
        try:
            opcion = int(input("Seleccione opcion: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número.")
            return
        
        if opcion == 1:
            self._cargar_experimento()
        elif opcion == 2:
            self._mostrar_estructura()
        elif opcion == 3:
            print("\nRegresando...")

    def _cargar_experimento(self):  # Listo
        Tk().withdraw() 
        archivo_seleccionado = askopenfilename(
            title="Seleccionar un archivo",
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
        )

        if not archivo_seleccionado:
            print("No se seleccionó ningún archivo.")
            return
        
        try:
            self._experimento_xml = ExperimentoXML(archivo_seleccionado)
            self._experimento_xml.extraer_xml()

            self._lista_experimento = self._experimento_xml._experimentos
            print("Experimentos cargados exitosamente.")

        except Exception as e:
            print("Error al leer el archivo XML:", e)
    
    def _mostrar_estructura(self):  # Listo
        print("\n--- Estructura del archivo XML de entrada ---")
        print("""<?xml version="1.0" encoding="UTF-8"?>
        <experimentos>
            <experimento nombre="paciente01">
                <tejido filas="5" columnas="5">
                    <rejilla>
                        LAV LAV VAL VAL VAL
                        VAR RAV GHI VAL VAL
                        LAV AVL ALV LAV LAV
                        VAL ILL KEQ DCC LAV
                        VAR ILL KQA CDC LAV
                    </rejilla>
                </tejido>
                <proteinas>
                    <pareja> LAV VAL </pareja>
                </proteinas>
            </experimento>
            <!-- otros experimentos -->
        </experimentos>""")

    def _desarrollar_experimento(self):  
        print("\n====================================================")
        print("|        *   Desarrollar un experimento    *       |")
        print("====================================================")
        print("| 1. Desarrollar experimento manual                |")
        print("| 2. Cargar un experimento del catálogo            |")
        print("| 3. Regresar                                      |")
        print("====================================================\n")
        try:
            opcion = int(input("Seleccione opcion: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número.")
            return
        
        if opcion == 1:
            self._desarrollo_manual()
            return
        elif opcion == 2:
            self._desarrollo_catalogo()
            return
        elif opcion == 3:
            print("\nRegresando...")

    def _desarrollo_manual(self):  # Listo
        nombre = input("Ingrese nombre del experimento: ").strip()
        try:
            filas = int(input("Ingrese número de filas: ").strip())
            columnas = int(input("Ingrese número de columnas: ").strip())
        except ValueError:
            print("Error: filas y columnas deben ser números.")
            return

        print("Ingrese la rejilla fila por fila, separando las proteínas con espacios:")

        rejilla = ""
        for i in range(filas):
            fila = input(f"Fila {i + 1}: ").strip()
            rejilla += fila + "\n"

        try:
            n_parejas = int(input("Ingrese el número de parejas: ").strip())
        except ValueError:
            print("Error: debe ingresar un número.")
            return

        parejas = ""  
        primera_pareja = True 

        if n_parejas > 0:
            print("Ingrese las parejas de proteínas (ejemplo: PROT1 PROT2):")

        for i in range(n_parejas):  
            pareja_texto = input(f"Pareja {i + 1}: ").strip()
            if pareja_texto:
                if not primera_pareja:
                    parejas += ", " 
                parejas += pareja_texto
                primera_pareja = False

        self._lista_experimento.insertar(nombre, filas, columnas, rejilla, parejas)
        print("\nExperimento guardado\n")

        self._nombre_ejecutar = nombre

        self._forma_de_ejecutar()
        

    def _modificar_experimento(self):  # Listo
        nombre = self._nombre_ejecutar
        if not nombre:
            return  
        experimento_modificar = self._lista_experimento.buscar(nombre)
        
        print(f"\n--- Modificando el experimento: {experimento_modificar.get_nombre()} ---")
        
        print(f"Nombre actual: {experimento_modificar.get_nombre()}")
        nuevo_nombre = input("Ingrese nuevo nombre (o deje vacío para mantener): ").strip()
        if nuevo_nombre != "":
            experimento_modificar._nombre = nuevo_nombre

        try:
            print(f"Numero de filas actuales: {experimento_modificar.get_filas()}")
            nueva_filas = input("Ingrese nuevo valor para filas (o deje vacío para mantener): ").strip()
            if nueva_filas != "":
                experimento_modificar._filas = int(nueva_filas)
        except ValueError:
            print("Valor no numérico; se mantendrá el valor actual.")

        try:
            print(f"Numero de columnas actuales: {experimento_modificar.get_columnas()}")
            nueva_columnas = input("Ingrese nuevo valor para columnas (o deje vacío para mantener): ").strip()
            if nueva_columnas != "":
                experimento_modificar._columnas = int(nueva_columnas)
        except ValueError:
            print("Valor no numérico; se mantendrá el valor actual.")

        print("\nRejilla actual:")
        print(experimento_modificar.get_rejilla())
        if input("¿Desea modificar la rejilla? (s/n): ").strip().lower() == "s":
            rejilla_nueva = ""
            filas_mod = experimento_modificar.get_filas()
            print("Ingrese la rejilla fila por fila, separando las proteínas con espacios:")
            for i in range(filas_mod):
                fila = input(f"Fila {i + 1}: ").strip()
                rejilla_nueva += fila + "\n"
            if rejilla_nueva != "":
                experimento_modificar._rejilla = rejilla_nueva

        print(f"\nPareja(s) actual(es): {experimento_modificar.get_pareja()}")
        if input("¿Desea modificar las parejas de proteínas? (s/n): ").strip().lower() == "s":
            try:
                n_parejas = int(input("Ingrese el nuevo número de parejas: ").strip())
            except ValueError:
                print("Número no válido; se mantendrán las parejas actuales.")
                n_parejas = 0
            parejas_nuevas = ""
            primera = True
            if n_parejas > 0:
                print("Ingrese las parejas de proteínas (ejemplo: PROT1 PROT2):")
            for i in range(n_parejas):
                pareja_texto = input(f"Pareja {i + 1}: ").strip()
                if pareja_texto:
                    if not primera:
                        parejas_nuevas += ", "
                    parejas_nuevas += pareja_texto
                    primera = False
            if parejas_nuevas != "":
                experimento_modificar._pareja = parejas_nuevas

        print("\nExperimento modificado correctamente.\n")
        self._forma_de_ejecutar()

    def _desarrollo_catalogo(self):  # Listo
        if self._lista_experimento.primero is None:
            print("No hay experimentos en el catálogo. Cargue un archivo XML primero.")
            return None  

        print("Experimentos disponibles:")
        tmp = self._lista_experimento.primero

        while tmp:
            print(f"- {tmp.get_nombre()}")
            tmp = tmp.siguiente

        nombre = input("Ingrese el nombre del experimento a ejecutar: ").strip()
        exp = self._lista_experimento.buscar(nombre)
        self._nombre_ejecutar = nombre

        if not exp:
            print("Experimento no encontrado.")
            return None 

        if input("¿Desea modificar el experimento? (s/n): ").strip().lower() == "s":
            self._modificar_experimento()
        else:
            self._forma_de_ejecutar()
        
    def _ingresar_proteinas(self, nombre):
        lista_proteinas = ListaProteina()
        exp = self._lista_experimento.buscar(nombre)
        rejilla = exp.get_rejilla().strip()
        filas = exp.get_filas()
        columnas = exp.get_columnas()
        lista_proteinas.cargar_rejilla_en_lista(rejilla, filas, columnas)
        return lista_proteinas

    def _ejecutar(self):
        nombre = self._nombre_ejecutar
        exp = self._lista_experimento.buscar(nombre)
        if not exp:
            print("Experimento no encontrado.")
            return

        lista_proteinas = self._ingresar_proteinas(nombre)
        filas = exp.get_filas()
        columnas = exp.get_columnas()

        self._experimento_xml._generar_rejilla(f"{nombre}", lista_proteinas.primero, filas, columnas, "Inicial")
        
        parejas = exp.get_pareja()

        for pareja in parejas.split(","):
            proteina01, proteina02 = pareja.split()
            lista_proteinas.buscar_parejas(proteina01, proteina02)

        self._experimento_xml._generar_rejilla(f"{nombre}", lista_proteinas.primero, filas, columnas, "Final")

        porcentaje = lista_proteinas.contar_porcentaje_inertes()
        self._resultado(porcentaje)
        
    def _ejecutar_pasos(self):
        nombre = self._nombre_ejecutar
        exp = self._lista_experimento.buscar(nombre)
        if not exp:
            print("Experimento no encontrado.")
            return

        lista_proteinas = self._ingresar_proteinas(nombre)
        filas = exp.get_filas()
        columnas = exp.get_columnas()

        self._experimento_xml._generar_rejilla(f"{nombre}", lista_proteinas.primero, filas, columnas, 1) 

        index = 1
        listo = False

        for pareja in exp.get_pareja().split(","):
            proteina01, proteina02 = pareja.split()
            listo = lista_proteinas.buscar_parejas(proteina01, proteina02)
            if listo:
                index += 1
                self._experimento_xml._generar_rejilla(f"{nombre}", lista_proteinas.primero, filas, columnas, index)

        porcentaje = lista_proteinas.contar_porcentaje_inertes()
        self._resultado(porcentaje)

    def _cargar_rejilla_en_lista(self, exp):
        rejilla_txt = exp.get_rejilla().strip()
        primera_fila = None
        fila_anterior = None
        for linea in rejilla_txt.splitlines():
            linea = linea.strip()
            if linea == "":
                continue
            palabras = linea.split()
            cabeza_fila = None
            nodo_anterior = None
            for palabra in palabras:
                nuevo = NodoProteina(palabra, False)
                if cabeza_fila is None:
                    cabeza_fila = nuevo
                else:
                    nodo_anterior.siguiente = nuevo
                nodo_anterior = nuevo

            if fila_anterior is not None:
                nodo_actual = cabeza_fila
                nodo_superior = fila_anterior
                while nodo_actual is not None and nodo_superior is not None:
                    nodo_superior.abajo = nodo_actual
                    nodo_superior = nodo_superior.siguiente
                    nodo_actual = nodo_actual.siguiente
            else:
                primera_fila = cabeza_fila
            fila_anterior = cabeza_fila
        lista_proteinas = ListaProteina()
        lista_proteinas.primero = primera_fila
        return lista_proteinas

    def _forma_de_ejecutar(self):
        while True:
            if not os.path.exists('graficas'):
                os.makedirs('graficas')
            print("\n====================================================")
            print("|         *       Forma de Ejecución      *        |")
            print("====================================================")
            print("| 1. Paso a paso                                   |")
            print("| 2. Directamente                                  |")
            print("| 3. Regresar                                      |")
            print("====================================================\n")
            
            try:
                opcion = int(input("Seleccione opcion: ").strip())
                if opcion == 1:
                    self._ejecutar_pasos()
                    break  
                elif opcion == 2:
                    self._ejecutar()
                    break  
                elif opcion == 3:
                    print("\nRegresando...")
                    break 
                else:
                    print("Opción no válida. Intente de nuevo.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")

    
    def _resultado(self, porcentaje):
        print("\nResultados del experimento:")
        if porcentaje >= 30 and porcentaje <= 60:
            print("Medicamento exitoso")
        elif porcentaje > 0 and porcentaje < 30:
            print("Medicamento no eficiente")
        elif porcentaje > 60 and porcentaje < 100:
            print("Medicamento fatal")
        else:
            print("Resultado fuera de rango definido")
    
    def _datos_estudiante(self):
        print("\n==============================================================")
        print("|             *      Datos del Estudiante     *              |")
        print("==============================================================")
        print("| Carné: 201942079                                           |")
        print("| Nombre: Luz de Maria Jose Castillo Flores                  |")
        print("| Curso: Introducción a la Programación y Computación 2      |")
        print("| Carrera: Ingeniería en Sistemas                            |")
        print("| Semestre: 4to                                              |")
        print("==============================================================\n")
        print("Documentación: https://drive.google.com/drive/folders/15elavU79BfjLuztjmmmCp9a7bpJ-OZQM?usp=drive_link ")
        while True:    
            opcion = input("Presione Enter para regresar al menú... ").strip()
            if opcion == "":
                print("\nRegresando...")
                break
            else:
                print("\nPor favor, solo presione Enter.")

if __name__ == "__main__":
    exp = Experimento()
    while True:
        exp.menu_principal()

from clases import *
dic_archivos = {}
pacientes = {} 
medios = {}

def main():
    
    carpeta_imagenes = os.getcwd()
    archivo_dicom = DICOM()
    pacientes = {} 
    medios = {}  
    
    while True:
        print("\n=== Menú Principal ===")
        print("a) Procesar carpeta DICOM")
        print("b) Ingresar Paciente")
        print("c) Ver imágenes disponibles y seleccionar")
        print("d) Procesar imagen (binarización + morfología + forma + texto)")
        print("e) Aplicar translación")
        print("f) Salir")
        opc = input("Opción: ").lower()
        